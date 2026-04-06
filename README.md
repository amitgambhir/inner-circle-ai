# Inner Circle AI

**Five AI agents. One team. You're the CEO.**

A file-based framework for running a team of 5 specialized AI agents that operate as your startup's leadership team. No APIs between agents, no message queues, no orchestration servers. Just markdown files. Each agent reads what it needs, writes what it owns, and routes everything through your Chief of Staff.

You make every decision. Agents propose. You approve. Nothing ships, publishes, merges, or goes live without your explicit sign-off.

Built as a self-managing open-source project (this repo manages itself), but the pattern works for any business. Fork it, rename the agents, swap in your industry context, and you have your own autonomous team.

---

## Why File-Based?

Modern AI tools — Claude Code, Cursor, Windsurf, Cline, Aider, and others — all understand files natively. They read markdown, follow instructions in context, and write output to disk. This framework leans into that.

- **No vendor lock-in.** SOUL.md files work in any tool that reads project files.
- **No infrastructure.** No databases, no queues, no orchestration servers. Git is your state management.
- **Portable agents.** Move a SOUL.md between tools and the agent behaves the same way.
- **Human-readable everything.** Every instruction, every output, every coordination artifact is a markdown file you can read and edit.

Pick whichever AI tool fits your workflow. Open a session, point it at an agent's SOUL.md, and go.

---

## The Team

| Agent | Named After | Role | Job |
|-------|------------|------|-----|
| **Ada** | Ada Lovelace | Chief of Staff | Coordinate the team, brief the CEO, route all decisions |
| **Curie** | Marie Curie | Head of Research | Gather intelligence, analyze signals, deliver structured briefs |
| **Tesla** | Nikola Tesla | Head of Engineering | Triage issues, review PRs, write specs, technical decisions |
| **Ogilvy** | David Ogilvy | Head of Growth | Release notes, community updates, social content, announcements |
| **Nightingale** | Florence Nightingale | Head of Operations | Documentation, metrics, contributor experience, process improvement |

### How They Work Together

```
Curie (Research) ───→ writes intel ───→ Everyone reads
Tesla (Engineering) ─→ writes specs ──→ Nightingale updates docs, Ogilvy writes release notes
Ogilvy (Growth) ────→ writes drafts ──→ Ada reviews, routes to CEO
Nightingale (Ops) ──→ writes docs ───→ Ada includes in CEO briefing

All agents ─────────→ write to outbox → Ada consolidates → CEO decides
```

Ada is your single point of contact. You talk to Ada. Ada talks to the team. The agents never bypass her unless something is genuinely stuck (see Escalations below).

---

## The Governance Model — You're the CEO

This is not a "set it and forget it" system. You have explicit authority over every output.

### The Approval Queue

```
Agent produces output
        ↓
Writes to: projects/{slug}/outbox/{agent}/filename.md
        ↓
Ada reads ALL outboxes, consolidates
        ↓
Ada writes: outbox/ada/ceo-briefing-YYYY-MM-DD.md
  → Everything pending, prioritized, with her recommendations
        ↓
You read Ada's briefing (the ONLY thing you need to check)
You respond: "approve 1 and 3, feedback on 2"
        ↓
Ada routes your decisions back to each agent
        ↓
Agents pick up approvals/feedback next session
```

### Standing Permissions

As you build trust, you can grant agents permission to act without approval on specific tasks. Define these in `CEO.md`. Example: "Nightingale may fix README typos without approval." Everything else goes through the queue.

### Escalations — The Fire Alarm

If an agent finds their outbox items have been waiting 48+ hours with no response (24 hours for urgent items), they write an escalation to `projects/{slug}/escalations/`. You check this directory directly — it should almost always be empty. Ada also monitors staleness and flags items before they hit the threshold.

---

## Directory Structure

```
inner-circle-ai/
├── README.md                         ← You are here
├── AGENTS.md                         ← Shared operating rules for all agents
├── CEO.md                            ← Your preferences, standing permissions, voice profile
├── PROJECTS.md                       ← Project registry & priority dashboard
├── HEARTBEAT.md                      ← Self-healing cron monitor
│
├── agents/                           ← Agent identities (global, not project-specific)
│   ├── ada/
│   │   ├── SOUL.md                   ← Ada's identity and instructions
│   │   ├── MEMORY.md                 ← Ada's curated long-term memory
│   │   └── memory/                   ← Ada's daily session logs
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
│   ├── _template/                    ← Copy this to start any new project
│   │   ├── PROJECT.md
│   │   ├── intel/
│   │   ├── outbox/
│   │   ├── approved/
│   │   ├── feedback/
│   │   ├── escalations/
│   │   ├── content/
│   │   └── CHANGELOG.md
│   │
│   └── inner-circle-mgmt/           ← Starter: this repo managing itself
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
└── docs/
    ├── GETTING-STARTED.md
    ├── USE-CASES.md                  ← 4 use case templates
    ├── GOVERNANCE.md                 ← Deep dive on the approval queue
    └── CUSTOMIZATION.md              ← How to fork and make it yours
```

---

## The Starter Use Case: This Repo Manages Itself

The default project (`projects/inner-circle-mgmt/`) is the agents managing the inner-circle-ai repo. This is intentionally self-referential:

- **Curie** monitors GitHub issues, PRs, community discussions, stars/forks trends, and competitor agent frameworks
- **Tesla** triages issues, reviews PRs, writes architecture decision records
- **Ogilvy** writes release notes, community updates, social announcements
- **Nightingale** maintains the docs you're reading right now, tracks repo health metrics
- **Ada** coordinates everything and delivers your daily briefing

This means you can see the framework in action the moment you fork it.

---

## Other Use Cases

The framework is use-case-agnostic. These are included as templates in `docs/USE-CASES.md`:

**Content Engine for a SaaS Blog** — Curie researches trending topics, Ogilvy drafts posts and social content, Nightingale tracks what's performing, Ada coordinates the editorial calendar. Great for solo founders who need consistent content output.

**Launch Week Playbook** — All five agents at full throttle for a bounded sprint. Tesla writes the changelog, Ogilvy writes the announcements, Curie researches positioning, Nightingale prepares support docs, Ada runs the launch checklist with hard deadlines.

**Weekly Competitor Intelligence Briefing** — Curie monitors competitor activity on a weekly cadence. Ogilvy suggests response content. Tesla flags technical implications. Ada delivers a consolidated Monday briefing.

**Customer Feedback → Product Pipeline** — Nightingale aggregates feedback from support channels, Curie analyzes patterns, Tesla writes specs for top requests, Ada presents a prioritized roadmap.

---

## Compatible AI Tools

This framework works with any tool that reads files and follows markdown instructions:

- **Claude Code** — load a SOUL.md as context
- **Cursor** — use SOUL.md as project rules
- **Windsurf** — rules files are natively supported
- **Cline / Roo Code** — pass SOUL.md as system context
- **Aider** — include SOUL.md in chat context
- **OpenClaw** — for always-on scheduling with cron and Telegram

If your tool can read a file and follow instructions, it can run these agents.

---

## How to Get Started

**Do not build all five agents on day one.**

### Week 1: Curie (Research)
Install your preferred AI tool. Point it at `agents/curie/SOUL.md`. Ask Curie to research your repo's open issues and community activity. Review her output in `outbox/curie/`. Practice giving feedback. Refine her SOUL.md.

### Week 2: Add Ada (Chief of Staff)
Ada reads Curie's intel and starts writing CEO briefings. You now have a daily review habit: read Ada's briefing, respond with decisions.

### Week 3: Add Tesla (Engineering)
Tesla triages issues, reviews PRs, writes specs. Three agents coordinating through files.

### Week 4: Add Ogilvy + Nightingale
Ogilvy writes release notes from Tesla's changelogs. Nightingale maintains docs. Full team operational.

### Week 5+: Add Projects
New initiative? Copy `projects/_template/`, fill in `PROJECT.md`, set priority in `PROJECTS.md`, assign agents. The system scales horizontally.

---

## Making It Yours

1. **Fork this repo**
2. **Rename agents** if you want — pick figures who embody each role for your domain
3. **Fill in `CEO.md`** — your preferences, voice profile, and standing permissions
4. **Swap the starter use case** — replace `inner-circle-mgmt/` with your own project
5. **Start with one agent** — get comfortable, then add the rest

---

## Key Files Explained

| File | What It Does |
|------|-------------|
| `SOUL.md` | Defines an agent's identity, role, principles, and stop condition. The most important file per agent. |
| `AGENTS.md` | Shared rules every agent follows. Session startup checklist, memory rules, communication standards. |
| `CEO.md` | Your preferences, standing permissions, and voice profile. Agents read this to understand how you work. |
| `PROJECTS.md` | The priority dashboard. What's active, what matters most. Agents check this at session start. |
| `HEARTBEAT.md` | Self-healing monitor. Detects stale cron jobs and forces re-runs. |
| `MEMORY.md` | Per-agent curated long-term memory. Lessons, preferences, patterns — distilled from daily logs. |

---

## License

MIT — use it however you want.
