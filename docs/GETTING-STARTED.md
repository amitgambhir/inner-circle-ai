# Getting Started — Inner Circle AI

## Prerequisites

You need one thing: an AI coding tool that can read files and follow markdown instructions. Any of these work:

- **Claude Code** (terminal)
- **Cursor** (IDE)
- **Windsurf** (IDE)
- **Cline / Roo Code** (VS Code extension)
- **Aider** (terminal)
- **OpenClaw** (always-on daemon with scheduling)

No programming language, no dependencies, no build step. The framework is pure markdown files.

---

## Quick Start (15 minutes)

### 1. Fork or Clone the Repo

```bash
git clone https://github.com/{your-username}/inner-circle-ai.git
cd inner-circle-ai
```

### 2. Fill in CEO.md

Open `CEO.md` and fill in your preferences. At minimum:
- Your communication style preferences
- Your voice profile (even a rough draft helps)
- Review the standing permissions — adjust if needed

### 3. Start Your First Agent Session (Curie)

Open your AI tool and point it at the Curie agent:

**Claude Code:**
```
Read agents/curie/SOUL.md, AGENTS.md, CEO.md, and PROJECTS.md. 
You are Curie, Head of Research. Your active project is inner-circle-mgmt.
Start by reading the project brief at projects/inner-circle-mgmt/PROJECT.md, 
then run your session workflow as defined in your SOUL.md.
```

**Cursor / Windsurf:** Add `agents/curie/SOUL.md` and `AGENTS.md` as project rules or reference files, then start a chat session.

### 4. Review Curie's Output

After the session, check:
- `projects/inner-circle-mgmt/intel/research/` — her research brief
- `projects/inner-circle-mgmt/outbox/curie/` — anything needing your approval
- `agents/curie/memory/` — her session log

### 5. Repeat Daily for One Week

Run Curie once a day for a week. Give feedback. Watch her output improve as her memory files accumulate context.

---

## Week-by-Week Ramp-Up

### Week 1: Curie Only
- Run daily research sessions
- Practice the feedback loop: review output → give feedback → watch improvement
- Refine her SOUL.md if the output doesn't match expectations
- Goal: Curie produces research briefs you find useful

### Week 2: Add Ada
- Run Ada after Curie each day
- Ada reads Curie's intel and writes your first CEO briefing
- Practice the approval flow: read briefing → respond with decisions → Ada routes them
- Goal: You have a daily briefing habit that takes <5 minutes to review

### Week 3: Add Tesla
- Run Tesla after Curie (he reads her intel)
- Tesla triages issues and reviews PRs
- Three agents coordinating through files
- Goal: Issues are triaged and PRs have review notes without you doing it manually

### Week 4: Add Ogilvy + Nightingale
- Ogilvy drafts release notes from Tesla's changelogs
- Nightingale starts tracking metrics and reviewing docs
- Full team operational
- Goal: Complete team running with <15 minutes/day CEO oversight

### Week 5+: Add Projects
- When a new initiative comes up, copy `projects/_template/`
- Set priority in `PROJECTS.md`
- Assign agent focus areas
- The system scales horizontally

---

## Running Agents in Order

When running manually, follow this order (each agent depends on the previous one's output):

```
1. Curie    (research — runs first, no dependencies)
2. Tesla    (engineering — reads Curie's intel)
3. Ogilvy   (growth — reads Curie's intel + Tesla's output)
3. Nightingale (ops — reads Curie's intel + Tesla's output, parallel with Ogilvy)
4. Ada      (chief of staff — reads everyone's output, runs last)
```

You don't need to run every agent every day. Curie and Ada daily, Tesla 2-3x/week, Ogilvy and Nightingale as needed.

---

## Tips for Getting Good Output

**Keep SOUL.md short.** 40-60 lines is the sweet spot. Long enough for clear instructions. Short enough to fit in context every session.

**Give specific feedback.** "This is bad" teaches nothing. "The ranking should prioritize items with >100 GitHub stars" teaches a lot.

**Let memory accumulate.** Agents get better over time because their memory files get richer. Don't clear memory unless it's actually cluttered.

**Start simple.** One agent, one job, one project. Get that working before adding complexity.

---

## Troubleshooting

**Agent ignores its SOUL.md:** Make sure you're loading the file at session start. In some tools, you need to explicitly reference it.

**Output quality degrades:** Check if memory files are cluttered or contradictory. Review MEMORY.md and trim it.

**Agents produce duplicate work:** Check that file flow is clear — one writer per file. If two agents are writing to the same directory, clarify ownership in their SOUL.md files.

**Context window overflow:** Keep SOUL.md short, load only today's + yesterday's memory, and only the relevant project's files. The agent doesn't need to read its entire history every session.
