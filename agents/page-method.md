---
name: page-method
description: Writes the Method page describing how the analysis section was made
stage: 2 Pages
inputs: page-brief.md, agents/*.md, research/*.md, build.py, shoot.js
outputs: build/pages/method.html, ai.html (shortened build section)
run: to be recorded
---

Read agents/page-brief.md first and follow it exactly.

Write method.html, "Method": how the analysis section was created, including every agent. Organisation of the work, one entry per agent from agents/*.md (stage, job, inputs, outputs, tool calls, tokens, time), the rules every page followed, totals, and how I would reuse the approach on a Wipro pursuit. Interactive: an agent pipeline diagram with selectable nodes and each agent's instructions, a chart comparing agents by tool calls, tokens or minutes, and a claims-by-flag chart per research file. Shorten the build section of ai.html to a link to this page.
