# Wipro application: ICD Practitioner, UK and Ireland

A static site of research, decision models and plans for the ICD Practitioner role in Wipro's Industry Cloud & Digital portfolio, UK and Ireland. Built from October 2026.

## Site
The published site is the `docs/` folder. Open `docs/index.html`. It is a password page; only a salted hash of the password is stored here. After the password the reader lands on `overview.html`, the analysis index.

The pages are shown on screen in a panel interview and then shared with Wipro. Writing rules are in `build/STYLE.md`.

Analysis pages, numbered in the navigation bar:
A1 `role.html`, A2 `portfolio.html`, A3 `demand.html`, A4 `buyers.html`, A5 `accounts.html`, A6 `alternatives.html`, A7 `deal-shaping.html`, A8 `pursuits.html`, A9 `workshops.html`, A10 `ai-engagement.html`, A11 `first-months.html`.
About me, linked in the header: `ai.html` (AI Workflow) and `method.html` (Method: how the site was made and the agents that built it).

## Build
Page bodies live in `build/pages/`. Run `python3 build/build.py` to rebuild `docs/`: it copies `assets/`, wraps each page with the shared head, navigation and footer and writes `docs/index.html` from `build/gate.html`. Do not edit files in `docs/` by hand. Put the password in `build/.password` (ignored by git) to change it; otherwise the stored hash in `build/gate.hash` is reused.

Styles: `assets/site.css`, `nav.css`, `a11y.css`, `viz.css` and `viz.js` (chart helpers) come from the One Click LCA site. `assets/pages.css` holds the page components and the indigo accent.

`tools/shoot.js` screenshots every page at 1440 px light and 390 px dark and reports console errors, sideways scroll and axe-core results. Serve `docs/` on port 8765 first.

## Research
`research/` holds the sourced research behind the pages: `wipro.md`, `uki-market.md`, `competitors.md`, `deals.md`. Claims are flagged verified, secondary or unverified.

## Other files
- `job-description.txt`: the listing
- `PLAN.md`: the build plan
- `session-notes.md`: decisions and open points
- `agents/`: one markdown record per Claude Code agent used to build the site, plus the shared briefs

## Publishing
Publish the `docs/` folder only, for example with GitHub Pages set to deploy from this branch and the `/docs` folder. The password check runs in the browser, so it hides the pages from casual visitors but does not protect them: anyone with a page URL can fetch its HTML. Pages carry `noindex`.
