# Brief for the meeting pages

Project: /home/user/wipro-icd, a static site Arpan Bakshi will show on screen in a second interview with the IC&D Europe Sales Head at Wipro (Industry Cloud & Digital, UK and Ireland), then share with Wipro. Today is 27 October 2026. Job description: job-description.txt.

The site now has three layers. `overview.html` is the index, written as a brief in six sections: Situation, Argument, Strategy, Plan, Vision, Pages. Six new **meeting pages** (M1 to M6) expand those sections for the screen. The fourteen existing **analysis pages** (A1 to A14) become the Appendix, where every detail, model and source already lives.

## Read first
- build/STYLE.md: every writing rule applies. Never show gaps or weaknesses. No em dashes. No "not X but Y" or "rather than". No closing summary lines. Plain-noun headings. First person (I). British spelling. Judgement labelled "my estimate" or "my judgement". Placeholders labelled.
- build/pages/overview.html: the content source and the tone. The meeting pages say the same things, with fewer words and bigger visuals. Do not contradict it.
- agents/page-brief.md, section "Visual standard" and "File format": the components, chart helpers (window.VZ), CSS tokens and file format. The reference appendix pages are in build/pages/ (read two or three: role.html, banking.html, first-months.html).

## What a meeting page is
A page shown on a 1440 px screen in a conversation, and readable later on a phone. Rules:
- Three to five screens long at 1440 by 900. Each screen carries one idea: a heading, at most 60 words of prose, and one visual.
- The visual carries the point. Charts, diagrams, timelines, matrices and simple interactive controls built with VZ. Every chart has a one-sentence plain reading under its title. Nothing important depends on hovering.
- Type is larger than on the appendix pages: the lede at 20 to 22 px, body at 17 px, numbers at 40 px or more.
- No tables longer than four rows. No bullet lists longer than four items. No Sources panel; instead end with one short `<p class="mini">` line naming the appendix pages that hold the detail and sources, as links (for example "Detail and sources: A8 Account Map, A13 Banking Pursuit.").
- Keep the page-specific CSS in a `<style>` block at the top with a short prefix (`m1-`, `m2-` and so on), and JS in one `<script>` at the end. Colour roles only: var(--accent) for Move 1, var(--s2) for Move 2, var(--ink1..3), var(--s1..s8), never raw hex.
- Start the file with `<!--meta title="<Title>" desc="<one sentence>"-->`. The first `<section class="phead">` holds `<span class="eyebrow">` (the build inserts the page code), an h1, a lede and a meta line, as on the appendix pages.

## Facts
Use only facts that appear on overview.html or the appendix pages, with these corrections already applied on overview.html and to be applied everywhere:
- Clients above US$100m: 22 (FY24), 17 (FY25), 16 (FY26), 18 (Q2 FY27).
- Europe Q2 FY27: +5.1% year on year and +0.6% quarter on quarter in constant currency, 27.4% of IT services revenue, "broad-based growth led by BFSI, Consumer, and EMR" (CFO). Never "led by BFSI" alone.
- Q2 FY27: IT services operating margin 16.5%; bookings US$2,595m; large deals US$674m from nine deals; large deal means TCV of US$30m or more. Peers: TCS 24.0%, Infosys 21.0%, HCLTech 18.2%.
- 98.0% of Q2 FY27 revenue from existing clients; 33 new clients in the quarter, 216 in FY26.
- CFO Aparna Iyer, 17 January 2025: "hunting remains a very, very key lever for us."
- Lloyds Banking Group: a relationship of more than fifteen years (Wipro's own page says 15 years; a Wipro speaker at PegaWorld 2025 said "18 plus years" and 2,500 Wipro staff); two TESTA 2023 awards in Lloyds' name including the Payment Services Platform.
- Phoenix (now Standard Life plc): £500m over ten years, announced 26 March 2025.
- CHAPS: the November 2026 address rule was deferred by the Bank of England on 27 August 2026 with no new date. Purpose codes on all CHAPS payments from November 2027 still stand. Never show a November 2026 CHAPS date.
- FCA PS26/2 incident and third-party reporting applies 18 March 2027. Operational resilience transition ended 31 March 2025. DORA applied 17 January 2025. HM Treasury designated Google Cloud, Microsoft, AWS and Oracle UK as Critical Third Parties from 13 July 2026.
- 20 October 2026: Google Cloud europe-west2 failure disrupted several UK banks; the Treasury Committee wrote to the Bank of England and FCA the same day; replies due 4 November 2026 and 20 January 2027.
- Mergers: Santander completed TSB 30 April 2026; Virgin Money into Nationwide 2 April 2026; Coventry Building Society and The Co-operative Bank transfer 1 January 2027.
- Energy: half-hourly settlement migration complete by 7 May 2027. PSTN switch-off 31 January 2027. G-Cloud 15 from 6 August 2026, Wipro listed. Government Commercial Agency replaced CCS 1 April 2026.
- Alliances: Claude Applied AI Centre of Excellence 16 June 2026, 10,000 certified in 18 months; Google Cloud 27 August 2026, Gemini Enterprise as orchestration platform, LIFT, 1,500 forward deployed engineers; Microsoft 12 December 2025; Tricentis Global Platinum, 3,000+ Tosca specialists, Tricentis UK Partner of the Year 2023; AWS Collaboration Partner of the Year 2025 (North America); Wipro is listed on G-Cloud 15. Do not claim Anthropic Global Premier status for Wipro. Do not say "Google Cloud global partner of the year".
- Loopio 2026: average RFP win rate 39% in 2025, UK 47%.
- Do not present RSA, Metro Bank or Allied Irish Banks as expansion plays.
- Arpan's record (only these facts): WSP, more than $2m a year from outreach, pitches and bids; SOM New York, led business development for his department, more than $3m a year, presentations to Wall Street bank executives; Foster + Partners Associate Partner (2015 to July 2026), co-created and launched a strategic advisory service line (corporate environmental strategy, digital transformation, spatial consulting), led pitches, bids and competition entries behind more than £10m a year in fees, presentations to Fortune 500 chief executives, a multi-year contract with a global pharmaceutical company that he pitched, negotiated and signed, clients Roche, Genentech, Alibaba, Apple, Oracle, Hyundai, JPMorgan Chase (design clients); Atlas Learn co-founder from October 2025, trains executive teams on Claude, Gemini and Copilot, 250+ senior professionals trained including a FinTech board and a client chief executive with heads of HR, marketing and IT, runs sales, marketing and commercial operations; Anthropic credentials (AI Fluency, Claude Code in Action, Claude Cowork, Claude Platform), Microsoft Copilot Studio; Python and C#; eighteen years of client work in New York and London. Do not add claims beyond these.

## Check your work
1. `cd /home/user/wipro-icd && python3 build/build.py` (others build at the same time; if your page 404s, rebuild and retry).
2. A server runs on port 8765 from docs/ (if not: `cd docs && python3 -m http.server 8765 &`). Run `cd /home/user/wipro-icd && NODE_PATH=$(npm root -g) node tools/shoot.js <your scratch dir> <file>.html`: it screenshots at 1440 light and 390 dark and prints scrollX and console errors. Fix until scrollX=0 and errors=0. Read the screenshots (crop them with PIL if they are too tall to read) and fix overlaps, unreadable labels, empty charts and dark-mode contrast.
3. Grep your page for "—", " not ", "rather than", "gap", "Nov 2026", "November 2026" and the banned words in STYLE.md, and fix.
4. Reply with: pages written, the visuals on each, screen count at 1440, and anything you could not support.
