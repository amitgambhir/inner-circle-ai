# HEARTBEAT.md — Self-Healing Monitor

This file defines the health checks that Ada (or any scheduling system) runs periodically to catch failures and stale jobs.

---

## Purpose

Cron jobs fail. Sessions crash. Networks drop. This is infrastructure, and infrastructure has failure modes. The heartbeat system catches problems before they cascade.

Ada runs these checks at the start of every session. If using a scheduling system (OpenClaw, cron, etc.), these checks run on a regular heartbeat interval.

---

## Health Checks

### 1. Outbox Staleness Check

**What:** Scan all agent outboxes across active projects for items with no corresponding `.approved.md` or `.feedback.md` file.

**Threshold:**
- Normal items: flag if older than **36 hours** (warn), escalation-eligible at **48 hours**
- URGENT items: flag if older than **18 hours** (warn), escalation-eligible at **24 hours**

**Action:**
- If approaching threshold → include warning in CEO briefing
- If past threshold → verify agent hasn't already self-escalated, then flag as critical in briefing

### 2. Agent Activity Check

**What:** Verify each agent has produced a daily memory log within the expected timeframe.

**How:** Check `agents/{agent}/memory/` for a file dated within the last execution cycle.

**Expected cadence:**
| Agent | Expected Frequency |
|-------|--------------------|
| Curie | Daily (runs first) |
| Tesla | Daily (after Curie) |
| Ogilvy | 2-3x per week |
| Nightingale | Weekly (metrics), as-needed (docs) |
| Ada | Daily (runs last) |

**Action:** If an agent's last memory log is older than expected, note it in the CEO briefing: "{Agent} hasn't logged a session since {date}. May need manual session."

### 3. Intel Freshness Check

**What:** Verify Curie's research briefs are current.

**How:** Check `intel/research/` for a brief dated within the last execution cycle.

**Action:** If intel is stale, other agents may be working from outdated information. Flag in briefing and recommend running Curie before other agents.

### 4. Escalation Queue Check

**What:** Check `escalations/` directories across active projects.

**Action:** If any escalation files exist, surface them at the TOP of the CEO briefing. Escalations are fire alarms.

### 5. Project Priority Consistency

**What:** Verify `PROJECTS.md` matches the actual state of project directories.

**Checks:**
- Every project listed in `PROJECTS.md` has a corresponding directory in `projects/`
- No active project has an empty `intel/` directory (suggests no work has started)
- No paused project has recent outbox items (suggests someone is working on a paused project)

**Action:** Flag inconsistencies in the CEO briefing.

---

## For Scheduled Environments (OpenClaw, Cron, etc.)

If running agents on automated schedules, add cron job IDs here for monitoring:

```
Jobs to monitor:
- Curie Morning: {job-id}
- Tesla Daily: {job-id}
- Ogilvy Content: {job-id}
- Nightingale Weekly: {job-id}
- Ada EOD Briefing: {job-id}
```

**Staleness rule:** If any cron job's last run timestamp is older than 26 hours, force a re-run:
```
{scheduling-tool} cron run <jobId> --force
```

---

## For Manual Environments (No Scheduling)

If running agents manually (opening sessions in Claude Code, Cursor, etc.), Ada should check the timestamps of the most recent daily memory logs and flag any agent that hasn't been run recently.

The heartbeat is advisory in manual mode — it tells you what to run next, not what failed automatically.

---

## Heartbeat Report Section (For Ada's CEO Briefing)

Add this section to the CEO briefing when any check fails:

```markdown
## System Health

| Check | Status | Notes |
|-------|--------|-------|
| Outbox staleness | ✅ OK / ⚠️ {n} items approaching threshold / 🚨 {n} items past threshold | {details} |
| Agent activity | ✅ All active / ⚠️ {agent} last seen {date} | |
| Intel freshness | ✅ Current / ⚠️ Last brief: {date} | |
| Escalations | ✅ None / 🚨 {n} pending | |
| Project consistency | ✅ OK / ⚠️ {issue} | |
```

If all checks pass, omit this section from the briefing entirely. Don't clutter the briefing with "everything is fine" when it is.
