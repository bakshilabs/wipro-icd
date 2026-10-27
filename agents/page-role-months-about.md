---
name: page-role-months-about
description: Writes A1 The Role, A11 First Months, AI Workflow and CV
stage: 2 Pages
inputs: page-brief.md, research/*.md, CV
outputs: build/pages/role.html, first-months.html, ai.html, cv.html
run: 49 tool calls, 257,173 tokens, 13 min
---

Read agents/page-brief.md first and follow it exactly.

1. role.html, "The Role" (A1). Every responsibility line mapped to the page that answers it and to my experience. Where the role sits in Wipro. Interactive: a responsibility matrix, a coverage chart, count-up figures.

2. first-months.html, "First Months" (A11). Listen, decide, deliver over the first year; targets labelled "My estimate, to set with my manager". Interactive: a phase stepper or Gantt, a pipeline build chart, a measures panel.

3. ai.html, "AI Workflow". How I would bring AI working practices to a pursuit team, with a routine library of example prompts.

4. cv.html, "CV". Adapted from the One Click LCA CV, retitled for this role, facts unchanged.
