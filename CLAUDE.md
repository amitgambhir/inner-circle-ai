# CLAUDE.md — Inner Circle AI

## What this project is

A file-based multi-agent framework. No code — pure markdown. Five AI agents (Ada, Curie, Tesla, Ogilvy, Nightingale) coordinate through shared files in a hub-and-spoke model with CEO approval governance.

## Critical rules

- **Do not modify file content the user provides verbatim.** Write it exactly as given.
- **One writer per file.** Never have two agents write to the same file. If two agents contribute to the same output, one writes a draft, the other writes feedback in a separate file.
- **All agent output goes through the approval queue** unless covered by standing permissions in `CEO.md`.
- **Never mix project contexts.** Work within one project directory at a time. Research for one project does not belong in another.

## Project structure

- Root-level `.md` files (`AGENTS.md`, `CEO.md`, `PROJECTS.md`, `HEARTBEAT.md`) are framework-level — shared across all projects
- `agents/{name}/SOUL.md` defines each agent's identity and workflow — keep these under 60 lines of core instructions
- `agents/{name}/MEMORY.md` is curated long-term memory — keep under 100 lines
- `agents/{name}/memory/` holds daily session logs
- `projects/{slug}/` contains all project-specific work with isolated `intel/`, `outbox/`, `approved/`, `escalations/`, and `content/` directories
- `projects/_template/` is the canonical template — copy it to start a new project
- `.gitkeep` files preserve empty directories for git tracking — do not remove them

## File conventions

- Every outbox file must include YAML frontmatter with: `agent`, `type`, `project`, `priority`, `created`, `status`
- Urgent items use filename prefix: `URGENT-{filename}.md`
- Approvals: `{filename}.approved.md` — Feedback: `{filename}.feedback.md`
- Daily memory logs: `agents/{name}/memory/YYYY-MM-DD.md`
- Research briefs: `projects/{slug}/intel/research/YYYY-MM-DD-brief.md`
- CEO briefings: `projects/{slug}/outbox/ada/ceo-briefing-YYYY-MM-DD.md`

## When working as an agent

If you are invoked as one of the five agents (via SOUL.md context), follow the session workflow defined in your SOUL.md exactly. Read `AGENTS.md`, your `SOUL.md`, `CEO.md`, and `PROJECTS.md` at session start. Check your outbox for feedback before producing new work.

## When working as the CEO's assistant

If you are invoked without a SOUL.md (general Claude Code session), you are helping the CEO directly. Do not assume an agent role. Help with framework maintenance, file edits, project setup, or any task the CEO requests.

## Telegram Bot

- The bot lives in `bot/` — Python, using `python-telegram-bot`
- Run with `python3 -m bot.main`
- Config via `.env` (see `.env.example`)
- The bot IS Ada's Telegram interface — it reads/writes the same files the framework uses
- Agent runs are triggered via `claude -p` subprocesses, one per agent
- Tests in `tests/` — run with `python3 -m pytest tests/ -v`
