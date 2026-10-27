# Session notes

## 27 October 2026
- Scaffolded the site from `bakshilabs/oneclicklca` (build, assets, gate). Analysis pages only, password gate kept, indigo accent, no Wipro branding.
- Research agents writing `research/wipro.md`, `uki-market.md`, `competitors.md`, `deals.md`.
- User instruction: never show gaps. No page states missing experience or weaknesses; rule added to `build/STYLE.md`.
- Fourteen agents in all: four research, five page, an index agent, a Method page agent and three reviewers. Records in `agents/`.
- The CV page was removed at the user's request. The site has 14 pages: the index, A1 to A11, AI Workflow and Method.
- All 14 pages pass at 1440 px light and 390 px dark: no sideways scroll, no console errors, axe-core clean.
- To confirm: Government Commercial Agency replacing CCS, EU AI Act Omnibus dates, Allied Irish Banks contract status, Wipro's G-Cloud 15 listing, Europe constant-currency growth (broker figure), competitor ratings against UK analyst rankings, aggregator deal values.
- The password is a random placeholder in `build/.password`; set the real one and rebuild.

## 27 October 2026, later
- Independent review (four agents, 133 claims checked against primary sources): the Wipro figures hold; the November 2026 CHAPS address rule was deferred by the Bank of England on 27 August 2026; RSA and Metro Bank were stale on the Account Map; the Competitors page understated Anthropic Global Premier partners (HCLTech from 12 October 2026). All corrected on the pages.
- The study page is removed from the build and the repository and lives in `private/`, which git ignores. The repository is public, so the page remains in git history; making the repository private would complete the fix.
- The index is rebuilt as a brief: situation, argument, strategy, plan, vision, pages.
- Six meeting pages (M1 to M6) carry the case on screen; the fourteen analysis pages are now the Appendix group. Navigation shows Meeting and Appendix dropdowns.
- Open points: the £10m fee claim is worded two ways across appendix pages (pitches led against studio-owned pursuits); candidate claims beyond the CV facts on A1 The Role (Citigroup, £5m+ as Associate, Rafael Viñoly technology group, COP Week panels) should be checked against the CV; a personal "why Wipro", one lost-deal story and the pharma contract figures are still to write.
