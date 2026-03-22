---
name: prompt-mirror
description: Analyze yesterday's prompts to surface one technical concept worth understanding, delivered as a concise morning lesson with everyday analogy + engineer vocabulary. Use when "morning lesson", "prompt mirror", "today's learning", "what should I learn", or via scheduled automation each morning.
user_invocable: true
---

# Prompt Mirror — Concept Lens

Your prompts are a mirror. They reveal which technical concepts you understand intuitively and which ones have gaps. This skill reads yesterday's session prompts, identifies **one** concept worth understanding, and delivers it as a morning lesson: everyday analogy first, engineer vocabulary second.

## Goal

**Talk like an engineer — without writing code.** You don't read or write code, but you understand concepts, judge AI output quality, and participate in technical conversations with confidence.

## How it works

1. **Extract** — Run `scripts/extract_prompts.py YYYY-MM-DD` to collect all user prompts from yesterday's sessions
2. **Analyze** — Read the extracted prompts and identify **concept gaps**:
   - Technical terms used inaccurately
   - Related but distinct concepts being confused
   - Moments where AI output quality couldn't be judged (or was caught)
   - Concepts that engineers would use in conversation, used implicitly
3. **Select one** — Pick the highest-impact concept. Check `data/taught.jsonl` to avoid repeats
4. **Deliver** — Write a concise lesson to the Journal using the template in `templates/lesson.md`

## Analysis Guidelines — Concept Lens

- **Hunt for concept gaps, not code mistakes** — Not "you should use first_ts" but "file modification date and session start date are different concepts"
- **Start with everyday examples** — Like: "The 'last edited' date on a Google Doc is not the same as when it was created" — analogies anyone can grasp
- **Add engineer vocabulary** — After the analogy, one line: "Engineers call this mtime vs created_at"
- **Anchor to yesterday's experience** — Not abstract explanations, but "this happened in your session yesterday, and knowing this concept would have prevented it"
- **Distinguish delegated prompts** — See gotchas.md. Prompts sent via orchestrators (e.g., AGI Cockpit) to sub-agents may be AI-generated, not human-written
- **Don't force it** — If nothing surfaces, "No lesson today" is a valid output

## What NOT to Teach

- How to write or read code (the user doesn't code)
- Tool-specific command syntax (that's what docs are for)
- Things already corrected within the session
- Typos or language slips

## Config

Read `config.json` in this skill directory. If missing, use defaults:
- Journal dir: `~/Documents/Journal/` (or configure your own path)
- Projects dir: `~/.claude/projects`
- Codex dir: `~/.codex`

## Gotchas

See `gotchas.md` — failure patterns discovered in practice. Read every run.

## Memory

After delivering a lesson, append to `data/taught.jsonl`:

```jsonl
{"date":"YYYY-MM-DD","topic":"one-line topic","category":"concept|vocabulary|mental-model","engineer_term":"the technical term taught","prompt_examples":["truncated example"]}
```

On each run, read this log to:
- Avoid teaching the same topic twice
- Track which categories are most frequent
- Spot progression (are the concepts getting more advanced over time?)

## Jaggedness Map

Inspired by Andrej Karpathy's observation that AI models are "simultaneously a brilliant PhD student and a 10-year-old" — humans have the same jaggedness in their prompt capabilities. This feature builds a personal strength/weakness map over time.

### How it works

After 7+ entries in `data/taught.jsonl`, generate or update `data/jaggedness-map.json`:

```json
{
  "updated": "YYYY-MM-DD",
  "total_lessons": 12,
  "strong": [
    {"area": "Architecture delegation", "evidence": "Consistently clear system design prompts"},
    {"area": "Requirements definition", "evidence": "Scope and constraints well-specified"}
  ],
  "weak": [
    {"area": "Implicit references", "evidence": "3 lessons on ambiguity patterns"},
    {"area": "Data pipeline concepts", "evidence": "Confused event time vs processing time, precision vs recall"}
  ],
  "improving": [
    {"area": "Security awareness", "evidence": "Secrets management lesson led to behavior change"}
  ],
  "no_lesson_days": 6,
  "no_lesson_trend": "increasing — prompt quality improving"
}
```

### When to generate

- **Weekly**: After 7+ taught.jsonl entries, append a `## Prompt Mirror — Jaggedness Map` section to the weekly journal entry
- **On demand**: When the user asks "show my prompt map" or "jaggedness map"

### Analysis sources

1. `data/taught.jsonl` — What concepts were taught (= weak areas that needed teaching)
2. Prompt extraction — What areas the user prompts confidently in (= strong areas)
3. "No lesson" days — Increasing trend = overall improvement

### Map rules

- **Strong** = areas where prompts are consistently clear, specific, and technically accurate. No lessons needed
- **Weak** = areas where multiple lessons clustered. 2+ lessons in same domain = pattern
- **Improving** = areas where a lesson was taught AND subsequent prompts show the concept being applied correctly
- Don't fabricate strengths. Only mark "strong" if there's positive evidence from prompt patterns
