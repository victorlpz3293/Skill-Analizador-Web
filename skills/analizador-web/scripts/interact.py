#!/usr/bin/env python3
"""Controlled browser interaction. Mutating interactions are disabled by default."""
import argparse, json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from safety import UnsafeTarget, validate_public_url, redact_url


def route_guard(route):
    try: validate_public_url(route.request.url)
    except UnsafeTarget: route.abort("blockedbyclient")
    else: route.continue_()


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("url")
    ap.add_argument("--steps",required=True,help="JSON string or path to a JSON file")
    ap.add_argument("--out",default="./website-audit")
    ap.add_argument("--mobile",action="store_true")
    ap.add_argument("--timeout",type=int,default=20000)
    ap.add_argument("--allow-interactions",action="store_true",help="Enable click/fill/press; only use on authorized test systems")
    a=ap.parse_args()
    try: start=validate_public_url(a.url if "://" in a.url else "https://"+a.url)
    except UnsafeTarget as exc: ap.error(str(exc))
    \n    candidate=Path(a.steps)\n    try: is_file=candidate.is_file()\n    except OSError: is_file=False\n    raw=candidate.read_text(encoding="utf-8") if is_file else a.steps
    try: steps=json.loads(raw)
    except Exception as exc: ap.error(f"Invalid steps JSON: {exc}")
    if not isinstance(steps,list): ap.error("Steps must be a JSON array")
    out=Path(a.out); shots=out/"screenshots"; shots.mkdir(parents=True,exist_ok=True); log=[]
    with sync_playwright() as p:
        browser=p.chromium.launch()
        context=browser.new_context(**p.devices["iPhone 13"]) if a.mobile else browser.new_context(viewport={"width":1440,"height":900})
        context.route("**/*",route_guard)
        page=context.new_page(); page.set_default_timeout(a.timeout)
        try: page.goto(start,wait_until="domcontentloaded")
        except Exception as exc: ap.error(f"Navigation failed: {exc}")
        for index,step in enumerate(steps,1):
            action=step.get("action"); entry={"step":index,"action":action}
            try:
                if action=="goto":
                    target=validate_public_url(step["url"]); page.goto(target,wait_until="domcontentloaded")
                elif action in ("click","fill","press"):
                    if not a.allow_interactions: raise PermissionError("click/fill/press require --allow-interactions")
                    if action=="click": page.locator(step["selector"]).click()
                    elif action=="fill": page.locator(step["selector"]).fill(step.get("value",""))
                    else: page.locator(step["selector"]).press(step["key"])
                elif action=="wait": page.wait_for_timeout(min(max(int(step.get("ms",1000)),0),10000))
                elif action=="scroll": page.mouse.wheel(0,min(max(int(step.get("y",600)),-3000),3000))
                elif action=="screenshot":
                    dest=shots/(str(step.get("name",f"step-{index}"))+".png"); page.screenshot(path=str(dest),full_page=bool(step.get("full_page",False))); entry["screenshot"]=str(dest)
                elif action=="text": entry["text"]=page.locator(step.get("selector","body")).inner_text()[:3000]
                else: raise ValueError("Unsupported action")
                entry["current_url"]=redact_url(page.url)
            except Exception as exc: entry["error"]=str(exc)[:300]
            log.append(entry); print(json.dumps(entry,ensure_ascii=False))
        browser.close()
    (out/"interaction.json").write_text(json.dumps(log,indent=2,ensure_ascii=False),encoding="utf-8")

if __name__=="__main__": main()
