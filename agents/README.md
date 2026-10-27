# Agents

Each file records one Claude Code subagent used to build this site: its job, inputs, outputs, run statistics and the instructions it was given (lightly condensed; the shared briefs are verbatim). The front matter follows the `.claude/agents/*.md` format, so a file can be copied into `.claude/agents/` and reused.

Shared briefs: `page-brief.md` (every page agent) and `review-brief.md` (every reviewer).

Stages:
1. Research: `research-wipro`, `research-uki-market`, `research-competitors`, `research-deals`.
2. Pages: `page-portfolio-demand`, `page-buyers-accounts`, `page-competitors-deals`, `page-pursuits-workshops-ai`, `page-role-months-about`, `page-index`, `page-method`.
3. Review: `review-1`, `review-2`, `review-3`.

Run statistics are tool calls, tokens and wall-clock time as reported by Claude Code when each agent finished.
