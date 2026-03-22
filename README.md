# Prompt Mirror

![banner](banner.png)

**Your prompts are a mirror.** They reveal which technical concepts you understand intuitively — and which ones have gaps.

Prompt Mirror is a [Claude Code Skill](https://docs.anthropic.com/en/docs/claude-code/skills) that reads your previous day's session prompts, identifies one concept gap, and delivers a morning lesson: everyday analogy first, engineer vocabulary second.

Built for non-engineers who work with AI daily — founders, PMs, designers, operators — anyone who wants to speak the same language as their engineering team without writing a single line of code.

## What It Does

Every morning, Prompt Mirror:

1. **Extracts** your prompts from the previous day's Claude Code sessions
2. **Analyzes** them for concept gaps — technical terms used inaccurately, related concepts confused, or moments where you couldn't judge AI output quality
3. **Selects** the single highest-impact concept (never more than one)
4. **Delivers** a lesson to your journal: what happened → everyday analogy → engineer term → why it matters → action item

## Example Output

> ### Settings vs Secrets Are Not the Same Thing
>
> **What happened yesterday:**
> You pasted a CLIENT_ID and CLIENT_SECRET directly into a prompt for X API auth. These values are now permanently stored in plaintext in your session logs.
>
> **In everyday terms:**
> Your home address is fine to share. But writing your door key's PIN on a note taped to your mailbox lets anyone walk in. Settings have "OK to see" and "dangerous to see" categories too.
>
> **Engineers call this:**
> Secrets management. CLIENT_ID is semi-public (like an address), CLIENT_SECRET is a secret (like a key). Engineers store secrets in Keychain, Vault, or .env files (gitignored) — never in logs or chat history.
>
> **Why it's worth knowing:**
> AI agent prompts are automatically recorded to JSONL. If you hardcode secrets, anyone with access to that file can see your API credentials. Especially important for skills that run daily via automation.
>
> **Action for tomorrow:**
> Don't write API secrets directly in prompts. Instead say "use the value from .env" — point to where the value lives, don't paste the value itself.

## Installation

```bash
claude install-skill KaishuShito/prompt-mirror
```

## Setup

After installing, edit `config.json` in the skill directory to match your environment:

```json
{
  "journal_dir": "~/Documents/Journal",
  "projects_dir": "~/.claude/projects",
  "codex_dir": "~/.codex",
  "timezone": "Asia/Tokyo",
  "hour_cutoff": 6,
  "max_prompts_per_session": 20,
  "min_prompt_length": 30
}
```

| Field | Description | Default |
|-------|-------------|---------|
| `journal_dir` | Where daily journal markdown files live | `~/Documents/Journal` |
| `projects_dir` | Claude Code session JSONL directory | `~/.claude/projects` |
| `codex_dir` | Codex CLI session directory (optional) | `~/.codex` |
| `timezone` | Your timezone for date boundaries | `Asia/Tokyo` |
| `hour_cutoff` | Before this hour, treat as "yesterday" | `6` |

## Usage

### Manual

In Claude Code, type:

```
/prompt-mirror
```

### Scheduled (Recommended)

This skill is designed to run automatically each morning. Set up a recurring schedule using one of:

**Claude Desktop — Projects (Recommended)**
Add this skill to a Claude Desktop Project and configure a daily prompt schedule. Claude Desktop's built-in scheduling runs Prompt Mirror each morning automatically.

**AGI Cockpit autorun**
```bash
./cockpit autorun create \
  --name "Prompt Mirror" \
  --instruction "prompt-mirror スキルを実行してください" \
  --type cron \
  --expression "0 7 * * *" \
  --directory master
```

**Cron + Claude Code CLI**
```bash
# crontab -e
0 7 * * * cd ~/your-project && claude -p "Run /prompt-mirror"
```

The morning schedule matters — Prompt Mirror reads *yesterday's* prompts, so running it before you start today's work means the lesson is fresh context for the day ahead.

## Skill Architecture

```
prompt-mirror/
├── SKILL.md              # Core skill instructions
├── config.json           # User configuration
├── gotchas.md            # Failure patterns and edge cases
├── scripts/
│   └── extract_prompts.py  # Session JSONL → prompt extraction
├── templates/
│   └── lesson.md         # Lesson output format template
└── data/
    └── taught.jsonl      # Memory: topics already taught (auto-generated)
```

Following the [progressive disclosure pattern](https://x.com/trq212/article/2033949937936085378) from Anthropic's skill design guidelines — `SKILL.md` is the entry point, and Claude reads supporting files (`gotchas.md`, `templates/`) only when needed.

### Key Design Decisions

- **One lesson per day** — More than one won't get read. Quality over quantity
- **Everyday analogy first** — Never lead with technical jargon. The analogy is the hook
- **taught.jsonl as memory** — Prevents repeating topics and tracks concept progression over time
- **Standalone extractor** — `extract_prompts.py` works independently, no external dependencies
- **No code in lessons** — The target user doesn't write code. Concepts only

## Customization

### Language

The skill defaults to the language used in your prompts. Edit `templates/lesson.md` to set a specific output language.

### Journal Format

By default, lessons append to `YYYY-MM-DD.md` files as a `## Prompt Mirror` section. Modify `templates/lesson.md` to match your journal structure.

### Concept Depth

The skill automatically increases concept complexity over time based on `data/taught.jsonl` entry count. Early lessons cover basics (stateless vs stateful); later ones progress to more nuanced topics (event-driven vs polling).

## How It Works Under the Hood

The `scripts/extract_prompts.py` script walks `~/.claude/projects/` JSONL session files, filters by JST date, and extracts user messages while skipping:
- System reminders and command invocations
- Messages shorter than 30 characters
- Sub-agent (delegated) sessions

Claude then analyzes the extracted prompts using the concept lens guidelines in `SKILL.md`, cross-references `data/taught.jsonl` for duplicates, and writes the lesson.

## Credits

Built by [@KaishuShito](https://github.com/KaishuShito) with Claude Code.

Inspired by the skill design patterns from [Lessons from Building Claude Code: How We Use Skills](https://x.com/trq212/article/2033949937936085378).
