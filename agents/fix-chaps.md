---
name: fix-chaps
description: Replaces the November 2026 CHAPS address date with the Bank of England deferral on six pages
stage: 2 Pages
inputs: STYLE.md, Bank of England notice of 27 August 2026, the six pages
outputs: edits to account-map, banking, demand, first-months, new-logos and portfolio pages
run: 21 tool calls, 123,040 tokens, 5.7 min
---

On 27 August 2026 the Bank of England deferred its November 2026 RTGS standards release in its entirety, with no new date; the November 2027 purpose-code and LEI mandates stand. Rewrite every occurrence on the six pages so the deferral is stated where the date was a selling point, or the November 2027 mandate becomes the forcing event. Make plain readings and captions true again. Add the Bank of England source to each Sources panel. On First Months, quote the CFO's full phrase on Europe growth. Build, screenshot, require scrollX=0 and errors=0.
