---
name: page-meeting-situation-fit
description: Writes M1 Situation and M2 Fit, the first two meeting pages
stage: 2 Pages
inputs: meeting-brief.md, STYLE.md, page-brief.md, overview.html, role.html
outputs: build/pages/situation.html, build/pages/fit.html
run: 45 tool calls, 205,130 tokens, 9.2 min
---

Read the meeting brief. M1 Situation: three screens with the three Wipro figures as large tiles, the operating margin chart against peers with the bookings and large-deal tiles, and a selectable diagram linking each figure to one of three asks. M2 Fit: a career timeline from 2008 to 2026 with selectable stops, the four reasons as panels with appendix links, and a heat grid of the six responsibility groups against the five experience strands. Keep every claim inside the record in the brief. Build, screenshot, require scrollX=0 and errors=0.
