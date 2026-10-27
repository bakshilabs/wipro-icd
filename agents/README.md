# Agents

Each file records one Claude Code subagent used to build this site: its job, inputs, outputs, run statistics and the instructions it was given (lightly condensed; the shared briefs are verbatim). The front matter follows the `.claude/agents/*.md` format, so a file can be copied into `.claude/agents/` and reused.

Shared briefs: `page-brief.md` (every page agent), `review-brief.md` (every reviewer), `strategy-brief.md` (the second-round strategy agents) and `meeting-brief.md` (the meeting-page agents).

Stages:
1. Research: `research-wipro`, `research-uki-market`, `research-competitors`, `research-deals`.
2. Pages: `page-portfolio-demand`, `page-buyers-accounts`, `page-competitors-deals`, `page-pursuits-workshops-ai`, `page-role-months-about`, `page-index`, `page-method`.
3. Review: `review-1`, `review-2`, `review-3`.

Second round:
1. Research: `research-bfs-europe`, `research-wipro-sales`, `research-sales-scope`, `research-account-map`, `research-new-logos`.
2. Pages: `page-banking`, `page-banking-edits`, `page-strategy-index-role`, `page-strategy-commercial`, `page-strategy-plan`, `page-account-map`, `page-new-logos`.

Third round (review came first):
1. Review: `review-wipro`, `review-market`, `review-accounts`, `review-pages`. Independent fact-checks of the research files and the pages against primary sources.
2. Pages: `fix-chaps`, `fix-accounts` (corrections to the appendix pages), `page-meeting-situation-fit`, `page-meeting-strategy-banking`, `page-meeting-plan-vision` (the six meeting pages M1 to M6, written to `meeting-brief.md`).

Run statistics are tool calls, tokens and wall-clock time as reported by Claude Code when each agent finished.
