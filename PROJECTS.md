# PROJECTS.md — Project Registry & Priority Dashboard

Every agent reads this at session start. This is the single source of truth for what's active and what matters.

**Only the CEO can change priorities.** Ada updates this file when the CEO directs a priority shift.

---

## Active Projects

| Priority | Project | Slug | Status | Lead Agents | Notes |
|----------|---------|------|--------|-------------|-------|
| **P0** | Inner Circle AI — Self-Management | `inner-circle-mgmt` | Active | All | The framework managing its own repo. Starter use case. |

## Priority Levels

- **P0 (Critical):** Drop everything. Only one P0 at a time.
- **P1 (High):** Active work alongside P0.
- **P2 (Normal):** Steady progress when higher priorities are clear.
- **P3 (Low):** Background only. Work on this when nothing else is pending.
- **Paused:** Frozen in place. No active work. Don't touch.

## Adding a New Project

1. Copy `projects/_template/` to `projects/{new-slug}/`
2. Fill in `PROJECT.md` with the project brief
3. Add a row to this table
4. Assign priority and lead agents
5. CEO approves the addition

## Rules

- Only one P0 at a time.
- New projects start at P2 unless the CEO says otherwise.
- Paused projects are frozen — don't reference their context in other projects.
- If a project has no activity for 30+ days and isn't paused, Ada should flag it in the CEO briefing.
