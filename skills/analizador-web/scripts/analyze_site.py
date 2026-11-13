#!/usr/bin/env python3
"""Passive website inspection with Chromium and Playwright for Python."""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse, urldefrag

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from safety import UnsafeTarget, validate_public_url, redact_url

SECURITY_HEADERS = [
    "strict-transport-security", "content-security-policy", "x-frame-options",
    "x-content-type-options", "referrer-policy", "permissions-policy",
]
EXTRACT = """() => {
 const q=s=>document.querySelector(s);
 const meta=n=>(q('meta[name="'+n+'"]')||q('meta[property="'+n+'"]'))?.content||null;
 const imgs=[...document.images], resources=performance.getEntriesByType('resource');
 const nav=performance.getEntriesByType('navigation')[0];
 return {
  title:document.title, lang:document.documentElement.lang||null,
  meta_description:meta('description'), viewport:meta('viewport'), robots:meta('robots'),
  canonical:q('link[rel="canonical"]')?.href||null,
  open_graph:{title:meta('og:title'),description:meta('og:description'),image:meta('og:image')},
  headings:[...document.querySelectorAll('h1,h2,h3')].slice(0,60).map(x=>({tag:x.tagName.toLowerCase(),text:x.innerText.trim().slice(0,120)})),
  h1_count:document.querySelectorAll('h1').length, images_total:imgs.length,
  images_without_alt:imgs.filter(i=>!i.hasAttribute('alt')).length,
  inputs_without_label:[...document.querySelectorAll('input:not([type=hidden]),textarea,select')].filter(i=>!(i.labels&&i.labels.length)&&!i.getAttribute('aria-label')).length,
  links:[...document.querySelectorAll('a[href]')].map(a=>a.href),
  word_count:(document.body?.innerText||'').trim().split(/\\s+/).filter(Boolean).length,
  text_excerpt:null,
  timing_ms:nav?{ttfb:Math.round(nav.responseStart-nav.requestStart),dom_content_loaded:Math.round(nav.domContentLoadedEventEnd),load:Math.round(nav.loadEventEnd)}:{},
  resources_count:resources.length,
  transfer_kb_total:Math.round(resources.reduce((n,r)=>n+(r.transferSize||0),0)/1024),
  heaviest_resources:resources.map(r=>({url:r.name,kb:Math.round((r.transferSize||0)/1024),type:r.initiatorType})).sort((a,b)=>b.kb-a.kb).slice(0,10)
 };
}"""

def safe_route(route):
    try:
        validate_public_url(route.request.url)
    except UnsafeTarget:
        route.abort("blockedbyclient")
    else:
        route.continue_()


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("url")
    ap.add_argument("--out",default="./website-audit")
    ap.add_argument("--crawl",type=int,default=0)
    ap.add_argument("--no-mobile",action="store_true")
    ap.add_argument("--wait",type=int,default=1000)
    ap.add_argument("--timeout",type=int,default=30000)
    ap.add_argument("--check-links",type=int,default=0)
    ap.add_argument("--include-text-excerpt",action="store_true")
    args=ap.parse_args()
    if not 0<=args.crawl<=20 or not 0<=args.check_links<=40:
        ap.error("--crawl must be 0..20 and --check-links 0..40")
    try:
        start=validate_public_url(args.url if "://" in args.url else "https://"+args.url)
    except UnsafeTarget as exc:
        ap.error(str(exc))

    out=Path(args.out); shots=out/"screenshots"; shots.mkdir(parents=True,exist_ok=True)
    report={"start_url":redact_url(start),"pages":[],"notes":["Passive inspection only. Timing is a single browser observation.","URL validation is defense-in-depth, not a hardened network sandbox."]}
    with sync_playwright() as p:
        browser=p.chromium.launch()
        desktop=browser.new_context(viewport={"width":1440,"height":900})
        desktop.route("**/*",safe_route)
        mobile=None
        if not args.no_mobile:
            mobile=browser.new_context(**p.devices["iPhone 13"])
            mobile.route("**/*",safe_route)
        queue=[start]; seen=set()
        while queue and len(report["pages"])<1+args.crawl:
            url=queue.pop(0)
            if url in seen: continue
            seen.add(url)
            try: validate_public_url(url)
            except UnsafeTarget: continue
            page=desktop.new_page(); errors=[]; failed=[]; statuses=[]
            page.on("console",lambda m: errors.append(m.text[:250]) if m.type=="error" else None)
            page.on("pageerror",lambda e: errors.append("JS: "+str(e)[:250]))
            page.on("requestfailed",lambda r: failed.append({"url":redact_url(r.url),"error":r.failure}))
            page.on("response",lambda r: statuses.append({"url":redact_url(r.url),"status":r.status}) if r.status>=400 else None)
            item={"url":redact_url(url)}
            began=time.monotonic()
            try:
                response=page.goto(url,wait_until="domcontentloaded",timeout=args.timeout)
                try: page.wait_for_load_state("networkidle",timeout=min(8000,args.timeout))
                except PlaywrightTimeoutError: pass
                if args.wait: page.wait_for_timeout(min(args.wait,10000))
                data=page.evaluate(EXTRACT)
                if args.include_text_excerpt:
                    data["text_excerpt"]=page.locator("body").inner_text(timeout=3000)[:500]
                headers={k.lower():v for k,v in (response.all_headers().items() if response else [])}
                final=page.url
                item.update(data)
                item.update({"final_url":redact_url(final),"status":response.status if response else None,
                    "https":urlparse(final).scheme=="https","security_headers_missing":[h for h in SECURITY_HEADERS if h not in headers],
                    "elapsed_seconds":round(time.monotonic()-began,2),"console_errors":errors[:20],
                    "failed_requests":failed[:20],"http_errors":statuses[:20]})
                name=re.sub(r"[^a-zA-Z0-9]+","_",urlparse(final).netloc+urlparse(final).path)[:70] or "page"
                deskfile=shots/(name+"_desktop.png"); page.screenshot(path=str(deskfile),full_page=True)
                item["screenshots"]={"desktop":str(deskfile)}
                if mobile:
                    mp=mobile.new_page()
                    try:
                        mp.goto(url,wait_until="domcontentloaded",timeout=args.timeout)
                        try: mp.wait_for_load_state("networkidle",timeout=min(8000,args.timeout))
                        except PlaywrightTimeoutError: pass
                        overflow=mp.evaluate("() => document.documentElement.scrollWidth > window.innerWidth + 2")
                        mobfile=shots/(name+"_mobile.png"); mp.screenshot(path=str(mobfile),full_page=True)
                        item["screenshots"]["mobile"]=str(mobfile); item["mobile_horizontal_overflow"]=overflow
                    except Exception as exc: item["mobile_error"]=str(exc)[:200]
                    finally: mp.close()
                if args.crawl and url==start:
                    host=urlparse(final).hostname
                    for link in data.get("links",[]):
                        clean=urldefrag(link)[0]
                        if urlparse(clean).hostname==host and clean not in seen and clean not in queue:
                            try: validate_public_url(clean); queue.append(clean)
                            except UnsafeTarget: pass
                if args.check_links and url==start:
                    item["link_checks"]=[]
                    for link in data.get("links",[])[:args.check_links]:
                        try:
                            validate_public_url(link)
                            result=page.request.head(link,timeout=7000)
                            item["link_checks"].append({"url":redact_url(link),"status":result.status})
                        except Exception as exc:
                            item["link_checks"].append({"url":redact_url(link),"error":str(exc)[:120]})
            except Exception as exc:
                item["error"]=str(exc)[:300]
            finally: page.close()
            report["pages"].append(item)
        browser.close()
    (out/"report.json").write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
    lines=["# Website audit", "",f"- Target: {report['start_url']}",f"- Pages inspected: {len(report['pages'])}",""]
    for item in report["pages"]:
        lines += [f"## {item.get('final_url',item['url'])}",""]
        if item.get("error"): lines += [f"Could not inspect: {item['error']}",""]; continue
        lines += [f"- HTTP: {item.get('status')} | HTTPS: {item.get('https')}",
          f"- Title: {item.get('title')}",f"- Meta description: {item.get('meta_description')}",
          f"- H1 count: {item.get('h1_count')} | Images without alt: {item.get('images_without_alt')}",
          f"- Resources: {item.get('resources_count')} | Transfer: {item.get('transfer_kb_total')} KB",
          f"- Missing security headers: {', '.join(item.get('security_headers_missing',[])) or 'none'}",
          f"- Console errors: {len(item.get('console_errors',[]))} | HTTP errors: {len(item.get('http_errors',[]))}",""]
    (out/"summary.md").write_text("\n".join(lines),encoding="utf-8")
    print(f"Audit saved to {out.resolve()}")

if __name__=="__main__": main()
