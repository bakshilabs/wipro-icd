---
name: page-portfolio-demand
description: Writes A2 Portfolio and A3 Demand
stage: 2 Pages
inputs: page-brief.md, research/*.md, CV
outputs: build/pages/portfolio.html, demand.html
run: 43 tool calls, 240,513 tokens, 14 min
---

Read agents/page-brief.md first and follow it exactly.

1. portfolio.html, "Portfolio" (A2). Answers "Position and sell IC&D Practice Offerings" and "Collaborate with Wipro global practices, delivery organisations, and alliance partners". Where IC&D sits in Wipro; each offering in the job description mapped to the buyer problem it solves, the UKI buyer, the alliance partner and proof points. Interactive: a clickable structure diagram, an offering-by-problem grid with tabs, an alliances timeline, a proposition builder with draft messages.

2. demand.html, "Demand" (A3). Answers "Identify and shape large-scale digital transformation opportunities" and "Expand Wipro's presence across UKI clients". Sector demand drivers, dated forces, CX pressure, legacy estate and AI adoption data. Interactive: a sector-by-offering heat matrix, a filterable timeline of forcing dates, count-up figures, a pursuit panel per sector.
