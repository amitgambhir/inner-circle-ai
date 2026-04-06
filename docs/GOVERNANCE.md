# Governance — The CEO Approval Model

This document explains the full governance model in detail. For the quick version, see the README.

---

## Core Principle

The CEO has explicit authority over all output. Agents propose. The CEO decides. Nothing externally visible ships without approval.

---

## The Hub-and-Spoke Model

All communication between the CEO and the agent team flows through Ada (Chief of Staff).

```
           ┌── Curie (Research)
           ├── Tesla (Engineering)
CEO ←→ ADA ├── Ogilvy (Growth)
           └── Nightingale (Operations)
```

**Why this structure:**
- The CEO checks one briefing, not five outboxes
- Ada consolidates and prioritizes, saving CEO time
- Maps directly to a future chat interface (Telegram/WhatsApp) where Ada IS the bot
- Consistent communication standards — Ada enforces formatting and completeness

**Direct access clause:** The CEO can always talk to any agent directly. Ada doesn't gatekeep the CEO — she gatekeeps the agents.

---

## The Approval Queue — Step by Step

### Step 1: Agent Produces Output
The agent writes to their outbox directory:
```
projects/{slug}/outbox/{agent}/filename.md
```

Every file includes a standard header with agent name, type, project, priority, date, and status.

### Step 2: Ada Consolidates
At her next session, Ada reads all outboxes and writes a CEO briefing:
```
projects/{slug}/outbox/ada/ceo-briefing-YYYY-MM-DD.md
```

The briefing lists every pending item, prioritized, with Ada's recommendation (approve/revise/reject) per item.

### Step 3: CEO Reviews
The CEO reads Ada's briefing and responds with decisions. This can be as simple as:
- "Approve 1 and 3"
- "Item 2 needs work — the tone is too formal, make it conversational"
- "Reject 4 — we're not doing this right now"

### Step 4: Ada Routes Decisions
Ada writes the appropriate file to each agent's outbox:

**For approvals:**
```
projects/{slug}/outbox/{agent}/filename.approved.md
```

**For feedback:**
```
projects/{slug}/outbox/{agent}/filename.feedback.md
```

Ada includes the CEO's exact words plus routing context (which project, which file). She never rephrases feedback.

### Step 5: Agent Acts on Decision
Next session, the agent checks their outbox for `.approved.md` and `.feedback.md` files. Feedback gets addressed before new work is produced.

---

## Standing Permissions

The CEO can grant agents permission to bypass the queue for specific, well-defined actions. These are listed in `CEO.md`.

**Rules:**
- Standing permissions are the ONLY way to skip the approval queue
- They must be specific: "Nightingale may fix typos in already-approved docs" — not "Nightingale can update docs"
- The CEO adds and removes permissions by editing `CEO.md`
- Ada tracks which permissions exist and doesn't route those items to the CEO

**Default permissions (shipped with framework):**
- Curie can write research briefs directly to `intel/` (internal working documents)
- Nightingale can fix typos/formatting/broken links in already-approved docs
- All agents can write to their own memory files

---

## Escalations

If the approval queue stalls (Ada isn't running or the CEO hasn't responded), agents have a safety valve.

**Thresholds:**
- Normal items: eligible for escalation after 48 hours with no response
- Urgent items: eligible after 24 hours

**Process:**
1. Agent verifies no `.approved.md` or `.feedback.md` file exists
2. Agent writes to `projects/{slug}/escalations/{agent}-escalation-YYYY-MM-DD.md`
3. CEO checks `escalations/` directly (should almost always be empty)

**Prevention:** Ada proactively monitors staleness. She flags items approaching the threshold in her CEO briefings BEFORE agents need to escalate. If escalations are firing regularly, it means Ada isn't running frequently enough.

---

## What Requires Approval vs. What Doesn't

| Action | Approval Required? | Reasoning |
|--------|-------------------|-----------|
| Publishing content externally | Yes | Externally visible, irreversible |
| Merging a PR | Yes | Code changes are significant |
| Architecture decisions (ADRs) | Yes | Long-term impact |
| Changing project priority | CEO only | Strategic decision |
| Social media posts | Yes | Brand reputation |
| Internal research briefs | No | Working documents, not externally visible |
| Agent memory updates | No | Internal to the agent |
| CEO briefings from Ada | No | This IS the communication channel |
| Typo fixes in approved docs | Depends on standing permission | Low risk, high friction if queued |

---

## Future: Chat-Based Approval

The file-based approval queue is designed to be wrapped by a chat interface. A Telegram or WhatsApp bot would:

1. **Be Ada.** The bot IS Ada — one conversation, one contact.
2. Watch `outbox/ada/` for new CEO briefings
3. Send the CEO a message with a summary and approve/reject buttons per item
4. Write approval/feedback files back to each agent's outbox
5. Watch `escalations/` and send direct alerts for stalled items

The file layer underneath remains identical. The chat layer is a convenience wrapper.
