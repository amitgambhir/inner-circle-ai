# 🤝 Inner Circle AI

**Five AI agents. One team. You're the CEO.**

[![MIT License](https://img.shields.io/badge/license-MIT-00d4aa.svg)](LICENSE)
[![Markdown](https://img.shields.io/badge/stack-pure%20markdown-blue.svg)](#built-on)
[![Agents](https://img.shields.io/badge/agents-5-7c3aed.svg)](#the-team)
[![Works With](https://img.shields.io/badge/works%20with-Claude%20Code%20%7C%20Cursor%20%7C%20Windsurf%20%7C%20Aider-d97706.svg)](#compatible-ai-tools)

---

## Table of Contents

1. [The Problem](#the-problem)
2. [What It Does](#what-it-does)
3. [Demo](#demo)
4. [The Team](#the-team)
5. [Built On](#built-on)
6. [Quickstart](#quickstart)
7. [Architecture](#architecture)
8. [The Governance Model](#the-governance-model)
9. [Use Cases](#use-cases)
10. [Compatible AI Tools](#compatible-ai-tools)
11. [Why This Is Different](#why-this-is-different)

---

## The Problem

AI coding tools are powerful individually, but there's no coordination layer. You can ask Claude to research something, then ask it to write release notes, then ask it to triage issues — but each session starts from scratch. No memory, no delegation, no approval flow.

Solo founders and small teams end up doing the same work they'd delegate to a team of humans: reading issues, writing docs, drafting announcements, tracking metrics. They use AI for one-off tasks but never get the compounding benefits of a team that remembers, specializes, and routes decisions through a single point of contact.

You need a team, not a chatbot.

---

## What It Does

Inner Circle AI is a file-based framework for running 5 specialized AI agents as your leadership team. Each agent has a defined role, personality, memory, and output format. They coordinate through shared files — no APIs, no message queues, no orchestration servers.

```text
Input:  Your AI tool  +  An agent's SOUL.md  +  A project brief
Output: Structured deliverables in your outbox, ready for your approval
```

### Core Dimensions

| Dimension | How It Works |
| --------- | ------------ |
| **Specialization** | 5 agents with distinct roles: research, engineering, growth, operations, coordination |
| **Memory** | File-based memory that persists across sessions — agents get better over time |
| **Governance** | CEO approval queue — nothing ships without your sign-off |
| **Coordination** | Hub-and-spoke model through Ada (Chief of Staff) — you check one briefing, not five |
| **Portability** | Pure markdown — works in any AI tool that reads files |

---

## Demo

A typical CEO briefing from Ada after a day of agent work:

```text
# CEO Briefing — 2026-04-06

## Decisions Needed (3 items)

### 1. [URGENT] Release Notes v0.2.0 — from Ogilvy
Bottom line: Draft ready for the SOUL.md restructuring release.
Ada's recommendation: Approve — clear, user-focused, matches our voice.
File: outbox/ogilvy/release-notes-v0.2.0.md

### 2. Issue Triage Report — from Tesla
Bottom line: 4 new issues, 2 bugs (P1), 1 feature request (P2), 1 question.
Ada's recommendation: Approve triage. Assign bugs to Tesla for next session.
File: outbox/tesla/triage-2026-04-06.md

### 3. Ecosystem Brief — from Curie
Bottom line: CrewAI shipped v0.5 with memory support. Relevant to our positioning.
Ada's recommendation: Approve brief. Flag for Ogilvy to draft a comparison post.
File: outbox/curie/ecosystem-update-2026-04-06.md

## Status Update
- Curie: Delivered daily intel brief. Tracking 6 ecosystem frameworks.
- Tesla: Reviewed 2 PRs, triaged 4 issues.
- Ogilvy: Drafted release notes for v0.2.0.
- Nightingale: Updated GETTING-STARTED.md with new session workflow.
```

Your response: *"Approve 1 and 2. On 3 — have Ogilvy draft the comparison post this week."*

That's it. Under 2 minutes.

---

## The Team

| Agent | Named After | Role | Job |
| ----- | ---------- | ---- | --- |
| **Ada** | Ada Lovelace | Chief of Staff | Coordinate the team, brief the CEO, route all decisions |
| **Curie** | Marie Curie | Head of Research | Gather intelligence, analyze signals, deliver structured briefs |
| **Tesla** | Nikola Tesla | Head of Engineering | Triage issues, review PRs, write specs, technical decisions |
| **Ogilvy** | David Ogilvy | Head of Growth | Release notes, community updates, social content, announcements |
| **Nightingale** | Florence Nightingale | Head of Operations | Documentation, metrics, contributor experience, process improvement |

---

## Built On

| Component | Why |
| --------- | --- |
| **Markdown files** | Every AI tool reads them natively — zero vendor lock-in |
| **Git** | State management, version control, and collaboration built in |
| **SOUL.md** | One file per agent defines identity, principles, workflow, and stop condition |
| **File-based coordination** | Agents read and write to shared directories — no APIs, no queues, no servers |

No programming language. No dependencies. No build step.

---

## Quickstart

```bash
git clone https://github.com/amitgambhir/inner-circle-ai.git
cd inner-circle-ai
```

Fill in your preferences in `CEO.md`, then start your first agent session:

```bash
# In Claude Code, Cursor, Windsurf, or any AI tool:
# Point it at Curie's SOUL.md and the project context

"Read agents/curie/SOUL.md, AGENTS.md, CEO.md, and PROJECTS.md.
You are Curie, Head of Research. Your active project is inner-circle-mgmt.
Start by reading projects/inner-circle-mgmt/PROJECT.md,
then run your session workflow as defined in your SOUL.md."
```

Check Curie's output:

```bash
ls projects/inner-circle-mgmt/intel/research/    # her research brief
ls projects/inner-circle-mgmt/outbox/curie/       # anything needing your approval
ls agents/curie/memory/                            # her session log
```

---

## Architecture

```text
                         ┌─────────────────────────────────────────┐
                         │           CEO (You)                     │
                         │   Reads Ada's briefing, makes decisions │
                         └──────────────┬──────────────────────────┘
                                        │
                                        ▼
                         ┌──────────────────────────────┐
                         │     Ada (Chief of Staff)     │
                         │  Consolidates → Briefs CEO   │
                         │  Routes decisions → Agents   │
                         └──┬───────┬───────┬───────┬───┘
                            │       │       │       │
                   ┌────────┘   ┌───┘    ┌──┘      ┌┘
                   ▼            ▼        ▼         ▼
              ┌─────────-┐ ┌────────┐ ┌───────┐ ┌─────────────┐
              │  Curie   │ │ Tesla  │ │Ogilvy │ │ Nightingale │
              │ Research │ │ Engin. │ │Growth │ │ Operations  │
              └────┬─────┘ └───┬────┘ └───┬───┘ └──────┬──────┘
                   │           │          │             │
                   ▼           ▼          ▼             ▼
              intel/       intel/     outbox/       outbox/
              research/    architecture/ ogilvy/    nightingale/

File flow:
  Curie writes intel    → Everyone reads
  Tesla writes specs    → Nightingale + Ogilvy read
  All agents            → write to outbox/ → Ada consolidates → CEO decides
```

For the full architecture — dependency graphs, file flow diagrams, agent identity summaries, memory system, and the Telegram bot internals — see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## The Governance Model

Nothing ships without your approval. The flow is simple:

1. **Agent produces output** → writes to `outbox/{agent}/`
2. **Ada consolidates** → writes a single CEO briefing with recommendations
3. **You review** → approve, give feedback, or reject each item
4. **Ada routes decisions** → agents pick up approvals/feedback next session

**Standing permissions** let trusted agents skip the queue for low-risk tasks (e.g., fixing typos in approved docs). Define these in `CEO.md`. Start tight, loosen over time.

**Escalations** fire if items sit unanswered for 48+ hours (24 for urgent). This should almost never happen — Ada flags staleness before it hits the threshold.

See [docs/GOVERNANCE.md](docs/GOVERNANCE.md) for the full model.

---

## Use Cases

The framework ships with **open source repo management** as the starter (this repo manages itself). Four additional templates are included in [docs/USE-CASES.md](docs/USE-CASES.md):

| Use Case | Primary Agents | Cadence |
| -------- | ------------- | ------- |
| **Content engine for a SaaS blog** | Curie + Ogilvy | Daily |
| **Launch week playbook** | All five, full throttle | Sprint (bounded) |
| **Weekly ecosystem intelligence** | Curie + Ada | Weekly |
| **Customer feedback → product pipeline** | Nightingale + Curie + Tesla | Weekly |

To start your own: copy `projects/_template/`, fill in `PROJECT.md`, set priority in `PROJECTS.md`.

---

## Telegram Bot — Ada as a Chat Interface

The framework includes a Telegram bot that IS Ada. One conversation, one contact. You trigger agent runs, receive briefings, and make decisions — all from your phone.

```text
You:  "run the team"
Ada:  "Running agents for inner-circle-mgmt..."
Ada:  "✓ Curie complete"
Ada:  "✓ Tesla complete"
Ada:  "✓ Ogilvy complete"
Ada:  "✓ Nightingale complete"
Ada:  "✓ Ada complete — briefing ready"
Ada:  [Briefing with Approve/Reject/Feedback buttons per item]

You:  [taps Approve on item 1]
Ada:  "Item 1 approved. Routing to Ogilvy."

You:  "what did Curie find on CrewAI?"
Ada:  [reads Curie's intel, responds]
```

**How it works:**

- CEO sends "run the team" (or "run curie", "run tesla ada", etc.)
- Bot spawns `claude -p` sessions sequentially, one per agent, each with isolated context
- Each agent gets only the tools it needs (per-agent permissions — see below)
- After all agents finish, Ada's briefing arrives with inline buttons
- CEO taps Approve/Reject/Feedback — bot writes the files immediately
- Free-text messages go through Ada for follow-ups, priority changes, or ad-hoc requests

**Per-agent tool permissions:**

| Agent | File Access | Git | GitHub CLI | Web |
| ----- | ----------- | --- | ---------- | --- |
| Curie | Read/Write/Edit | Read | Issues, PRs, API | Search, Fetch |
| Tesla | Read/Write/Edit | Read + Write | Issues, PRs, API | No |
| Ogilvy | Read/Write/Edit | Read | No | Search, Fetch |
| Nightingale | Read/Write/Edit | Read | No | Search, Fetch |
| Ada | Read/Write/Edit | Read + Write | No | No |

**Setup:**

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Telegram bot token and chat ID
python3 -m bot.main
```

---

## Compatible AI Tools

| Tool | How to Load Agents |
| ---- | ------------------ |
| **Telegram Bot** | Built-in — send "run the team" and Ada handles everything |
| **Claude Code** | Load SOUL.md as context at session start |
| **Cursor** | Add SOUL.md as project rules |
| **Windsurf** | Use rules files (natively supported) |
| **Cline / Roo Code** | Pass SOUL.md as system context |
| **Aider** | Include SOUL.md in chat context |
| **OpenClaw** | Built-in cron scheduling + Telegram integration |

If your tool can read a file and follow instructions, it can run these agents.

---

## Why This Is Different

- **No code, no infrastructure.** Pure markdown files in a git repo. The only code is the optional Telegram bot — and that's just a convenience wrapper around the file layer.
- **You stay in control.** Every other multi-agent framework optimizes for autonomy. This one optimizes for CEO oversight with a 2-minute daily review.
- **Tool-agnostic.** Switch from Claude Code to Cursor to Aider — the agents don't care. SOUL.md works everywhere.

---

## Extensibility

The framework is designed to be forked and adapted, not used as-is. Every layer is a seam you can extend.

**Add agents.** Copy any agent directory, write a new SOUL.md, add a row to AGENTS.md. The hub-and-spoke model through Ada means new agents plug in without rewiring anything — they just write to their outbox and Ada picks it up.

**Add projects.** Copy `projects/_template/`, fill in PROJECT.md. Each project is fully isolated with its own intel, outbox, and escalation directories. Agents work across multiple projects by checking PROJECTS.md for priorities.

**Add use cases.** The five agent roles (research, engineering, growth, operations, coordination) map to most business functions. Swap the domain context in SOUL.md files and the agent behavior follows — the LLM already understands roles like "Head of Research" from training data. See [docs/USE-CASES.md](docs/USE-CASES.md) for four ready-made templates.

**Swap the communication layer.** The Telegram bot is one interface. The file layer underneath is the real system. Build a Slack bot, a Discord bot, a web dashboard, or a CLI wrapper — anything that reads `outbox/ada/` and writes approval files works.

**Swap the AI tool.** SOUL.md files are plain markdown. Any tool that reads files and follows instructions can run these agents. Move from Claude Code to Cursor mid-project and nothing breaks.

**Customize governance.** Start with the approval queue as-is, then loosen it. Grant standing permissions in CEO.md for trusted actions. Adjust escalation thresholds. The governance model is a dial, not a switch.

---

## Contributing

Contributions are welcome. This is an MIT-licensed open-source project.

**Good first contributions:**

- New use case templates in `docs/USE-CASES.md`
- Improvements to SOUL.md files (better prompts, clearer stop conditions)
- Bug fixes in the Telegram bot (`bot/`)
- Documentation improvements

**How to contribute:**

1. Fork the repo
2. Create a branch (`git checkout -b feature/your-idea`)
3. Make your changes
4. Run tests (`python3 -m pytest tests/ -v`)
5. Submit a PR with a clear description of what changed and why

**Guidelines:**

- Keep SOUL.md files under 60 lines of core instructions. Complexity goes in PROJECT.md or `intel/`, not in the agent identity.
- One writer per file. If your change introduces a new file, make clear which agent owns it.
- The approval queue is the governance backbone. Changes that bypass or weaken it need strong justification.
- Test your changes. The bot has 47 tests — don't break them, and add tests for new behavior.

**What we're looking for:**

- Real-world use case reports — what worked, what didn't, what you changed
- Agent prompt improvements backed by actual session output
- Integration with other AI tools (Cursor rules, Windsurf rules, Aider configs)
- Alternative communication layers (Slack, Discord, web UI)

---

## License

MIT — use it however you want.

---

*I built this because I wanted a team that works while I sleep — but only ships what I approve.*
