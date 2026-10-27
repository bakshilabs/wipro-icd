# Plan: Wipro ICD Practitioner interview site

## Context
Arpan is applying for the ICD Practitioner role (Industry Cloud & Digital, UKI) at Wipro and will present a website in a panel round with no set brief. He likes the Research Appendix of `bakshilabs/oneclicklca` (the `overview.html` index plus numbered A1–A12 pages with interactive SVG charts, tabs, pinned tooltips, a section stepper, light and dark themes). The new site is that analysis section only: an index page and numbered analysis pages, each answering lines of the job description. The weight sits on AI solutions (Claude and Gemini), digital and customer experience, and advisory sales and deal shaping, which is where Arpan's experience is strongest. The site keeps the password gate and `noindex`.

`wipro-icd` is empty (branch `claude/epic-ride-e81q54`, no commits). The reference repo is cloned read-only at `/home/user/bakshilabs/oneclicklca`.

## Reuse from oneclicklca
- `build/build.py`: page wrapping, nav, pager, footer, salted-hash gate. Adapt: new `SALT`, brand line "Arpan Bakshi · Wipro ICD Practitioner", one group only (index + appendix codes A1…), drop the meeting nav and the separate appendix bar so the code bar becomes the main nav.
- `build/gate.html`, `build/STYLE.md` (writing rules already match the user's preferences; change company references and drop the "no figures on meeting pages" rule).
- `assets/site.css`, `nav.css`, `a11y.css`, `viz.css`, `viz.js` unchanged (chart helpers `VZ.el/svg/lin/bar/tip/tabs`, stepper, count-up).
- `assets/pages.css`: same components, with a new neutral accent (deep indigo, light and dark variants). No Wipro logo, colours or branding; footer says it is independent work from public sources that Wipro did not produce or review.
- `build/pages/overview.html` layout for the index (hero, headline finding cards, filterable page cards with SVG thumbnails).
- `build/pages/cv.html` and `assets/arpan-bakshi.jpg` as the starting CV, retitled for IC&D.
- `build/pages/ai.html` as the template for the AI workflow page.

## Research first
Four parallel agents write sourced notes to `research/` (claims flagged verified, secondary or unverified, every link dated):
1. `wipro.md`: Wipro structure and the IC&D practice offerings, UKI presence and named public clients, alliance partners (Google Cloud and Gemini, Anthropic and Claude, Microsoft, AWS, ServiceNow, Salesforce), Wipro's AI programmes, recent results by region.
2. `uki-market.md`: UK and Ireland demand drivers by sector (financial services, public sector, retail, utilities, health, telecoms): legacy and mainframe estates, FCA Consumer Duty, operational resilience and DORA, public sector digital spend, AI adoption surveys, cloud spend.
3. `competitors.md`: Accenture, TCS, Infosys, Cognizant, Capgemini, HCLTech, Deloitte, IBM and specialist CX and AI firms, with their UKI AI and CX offers and alliances.
4. `deals.md`: how services deals are shaped and priced in the market (pyramid, onshore and offshore mix, fixed price against time and materials, outcome-based pricing, AI effect on effort and price), from public sources.

## Pages (`build/pages/`)
| Code | File | Title | Job description lines | Main interactive element |
|---|---|---|---|---|
| Index | `overview.html` | Analysis | All | Hero chart of UKI demand by sector and offering; headline finding cards; filterable page cards |
| A1 | `role.html` | The Role | All | Matrix of responsibilities against my evidence, click a row for detail |
| A2 | `portfolio.html` | IC&D Portfolio | Position and sell offerings | Offering by buyer problem grid with tabs for AI, CX, modernisation, engineering |
| A3 | `demand.html` | UKI Demand | Identify large transformation opportunities | Sector drivers timeline and heat table |
| A4 | `buyers.html` | Buyers | Executive relationships, trusted advisor | Persona tabs (CIO, CDO, CX director, CFO, COO, procurement): trigger, criteria, objections |
| A5 | `accounts.html` | Account Model | Hunting and farming, expand presence | Scoring model for new and existing accounts with editable placeholder weights |
| A6 | `alternatives.html` | Competitors | Differentiated solutions | Rated comparison with sources and dates |
| A7 | `deal-shaping.html` | Deal Shaping | Margin-positive deals, pricing, scope | Margin calculator (mix, rates, pyramid, contingency, AI productivity), placeholder figures labelled |
| A8 | `pursuits.html` | Pursuits | Qualification, RFPs, deal closure | Bid and no-bid scorecard and pursuit stage stepper |
| A9 | `workshops.html` | Executive Workshops | Facilitate workshops, align priorities | Workshop agenda builder with outputs per session |
| A10 | `ai-engagement.html` | AI Engagement Models | AI-enabled engagement models, Claude and Gemini | Use case value against feasibility chart for CX use cases |
| A11 | `first-months.html` | First Months | OB and revenue contribution | Listen, decide, deliver plan with targets labelled as my estimates |
| A12 | `ai.html` | AI Workflow | AI adoption | How the site was researched and built with Claude Code agents |
| A13 | `cv.html` | CV | Background | Adapted from the oneclicklca CV |

All pages follow `STYLE.md`: plain-noun titles, first person, full sentences, British spelling, no em dashes, no contrast constructions, no closing summary lines, judgement and placeholder figures labelled, outside readings of Wipro stated as such.

## Other files
- `README.md`, `job-description.txt` (the listing as given), `PLAN.md` (this plan), `session-notes.md`, `.gitignore` (`build/.password`, `private/`).
- Build output in `docs/` for GitHub Pages. I will ask for the password before the gate is built; until then a placeholder hash is used.

## Build order
1. Copy and adapt build system and assets; build one stub page to check the shell.
2. Research agents (parallel).
3. Pages in parallel batches by page agents: A2–A6, then A7–A10, then index, A1, A11–A13.
4. Independent review pass per page for accuracy against `research/` and for the writing rules.
5. Commit and push to `claude/epic-ride-e81q54`.

## Verification
- `python3 build/build.py` writes every page with no "missing" lines.
- Serve `docs/` locally and use Playwright (pre-installed Chromium) to open every page at 1440 and 390 px in light and dark: no console errors, no horizontal scroll, screenshots saved to `shots/` for review.
- Run axe-core in the same Playwright pass on each page in both themes.
- Grep page bodies for banned patterns (em dashes, "not … but", listed hype words).
- Check the gate: wrong password rejected, right password opens `overview.html`, direct page URLs redirect to the gate.
