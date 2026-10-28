# Wipro application: ICD Practitioner, UK and Ireland

A static site of research, decision models and plans for the ICD Practitioner role in Wipro's Industry Cloud & Digital portfolio, UK and Ireland. Built from October 2026.

## Site
The published site is the `docs/` folder, live at https://bakshilabs.github.io/wipro-icd/ (GitHub Pages from `main`, `/docs`). Open `docs/index.html`, which forwards to `overview.html`, the overview, written as a brief in six sections: situation, argument, strategy, plan, vision and pages. The site has no password; pages carry `noindex`.

The pages are shown on screen in a panel interview and then shared with Wipro. Writing rules are in `build/STYLE.md`.

Meeting pages, concise and visual, shown on screen in the interview: M1 `situation.html`, M2 `fit.html`, M3 `strategy.html`, M4 `banking-first.html`, M5 `plan.html`, M6 `vision.html`.
Appendix pages, the full analysis, models and sources: A1 `role.html`, A2 `portfolio.html`, A3 `ai-engagement.html`, A4 `demand.html`, A5 `alternatives.html`, A6 `buyers.html`, A7 `accounts.html`, A8 `account-map.html`, A9 `new-logos.html`, A10 `workshops.html`, A11 `pursuits.html`, A12 `deal-shaping.html`, A13 `banking.html`, A14 `first-months.html`. The navigation bar shows Meeting and Appendix as dropdown menus.
About me, linked in the header: `ai.html` (AI Workflow) and `method.html` (Method: how the site was made and the agents that built it).

## Build
Page bodies live in `build/pages/`. Run `python3 build/build.py` to rebuild `docs/`: it copies `assets/`, wraps each page with the shared head, navigation and footer, and writes `docs/index.html`. Do not edit files in `docs/` by hand. Pages listed in `HIDDEN` in `build/build.py` are built without navigation links; the list holds `preparation.html`, a one-page interview preparation dashboard reachable only by its address. Interview notes live in `private/`, which git ignores and the build does not read.

Styles: `assets/site.css`, `nav.css`, `a11y.css`, `viz.css` and `viz.js` (chart helpers) come from the One Click LCA site. `assets/pages.css` holds the page components and the indigo accent.

`tools/method/gen.py` regenerates `build/pages/method.html` from `tools/method/template.html`, `agents/*.md` and `research/*.md`; run it after any agent record changes, then the build.

`tools/shoot.js` screenshots every page at 1440 px light and 390 px dark and reports console errors, sideways scroll and axe-core results. Serve `docs/` on port 8765 first.

## Research
`research/` holds the sourced research behind the pages: `wipro.md`, `uki-market.md`, `competitors.md`, `deals.md`. Claims are flagged verified, secondary or unverified.

## Other files
- `job-description.txt`: the listing
- `PLAN.md`: the build plan
- `session-notes.md`: decisions and open points
- `agents/`: one markdown record per Claude Code agent used to build the site, plus the shared briefs

## Publishing
Publish the `docs/` folder only, for example with GitHub Pages set to deploy from this branch and the `/docs` folder. Anyone with the address can read every page, including unlisted ones.
