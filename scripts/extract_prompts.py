#!/usr/bin/env python3
"""
Extract user prompts from Claude Code sessions for a given date.

Usage: python3 extract_prompts.py YYYY-MM-DD [--projects-dir PATH]

Output: JSON with all user prompts grouped by project.

This is a standalone extractor. If you also use the session-to-ppp skill,
you can optionally import from its extract module for richer session data.
"""
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

JST = timezone(timedelta(hours=9))


def session_jst_date(first_ts: str) -> str | None:
    """Return the JST date string (YYYY-MM-DD) of a timestamp."""
    if not first_ts:
        return None
    try:
        dt = datetime.fromisoformat(first_ts.replace('Z', '+00:00'))
        return dt.astimezone(JST).strftime('%Y-%m-%d')
    except Exception:
        return None


def extract_prompts_from_file(filepath: str, min_length: int = 30) -> list[dict]:
    """Extract user messages from a JSONL session file."""
    size = os.path.getsize(filepath)
    prompts = []
    first_ts = None

    try:
        with open(filepath, 'r', errors='replace') as f:
            if size > 5_000_000:
                lines = f.readlines()
                lines = lines[:50] + lines[-50:]
            elif size > 1_000_000:
                lines = f.readlines()
                lines = lines[:100] + lines[-100:]
            else:
                lines = f.readlines()
    except Exception:
        return []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue

        timestamp = obj.get('timestamp', '')
        if timestamp and first_ts is None:
            first_ts = timestamp

        msg_type = obj.get('type', '')

        if msg_type == 'user':
            content = obj.get('message', {}).get('content', '')
            texts = []
            if isinstance(content, str) and content.strip():
                texts.append(content[:1000])
            elif isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get('type') == 'text':
                        texts.append(item['text'][:1000])

            for text in texts:
                if len(text.strip()) < min_length:
                    continue
                if any(text.startswith(p) for p in
                       ['<system-', '<command-', '[cockpit]', '<local-']):
                    continue
                prompts.append({
                    'text': text,
                    'first_ts': first_ts or '',
                })

    return prompts


def normalize_project(dirname: str) -> str:
    """Directory name → human-readable project name."""
    name = dirname.strip('-')
    prefixes = [
        'Users-',
    ]
    for prefix in prefixes:
        if name.startswith(prefix):
            parts = name.split('-')
            # Skip user directory segments, keep project name
            if len(parts) > 3:
                return '-'.join(parts[-3:])
            return '-'.join(parts[-2:]) if len(parts) > 1 else name
    return name or dirname


def find_sessions(target_date: str, projects_dir: str) -> dict:
    """Find all JSONL sessions that started on target_date (JST)."""
    projects_dir = os.path.expanduser(projects_dir)
    results = {}

    if not os.path.isdir(projects_dir):
        return results

    target_dt = datetime.strptime(target_date, '%Y-%m-%d')
    mtime_start = (target_dt - timedelta(days=1)).strftime('%Y-%m-%d')
    mtime_end = (target_dt + timedelta(days=1)).strftime('%Y-%m-%d')

    for root, dirs, files in os.walk(projects_dir):
        depth = root.replace(projects_dir, '').count(os.sep)
        if depth > 4:
            dirs.clear()
            continue

        for fname in files:
            if not fname.endswith('.jsonl'):
                continue
            if 'subagents' in root:
                continue

            fpath = os.path.join(root, fname)

            try:
                mtime = datetime.fromtimestamp(os.path.getmtime(fpath))
                mod_date = mtime.strftime('%Y-%m-%d')
            except Exception:
                continue

            if mod_date < mtime_start or mod_date > mtime_end:
                continue

            rel = os.path.relpath(fpath, projects_dir)
            project_dir = rel.split(os.sep)[0]
            project_name = normalize_project(project_dir)

            prompts = extract_prompts_from_file(fpath)
            if not prompts:
                continue

            # Check first_ts matches target_date
            jst_date = session_jst_date(prompts[0].get('first_ts', ''))
            if jst_date != target_date:
                continue

            if project_name not in results:
                results[project_name] = []

            for p in prompts:
                p['project'] = project_name
                p['source'] = 'claude'
                results[project_name].append(p)

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: extract_prompts.py YYYY-MM-DD [--projects-dir PATH]",
              file=sys.stderr)
        sys.exit(1)

    target_date = sys.argv[1]
    projects_dir = '~/.claude/projects'

    if '--projects-dir' in sys.argv:
        idx = sys.argv.index('--projects-dir')
        projects_dir = sys.argv[idx + 1]

    results = find_sessions(target_date, projects_dir)

    all_prompts = []
    for prompts in results.values():
        all_prompts.extend(prompts)

    output = {
        'target_date': target_date,
        'total_prompts': len(all_prompts),
        'total_projects': len(results),
        'prompts': all_prompts,
    }
    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
