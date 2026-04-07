# Architecture Blueprint — Inner Circle AI

> **Repo:** `inner-circle-ai`
> **Tagline:** "Five AI agents. One team. You're the CEO."
> **Primary Use Case:** Open Source Repo Management (self-referential — this repo manages itself)
> **Target Audience:** Open-source community / broad adoption
> **Harness Compatibility:** Any (Claude Code, Cursor, Windsurf, Cline, Aider, OpenClaw, etc.)
> **License:** MIT

---

## 1. Core Philosophy

### 1.1 Files, Not APIs
All coordination happens through the filesystem. Markdown for humans, JSON for machines. No databases, no message queues, no orchestration servers. Git is the state manager.

### 1.2 CEO-First Governance
The human (CEO) has explicit authority over all output. Nothing leaves the system, gets published, merged, or acted upon without passing through an approval queue. Agents propose. The CEO disposes.

### 1.3 Hub-and-Spoke Communication
All communication between the CEO and the agent team flows through Ada (Chief of Staff). The CEO talks to Ada. Ada talks to the team. This simplifies oversight to a single briefing and maps directly to a future chat interface (Telegram/WhatsApp).

### 1.4 One Agent, One Job
Each agent has a single, boring job title and a clear stop condition. Constraints produce better output than flexibility. When an agent finishes its scope, it stops — it doesn't expand into adjacent work.

### 1.5 Start With One
The framework ships with 5 agents, but users should activate one at a time. Week-by-week ramp-up. The README and onboarding guide enforce this.

---

## 2. The Team

| Agent | Named After | Role Title | One-Line Job |
|-------|------------|------------|--------------|
| **Ada** | Ada Lovelace | Chief of Staff | Coordinate the team, brief the CEO, route decisions |
| **Curie** | Marie Curie | Head of Research | Gather intelligence, analyze signals, deliver structured briefs |
| **Tesla** | Nikola Tesla | Head of Engineering | Triage issues, review PRs, write specs, make technical decisions |
| **Ogilvy** | David Ogilvy | Head of Growth | Write release notes, community updates, social content, announcements |
| **Nightingale** | Florence Nightingale | Head of Operations | Maintain docs, track metrics, manage contributor experience |

### 2.1 Dependency Graph

```
Curie (Research)
  ↓ writes intel
  ├──→ Ada (reads intel, synthesizes CEO briefing)
  ├──→ Tesla (reads intel, informs technical decisions)
  ├──→ Ogilvy (reads intel, creates content angles)
  └──→ Nightingale (reads intel, updates docs/processes)

Tesla (Engineering)
  ↓ writes technical specs, PR reviews
  ├──→ Nightingale (reads specs, updates docs)
  └──→ Ogilvy (reads changelogs, writes release notes)

Ogilvy (Growth)
  ↓ writes content drafts
  └──→ Ada (reviews for consistency, routes to CEO)

Nightingale (Operations)
  ↓ writes docs, metrics reports
  └──→ Ada (includes in CEO briefing)

Ada (Chief of Staff)
  ↓ writes CEO briefings, routes decisions
  └──→ CEO (final authority)
```

### 2.2 One Writer, Many Readers Rule

Every file has exactly ONE agent who writes to it. Other agents read it. If two agents need to contribute to the same output, one writes a draft and the other writes feedback in a **separate file**. This prevents conflicts and keeps accountability clear.

---

## 3. CEO Governance Model — The Approval Queue

### 3.1 Hub-and-Spoke Model — Ada as Single Point of Contact

The CEO communicates with the team **through Ada only** (by default). Ada is the single pane of glass.

```
Agents produce output
        ↓
Write to: projects/{slug}/outbox/{agent}/filename.md
        ↓
ADA reads ALL outboxes at session start
        ↓
Ada writes: outbox/ada/ceo-briefing-YYYY-MM-DD.md
  - Consolidated view of everything pending
  - Ada's recommendations (approve / reject / needs-discussion)
  - Prioritized by urgency
        ↓
CEO reads ONLY Ada's briefing
CEO responds to Ada with decisions
        ↓
Ada writes approval/feedback files to each agent's outbox
  - Approval: outbox/{agent}/filename.approved.md
  - Feedback: outbox/{agent}/filename.feedback.md
  - Ada relays CEO feedback VERBATIM — she adds routing context
    but NEVER rephrases the CEO's actual words
        ↓
Agents pick up approvals/feedback next session
```

**Direct access clause:** The CEO reserves the right to talk to any agent directly, bypassing Ada, at any time. Ada does not gatekeep the CEO — she gatekeeps the agents. If the CEO opens Tesla's SOUL.md in a session and works with him directly, that's fine. Ada learns about it next session from the daily logs.

### 3.2 Escalation Path — The Fire Alarm

Ada is the normal path. Escalations are the safety net for when Ada stalls.

```
projects/{slug}/escalations/    ← CEO checks this directly (should usually be empty)
```

**When to escalate:**
- Agent starts a session and finds outbox items **older than 48 hours** with no approval AND no feedback file
- For items tagged `[URGENT]`: escalation threshold is **24 hours**
- These thresholds are configurable in `CEO.md`

**Escalation file format:**
```markdown
---
agent: tesla
stuck-item: outbox/tesla/pr-review-142.md
waiting-since: 2026-04-05
urgency: normal | urgent
---

## What's Stuck
PR #142 review has been in outbox for 3 days with no response.

## Impact If It Keeps Waiting
Contributor has been waiting for merge. Risk of contributor churn.

## Recommended Action
Approve or provide feedback on the PR review.
```

**Escalation rules:**
1. Escalations are for genuine stalls only — not a shortcut to bypass Ada for routine work.
2. Before escalating, the agent MUST verify Ada hasn't already responded (check for .approved.md and .feedback.md files).
3. One escalation per stuck item. Don't re-escalate the same item.
4. Ada should also self-monitor: at each session, she checks if any agent's outbox items are approaching the staleness threshold and proactively flags them in the CEO briefing BEFORE escalation is needed.

### 3.3 Approval Rules

1. **Nothing leaves the outbox without CEO action (routed through Ada).** No agent can self-approve.
2. **Agents check their outbox at session start.** If feedback files exist, address them before producing new work.
3. **Urgency tagging.** Agents can mark items `[URGENT]` in the filename (e.g., `URGENT-security-vuln-report.md`). Ada surfaces these at the top of the CEO briefing.
4. **Bulk approval.** CEO can tell Ada "approve items 1, 3, and 5 from today's briefing." Ada writes the individual approval files.
5. **Standing permissions.** CEO can grant standing permission in `CEO.md` for specific action types (e.g., "Nightingale may update README typos without approval"). This is the **only** way agents skip the queue. Ada tracks which standing permissions exist and does not route those items to the CEO.

### 3.4 Outbox File Format

Every file in the outbox follows this header:

```markdown
---
agent: ogilvy
type: content-draft | technical-spec | briefing | docs-update | metrics-report
project: inner-circle-mgmt
priority: P0 | P1 | P2 | P3
created: YYYY-MM-DD
status: pending-review
---

# [Title]

## Summary
[2-3 sentence executive summary — what this is and why it matters]

## Content
[The actual deliverable]

## Draft Notes
[Agent's notes on choices made, uncertainties, things CEO should pay attention to]
```

### 3.5 Feedback File Format

```markdown
---
from: ceo
re: filename.md
date: YYYY-MM-DD
verdict: revise | approved-with-changes | rejected
---

## Feedback
[Specific, actionable feedback — relayed verbatim by Ada]

## Required Changes
- [ ] Change X to Y
- [ ] Add section on Z
- [ ] Tone is too formal, loosen it up
```

### 3.6 Future: Chat-Based Approval (Roadmap)

The hub-and-spoke model maps directly to a chat interface. A Telegram/WhatsApp bot would:
1. **Be Ada.** The bot IS Ada — one conversation, one contact.
2. Watch `outbox/ada/` for new CEO briefings
3. Send the CEO a summary with approve/reject options per item
4. Write approval/feedback files back to each agent's outbox
5. Watch `escalations/` and send the CEO direct alerts for stalled items

The file-based foundation stays the same. The chat layer is just a convenience wrapper around Ada's existing workflow.

---

## 4. Directory Structure

```
inner-circle-ai/
├── README.md                         # Framework overview, getting started, use cases
├── AGENTS.md                         # Shared operating rules for all agents
├── CEO.md                            # CEO preferences, standing permissions, voice profile
├── CLAUDE.md                         # Project rules for Claude Code sessions
├── PROJECTS.md                       # Project registry & priority dashboard
├── HEARTBEAT.md                      # Self-healing cron monitor
│
├── agents/                           # Agent identities (global, not project-specific)
│   ├── ada/
│   │   ├── SOUL.md                   # Ada's identity, role, principles
│   │   ├── MEMORY.md                 # Ada's curated long-term memory
│   │   └── memory/                   # Ada's daily session logs
│   │       └── YYYY-MM-DD.md
│   ├── curie/
│   │   ├── SOUL.md
│   │   ├── MEMORY.md
│   │   └── memory/
│   ├── tesla/
│   │   ├── SOUL.md
│   │   ├── MEMORY.md
│   │   └── memory/
│   ├── ogilvy/
│   │   ├── SOUL.md
│   │   ├── MEMORY.md
│   │   └── memory/
│   └── nightingale/
│       ├── SOUL.md
│       ├── MEMORY.md
│       └── memory/
│
├── projects/
│   ├── _template/                    # Copy this to start any new project
│   │   ├── PROJECT.md
│   │   ├── intel/
│   │   │   ├── research/
│   │   │   ├── architecture/
│   │   │   └── ops/
│   │   ├── outbox/                   # Agent output → Ada consolidates → CEO decides
│   │   │   ├── ada/
│   │   │   ├── curie/
│   │   │   ├── tesla/
│   │   │   ├── ogilvy/
│   │   │   └── nightingale/
│   │   ├── approved/                 # CEO-approved outputs (routed by Ada)
│   │   ├── feedback/                 # Archived feedback (after revision cycles)
│   │   ├── escalations/             # Direct-to-CEO fire alarm (should be empty)
│   │   ├── content/
│   │   │   ├── releases/
│   │   │   ├── social/
│   │   │   ├── docs/
│   │   │   └── community/
│   │   └── CHANGELOG.md
│   │
│   └── inner-circle-mgmt/           # ← STARTER USE CASE (pre-populated)
│       ├── PROJECT.md
│       ├── intel/
│       │   ├── research/
│       │   ├── architecture/
│       │   └── ops/
│       ├── outbox/
│       │   ├── ada/
│       │   ├── curie/
│       │   ├── tesla/
│       │   ├── ogilvy/
│       │   └── nightingale/
│       ├── approved/
│       ├── feedback/
│       ├── escalations/
│       ├── content/
│       │   ├── releases/
│       │   ├── social/
│       │   ├── docs/
│       │   └── community/
│       └── CHANGELOG.md
│
├── bot/                              # Telegram bot — Ada's chat interface
│   ├── main.py                       # Entry point, polling loop
│   ├── config.py                     # Agent defs, per-agent tool permissions
│   ├── runner.py                     # Spawns claude -p per agent
│   ├── briefing.py                   # Parses Ada's briefing markdown
│   ├── router.py                     # Writes approval/feedback files
│   ├── ada.py                        # Free-text → Ada Claude session
│   ├── projects.py                   # Parses PROJECTS.md for active slugs
│   ├── handlers.py                   # Telegram message/callback routing
│   └── watcher.py                    # Escalation directory scanner
│
├── tests/                            # pytest test suite (47 tests)
│
├── docs/
│   ├── ARCHITECTURE.md               # This file
│   ├── GETTING-STARTED.md
│   ├── USE-CASES.md                  # 4 use case templates
│   ├── GOVERNANCE.md                 # Deep dive on the approval queue
│   ├── CUSTOMIZATION.md              # How to fork and make it yours
├── requirements.txt                  # Python dependencies
└── .env.example                      # Bot config template
```

---

## 5. File Flow — OSS Repo Management Use Case

### 5.1 Daily/Weekly Flow

```
CURIE (Research) — runs first
├── Scans: GitHub issues, PRs, discussions, stars/forks trends,
│          community sentiment, ecosystem framework repos
├── Writes: projects/inner-circle-mgmt/intel/research/YYYY-MM-DD-brief.md
└── Writes: projects/inner-circle-mgmt/intel/research/signal-tracker.json
                ↓
TESLA (Engineering) — runs after Curie
├── Reads: Curie's research brief
├── Triages: open issues (labels, priority, assignment recommendations)
├── Reviews: open PRs (code quality, test coverage, breaking changes)
├── Writes: projects/inner-circle-mgmt/outbox/tesla/issue-triage-YYYY-MM-DD.md
├── Writes: projects/inner-circle-mgmt/outbox/tesla/pr-review-{pr-number}.md
└── Writes: projects/inner-circle-mgmt/intel/architecture/ (specs, ADRs)
                ↓
OGILVY (Growth) — runs after Tesla (needs changelog/release info)
├── Reads: Curie's intel + Tesla's approved changelogs
├── Writes: projects/inner-circle-mgmt/outbox/ogilvy/release-notes-vX.Y.Z.md
├── Writes: projects/inner-circle-mgmt/outbox/ogilvy/community-update-YYYY-MM-DD.md
└── Writes: projects/inner-circle-mgmt/outbox/ogilvy/social-{platform}-YYYY-MM-DD.md
                ↓
NIGHTINGALE (Operations) — runs after Tesla (needs approved specs)
├── Reads: Tesla's approved specs + Curie's contributor data
├── Writes: projects/inner-circle-mgmt/outbox/nightingale/docs-update-{topic}.md
├── Writes: projects/inner-circle-mgmt/outbox/nightingale/contributor-guide-update.md
└── Writes: projects/inner-circle-mgmt/outbox/nightingale/weekly-metrics.md
                ↓
ADA (Chief of Staff) — runs last, reads everything
├── Reads: ALL outbox items from all agents, all intel, all approved items
├── Reads: escalations/ to verify none are pending
├── Writes: outbox/ada/ceo-briefing-YYYY-MM-DD.md
│           (single document: what happened, what needs approval,
│            what's blocked, recommended priorities, items approaching
│            staleness threshold)
├── Flags: any conflicts, missed deadlines, or coordination issues
└── After CEO responds: writes .approved.md or .feedback.md files
    to each agent's outbox, relaying CEO decisions verbatim
                ↓
CEO (You) — talks ONLY to Ada (unless using direct access)
├── Reads: Ada's briefing (the only thing you need to check)
├── Responds: to Ada with approve/reject/feedback per item
├── Checks: escalations/ as a safety net (should be empty)
└── Updates: CEO.md with any new standing permissions or preferences
```

### 5.2 Execution Order

| Order | Agent | Depends On | Typical Timing |
|-------|-------|-----------|----------------|
| 1 | Curie | Nothing | Morning (first) |
| 2 | Tesla | Curie's intel | After Curie |
| 3 | Ogilvy | Curie's intel + Tesla's output | After Tesla |
| 3 | Nightingale | Curie's intel + Tesla's output | After Tesla (parallel with Ogilvy) |
| 4 | Ada | Everyone's outbox | Last (end of day) |

---

## 6. Agent Identity Summaries

### 6.1 Ada (Chief of Staff)

**Core Identity:** Organized, strategic, slightly protective of the CEO's time. Named after Ada Lovelace because she saw the bigger picture when everyone else was focused on gears.

**Key Responsibilities:**
- Single point of contact between the CEO and the team
- CEO briefings — one consolidated document with everything pending
- Route CEO decisions back to agents — relay feedback VERBATIM
- Staleness monitoring — proactively flag outbox items approaching escalation threshold
- Conflict resolution — mediate before escalating to CEO

**Critical Principles:**
1. The CEO's time is the scarcest resource. Protect it.
2. You are a router, not a filter. Never suppress or soften agent output.
3. When relaying CEO feedback to agents, preserve the CEO's exact words.
4. Flag problems early. Never let the CEO be surprised.

**Stop Condition:** When the CEO briefing is written, all CEO decisions from last session are routed to agents, and all coordination issues are logged.

**Writes to:** `outbox/ada/` (CEO briefings), `outbox/{agent}/` (relayed approvals and feedback)
**Reads from:** All other agents' outbox directories, all intel directories, `escalations/`, `CEO.md`

### 6.2 Curie (Head of Research)

**Core Identity:** Evidence-obsessed, thorough, allergic to speculation. Named after Marie Curie — she didn't guess, she measured.

**Key Responsibilities:**
- Gather signals: GitHub issues/PRs/discussions, community sentiment, ecosystem framework activity, trends
- Deliver structured intel briefs that every other agent consumes
- Track signals over time — what's trending up, what's fading

**Critical Principles:**
1. Every claim has a source. No exceptions.
2. Signal over noise. Not everything trending matters.
3. If uncertain, mark it [UNVERIFIED]. "I don't know" beats wrong.
4. Structure over narrative. Tables, rankings, data — not essays.

**Stop Condition:** When the intel brief is written with sources and delivered to the intel directory.

**Writes to:** `intel/research/` (briefs, signal tracker — no approval needed)
**Reads from:** External sources (GitHub, community channels, ecosystem framework repos)

### 6.3 Tesla (Head of Engineering)

**Core Identity:** Systems thinker, obsessed with elegant solutions, allergic to over-engineering. Named after Nikola Tesla — inventive but principled.

**Key Responsibilities:**
- Triage GitHub issues (label, prioritize, recommend assignments)
- Review PRs (code quality, test coverage, breaking changes, style)
- Write Architecture Decision Records (ADRs) for significant technical choices
- Make technology decisions with clear rationale

**Critical Principles:**
1. Start simple. Complexity is earned, not assumed.
2. Understand the problem fully before proposing a solution.
3. Every technical decision gets a one-paragraph rationale.
4. Be specific in reviews. Vague feedback is useless.

**Stop Condition:** When all open issues are triaged and all open PRs have review notes in the outbox.

**Writes to:** `outbox/tesla/` (triage reports, PR reviews), `intel/architecture/` (specs, ADRs)
**Reads from:** `intel/research/` (Curie's briefs), GitHub repo state

### 6.4 Ogilvy (Head of Growth)

**Core Identity:** Clear writer, allergic to jargon, thinks about the reader first. Named after David Ogilvy — he sold with clarity, not cleverness.

**Key Responsibilities:**
- Write release notes that users actually want to read
- Draft community updates (GitHub Discussions, Discord, etc.)
- Create social media content (Twitter/X, LinkedIn, etc.)
- Announce new features, milestones, and contributor highlights

**Critical Principles:**
1. Write for the user, not the developer. Lead with "what changed for you."
2. No jargon without explanation.
3. Celebrate contributors by name. Community is built on recognition.
4. Every piece of content has one clear call-to-action.

**Stop Condition:** When all content drafts are in the outbox with draft notes.

**Writes to:** `outbox/ogilvy/` (release notes, social posts, community updates)
**Reads from:** `intel/research/`, `intel/architecture/`, `approved/`, `CEO.md`

### 6.5 Nightingale (Head of Operations)

**Core Identity:** Data-driven, process-oriented, obsessed with contributor experience. Named after Florence Nightingale — she transformed outcomes by measuring what no one else bothered to track.

**Key Responsibilities:**
- Maintain and improve documentation (README, guides, API docs)
- Track repo health metrics (issue close time, PR merge time, contributor retention)
- Manage contributor experience (onboarding guide, templates, labels)
- Surface operational problems before they become crises

**Critical Principles:**
1. If it's not documented, it doesn't exist.
2. Measure what matters. Vanity metrics are noise.
3. Make contributing easier every week. Remove one friction point per cycle.
4. Good docs are the best marketing.

**Stop Condition:** When docs are updated and the weekly metrics report is in the outbox.

**Writes to:** `outbox/nightingale/` (doc updates, metrics reports), `intel/ops/`
**Reads from:** `intel/research/`, `intel/architecture/`, `approved/`, `CEO.md`

---

## 7. Other Use Cases (Included as Templates)

The framework ships with the OSS Repo Management use case pre-populated. `docs/USE-CASES.md` describes four additional patterns:

### 7.1 Content Engine for a SaaS Blog
Curie researches trending topics. Ogilvy drafts posts and social content. Nightingale tracks performance. Ada coordinates the editorial calendar. Tesla reviews code samples in technical posts.

### 7.2 Launch Week Playbook
All five agents at full throttle for a bounded sprint. Dedicated project directory, P0 priority, hard deadline. Tesla writes changelog, Ogilvy writes announcements, Curie researches positioning, Nightingale prepares support docs, Ada runs the launch checklist.

### 7.3 Weekly Ecosystem Intelligence Briefing
Curie monitors peer frameworks on a strict weekly cadence. Ogilvy suggests positioning content. Tesla flags technical implications. Ada delivers a consolidated Monday briefing.

### 7.4 Customer Feedback → Product Pipeline
Nightingale aggregates feedback from support channels. Curie analyzes patterns. Tesla writes specs for top requests. Ada presents a prioritized roadmap. The intel flow reverses — operations feeds research feeds engineering.

---

## 8. Getting Started (Week-by-Week)

### Week 1: Curie Only
- Fork the repo, fill in `CEO.md`
- Point your AI tool at `agents/curie/SOUL.md`
- Run daily research sessions, practice the feedback loop
- Refine Curie's SOUL.md based on output quality

### Week 2: Add Ada
- Ada reads Curie's intel and writes CEO briefings
- Practice: read briefing → respond with decisions → Ada routes them
- Establish the daily briefing habit

### Week 3: Add Tesla
- Tesla triages issues and reviews PRs, reads Curie's intel
- Three agents coordinating through files

### Week 4: Add Ogilvy + Nightingale
- Ogilvy writes release notes from Tesla's changelogs
- Nightingale starts maintaining docs and tracking metrics
- Full team operational

### Week 5+: Add Projects
- New initiative? Copy `_template/`, fill in `PROJECT.md`, set priority, assign agents
- The system scales horizontally

---

## 9. Governance Quick Reference

| Action | Requires CEO Approval? | Flow |
|--------|----------------------|------|
| Publish release notes | Yes | Ogilvy → outbox → **Ada consolidates** → CEO decides → Ada routes back |
| Merge a PR recommendation | Yes | Tesla → outbox → **Ada consolidates** → CEO decides → Ada routes back |
| Update README/docs | Depends on `CEO.md` standing permissions | Nightingale → outbox → Ada checks permissions → routes or auto-approves |
| Post to social media | Yes | Ogilvy → outbox → **Ada consolidates** → CEO decides |
| Research brief (internal only) | No — intel is internal | Curie writes directly to `intel/research/` |
| Architecture decision (ADR) | Yes | Tesla → outbox → **Ada consolidates** → CEO decides |
| CEO briefing | No — it IS the CEO communication | Ada writes to `outbox/ada/` |
| Change project priority | CEO ONLY | CEO updates `PROJECTS.md` (tells Ada, who informs team) |
| Escalation (stalled item) | N/A — bypasses Ada | Agent writes to `escalations/` → CEO reads directly |
| Grant standing permission | CEO ONLY | CEO updates `CEO.md` → Ada reads next session |

---

## 10. Self-Healing (HEARTBEAT.md)

The framework includes a `HEARTBEAT.md` file that defines health checks Ada runs at every session:

1. **Outbox staleness** — flag items approaching the 48hr/24hr escalation thresholds
2. **Agent activity** — verify each agent has logged a session within expected timeframe
3. **Intel freshness** — verify Curie's research briefs are current
4. **Escalation queue** — surface any pending escalations at the top of the briefing
5. **Project consistency** — verify `PROJECTS.md` matches actual project directory state

If all checks pass, the health section is omitted from the briefing. No noise when things are healthy.

For scheduled environments (OpenClaw, cron), the heartbeat can force re-runs of stale jobs. For manual environments, it serves as advisory — telling the CEO which agent to run next.

---

## 11. Memory System

### Two-Layer Memory

**Daily logs** (`agents/{agent}/memory/YYYY-MM-DD.md`): Raw session notes. What happened, what was produced, what feedback came in. Written at the end of every session.

**Long-term memory** (`agents/{agent}/MEMORY.md`): Curated insights distilled from daily logs. Lessons learned, preferences discovered, patterns noticed. Kept under 100 lines. Quality over quantity.

### Memory Rules
- Agent-level memory is cross-project (lives in `agents/{agent}/`)
- Project-level context is project-specific (lives in the project directory)
- "Mental notes" don't survive sessions — if it matters, write it to a file
- Daily logs older than 14 days can be archived or summarized
- MEMORY.md is periodically reviewed and refined — curated wisdom, not raw history

### Why This Works
Agents improve over time not because the model changes, but because the context they load gets richer. Curie learns which signals pass the CEO's filter. Ogilvy learns the CEO's voice. Tesla learns the codebase conventions. This accumulated context is the real moat — not the model.

---

## 12. Compatible AI Tools

The framework works with any tool that reads files and follows markdown instructions:

| Tool | How to Use |
|------|-----------|
| **Claude Code** | Load SOUL.md as context, reference AGENTS.md and CEO.md |
| **Cursor** | Use SOUL.md as project rules or reference in chat |
| **Windsurf** | Rules files are natively supported |
| **Cline / Roo Code** | Pass SOUL.md as system context |
| **Aider** | Include SOUL.md in chat context |
| **OpenClaw** | For always-on scheduling with cron + Telegram |

If your tool can read a file and follow instructions, it can run these agents.

---

## 13. Repo File Manifest

| File | Path | Purpose |
|------|------|---------|
| README.md | `/README.md` | Framework overview, quick start, use cases |
| AGENTS.md | `/AGENTS.md` | Shared operating rules for all agents |
| CEO.md | `/CEO.md` | CEO preferences, standing permissions, voice profile |
| PROJECTS.md | `/PROJECTS.md` | Project registry & priority dashboard |
| HEARTBEAT.md | `/HEARTBEAT.md` | Self-healing cron monitor |
| ARCHITECTURE.md | `/docs/ARCHITECTURE.md` | This document |
| GETTING-STARTED.md | `/docs/GETTING-STARTED.md` | Detailed onboarding guide |
| USE-CASES.md | `/docs/USE-CASES.md` | 4 use case templates |
| GOVERNANCE.md | `/docs/GOVERNANCE.md` | Deep dive on the approval queue |
| CUSTOMIZATION.md | `/docs/CUSTOMIZATION.md` | How to fork and adapt |
| Ada SOUL.md | `/agents/ada/SOUL.md` | Chief of Staff identity & instructions |
| Curie SOUL.md | `/agents/curie/SOUL.md` | Head of Research identity & instructions |
| Tesla SOUL.md | `/agents/tesla/SOUL.md` | Head of Engineering identity & instructions |
| Ogilvy SOUL.md | `/agents/ogilvy/SOUL.md` | Head of Growth identity & instructions |
| Nightingale SOUL.md | `/agents/nightingale/SOUL.md` | Head of Operations identity & instructions |
| Template PROJECT.md | `/projects/_template/PROJECT.md` | Blank template for new projects |
| Starter PROJECT.md | `/projects/inner-circle-mgmt/PROJECT.md` | Self-referential starter use case |
| CLAUDE.md | `/CLAUDE.md` | Project rules for Claude Code sessions |
| Bot entry point | `/bot/main.py` | Telegram bot — Ada's chat interface |
| Bot config | `/bot/config.py` | Agent definitions, per-agent tool permissions |
| Bot runner | `/bot/runner.py` | Spawns `claude -p` sessions per agent |
| Bot briefing parser | `/bot/briefing.py` | Parses Ada's briefing markdown |
| Bot file router | `/bot/router.py` | Writes approval/feedback/rejection files |
| Bot Ada handler | `/bot/ada.py` | Free-text CEO messages → Ada Claude session |
| Bot projects parser | `/bot/projects.py` | Parses PROJECTS.md for active slugs |
| Bot escalation watcher | `/bot/watcher.py` | Scans escalation directories |
| Bot handlers | `/bot/handlers.py` | Telegram message/callback routing |

---

## 14. Telegram Bot — Ada as a Chat Interface

The file-based approval queue is wrapped by a Telegram bot. The bot IS Ada — one conversation, one contact.

### 14.1 How It Works

```text
CEO sends "run the team" in Telegram
        ↓
Bot spawns claude -p for each agent sequentially:
  Curie → Tesla → Ogilvy → Nightingale → Ada
        ↓
Each agent runs in its own isolated session:
  - Reads SOUL.md, AGENTS.md, CEO.md, PROJECTS.md, PROJECT.md
  - Checks outbox for feedback files
  - Executes session workflow
  - Writes output to intel/, outbox/, memory/
        ↓
Bot sends status updates to Telegram as each agent completes
        ↓
After Ada finishes, bot reads ceo-briefing-YYYY-MM-DD.md
        ↓
Bot sends each decision item with inline buttons:
  [✅ Approve]  [❌ Reject]  [💬 Feedback]
        ↓
CEO taps buttons → bot writes .approved.md or .feedback.md
        ↓
Next run, agents pick up decisions from their outbox
```

### 14.2 Per-Agent Tool Permissions

Each agent gets only the tools it needs via `claude -p --allowedTools`. This is the security boundary.

| Agent | File Access | Git | GitHub CLI | Web |
| ----- | ----------- | --- | ---------- | --- |
| Curie | Read/Write/Edit/Glob/Grep | Read | `gh issue`, `gh pr`, `gh api` | WebSearch, WebFetch |
| Tesla | Read/Write/Edit/Glob/Grep | Read + Write | `gh issue`, `gh pr`, `gh api` | No |
| Ogilvy | Read/Write/Edit/Glob/Grep | Read | No | WebSearch, WebFetch |
| Nightingale | Read/Write/Edit/Glob/Grep | Read | No | WebSearch, WebFetch |
| Ada | Read/Write/Edit/Glob/Grep | Read + Write | No | No |

**Why per-agent:** Curie needs web access for research but shouldn't push code. Tesla needs git write for commits but doesn't need web access. Ada needs git write to update PROJECTS.md but nothing else. Least privilege per role.

### 14.3 Message Types

| CEO Input | Bot Behavior |
| --------- | ------------ |
| `run the team` | All 5 agents in dependency order, then briefing |
| `run curie` | Single agent only |
| `run curie tesla ada` | Specified agents in dependency order |
| [Approve button] | Write `.approved.md` to agent's outbox |
| [Reject button] | Write `.feedback.md` with `rejected` verdict |
| [Feedback button] → text | Write `.feedback.md` with CEO's exact words |
| Free-text question | Spawn Ada Claude session, return answer |
| Free-text command | Ada executes (e.g., updates PROJECTS.md) |

### 14.4 Design Decisions

- **Sequential, not parallel.** Agents run one at a time because each depends on the previous agent's file output. Curie writes intel, Tesla reads it. No race conditions.
- **One Claude session per agent.** Each agent gets a fresh context window. No context pollution between agents. The files on disk are the handoff mechanism.
- **Single-user only.** CEO's Telegram chat ID is hardcoded. Bot silently ignores all other senders.
- **Long-polling, no webhook.** Runs locally on the CEO's machine. No server infrastructure needed.
- **File layer stays identical.** The bot is a convenience wrapper. Remove the bot and the framework still works via manual sessions in any AI tool.

### 14.5 Phase 2 (TBD)

- Cron-based scheduling — agents run on a schedule, bot sends briefings automatically
- Cloud deployment — always-on via Railway, Fly.io, or similar
- Multi-user — co-founders or team leads interacting with Ada
