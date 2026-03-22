# Gotchas

## Analysis

- **Distinguish delegated prompts** — If you use an AI orchestrator (e.g., AGI Cockpit, Claude Desktop Projects) that delegates to sub-agents, the orchestrator may auto-generate high-quality prompts. Don't mistake these for the user's own prompts. User-written prompts tend to be more casual regardless of tool
- **Skip command invocations** — `/session-to-ppp`, `/finance-report`, etc. are boilerplate skill calls, not analysis targets
- **Multi-turn context matters** — A single prompt in isolation is often meaningless. The pattern "fix this" → "no, not that" → "I mean this" is the richest signal
- **Mixed-language prompts** — If the user mixes languages (e.g., Japanese + English), pay attention to how technical English terms are used — vocabulary gaps show up there

## Output

- **Append to existing journal** — Don't create separate files. Add a `## Prompt Mirror` section to the existing `YYYY-MM-DD.md` journal entry
- **One topic per day, strictly** — Even if you find multiple candidates, pick only the highest-impact one. More than one won't get read
- **Always update taught.jsonl** — Never teach the same topic twice. Record every lesson in `data/taught.jsonl`

## Concept Detection Criteria

- **"Would knowing this concept have prevented the problem?" test** — If yes, it's worth teaching. If no, it's just a prompt-writing tip, not a concept lesson
- **Skip concepts that can't be explained with a daily-life example** — If you can't find an everyday analogy, the concept is too abstract to teach right now. Wait for a concrete example to appear
- **Check engineer_term against taught.jsonl** — Don't re-teach the same technical term. But related concepts are OK (e.g., after teaching mtime, teaching created_at vs last_accessed is fine)
- **Increase concept depth over time** — Start with basics like "stateless vs stateful". As the log grows, progress to "event-driven vs polling". Use taught.jsonl entry count as a guide

## Edge Cases

- **"Nothing found" is a valid answer** — Don't force a lesson. "No lesson today" is fine
- **High-quality prompt days = fewer lessons** — That's actually a good sign. Track whether "no lesson" days increase over time
- **Fallback to prompt improvement tips** — If no concept gap is found, you can optionally offer a prompt-writing tip instead (e.g., "avoid implicit references")
