# Analizador-Web Audit Checklist

Use this checklist to interpret the JSON report and screenshots. It is an inspection aid, not a formal certification.

## Scope and evidence
- [ ] Confirm authorization and target scope.
- [ ] Record the exact URL, timestamp, viewport, crawl limit, and tool version.
- [ ] Distinguish observed facts, heuristic detections, and assumptions.
- [ ] Record blocked pages, timeouts, bot challenges, and other limitations.

## Visual quality and UX
- [ ] Is the purpose of the site understandable within a few seconds?
- [ ] Is the primary call to action visible and unambiguous?
- [ ] Is the visual hierarchy consistent?
- [ ] Are text size, line length, spacing, and contrast comfortable?
- [ ] Are there overlapping elements, broken images, intrusive banners, or layout shifts?
- [ ] On mobile, is text readable without zoom?
- [ ] Are interactive targets sufficiently large and separated?
- [ ] Is there horizontal overflow?
- [ ] Are navigation and key content usable at narrow widths?

## Technical SEO
- [ ] Page title exists, is descriptive, and is reasonably unique.
- [ ] Meta description exists and describes the page.
- [ ] Heading hierarchy is meaningful; check for missing or excessive H1 headings.
- [ ] Document language is declared.
- [ ] Viewport metadata is present.
- [ ] Canonical URL is present and plausible.
- [ ] Open Graph metadata is available where sharing matters.
- [ ] Robots directives do not unintentionally block indexing.
- [ ] Important content is rendered and discoverable.

## Performance indicators
- [ ] Review navigation timing, DOMContentLoaded, load, and paint entries when available.
- [ ] Review transfer-size and resource-count indicators.
- [ ] Identify unusually large resources and third-party scripts.
- [ ] Consider image formats, responsive images, lazy loading, caching, and CDN use.
- [ ] Treat measurements as a single browser run affected by network, cache, geography, and request interception.
- [ ] Use Lighthouse or PageSpeed Insights separately for a more complete performance assessment.

## Accessibility signals
- [ ] Images have appropriate alternative text (decorative images may use empty alt).
- [ ] Form controls have programmatic labels.
- [ ] Links and buttons have accessible names.
- [ ] Page language is declared.
- [ ] Keyboard focus is visible and navigation is possible.
- [ ] Contrast is reviewed with a dedicated tool.
- [ ] Heading order and landmarks are meaningful.
- [ ] Do not claim WCAG conformance from this checklist alone.

## Security configuration observations
- [ ] HTTPS is used.
- [ ] Certificate validation succeeds in a normal browser context.
- [ ] Review HSTS, CSP, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, and frame protections.
- [ ] Treat server-identifying headers as informational exposure, not automatically as a vulnerability.
- [ ] Do not infer application security from public headers alone.
- [ ] Do not exploit, probe hidden endpoints, or test authentication.

## Reliability
- [ ] Review JavaScript console errors.
- [ ] Review failed network requests.
- [ ] Review HTTP responses with status 4xx/5xx.
- [ ] Check same-host links only when explicitly requested.
- [ ] Treat HEAD-only link checks as incomplete; some servers reject HEAD.

## Prioritization
- **High:** core page unavailable, broken primary navigation, severe mobile layout failure, widespread application errors, or important content inaccessible.
- **Medium:** missing essential metadata, heavy resources, recurring console errors, missing defensive headers where appropriate.
- **Low:** minor visual inconsistencies, non-critical metadata, or optional optimizations.

Every finding should include the evidence, impact, confidence, and a concrete next action.
