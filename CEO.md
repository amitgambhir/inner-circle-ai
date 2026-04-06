# CEO.md — CEO Preferences & Authority

This file defines the CEO's operating preferences, standing permissions, and voice profile. Every agent reads this at session start.

---

## Operating Preferences

### Communication Style
- Be direct. Skip preamble and pleasantries in work output.
- Lead with the recommendation, not the analysis.
- When presenting options, state which one you'd pick and why.
- Use real numbers and sources, not vague claims.
- Start simple. Complexity is earned, not assumed.

### Decision-Making
- I want one consolidated briefing from Ada, not five separate reports.
- For urgent items, flag them clearly — don't bury them in a long briefing.
- When something is blocked on me, say so explicitly. Don't hint.
- If you need a decision, frame it as: "I recommend X because Y. Approve or redirect?"

### Feedback Style
- When I give feedback, I mean it literally. Don't interpret or soften.
- If I say "too formal," make it casual. Don't make it slightly less formal.
- If I approve with no comments, that means ship it as-is.
- "Looks good" means approved. "Almost" means revise.

---

## Standing Permissions

These are the ONLY cases where an agent may act without routing through the approval queue. Everything else requires CEO approval via Ada.

| Agent | Permission | Scope |
|-------|-----------|-------|
| Curie | Write research briefs directly to `intel/` | All projects — intel is internal working documents |
| Nightingale | Fix typos, formatting, and broken links in docs | Only in already-approved documents |
| Ada | Write CEO briefings to outbox | This is her core job — no approval needed to brief |
| All agents | Write to their own memory files | Memory is internal |

**To add a permission:** CEO updates this table. Ada reads it next session and informs the relevant agent.

**To revoke a permission:** CEO removes the row. Effective immediately.

---

## Escalation Thresholds

| Item Type | Escalation After |
|-----------|-----------------|
| Normal outbox items | 48 hours with no response |
| Items tagged `[URGENT]` | 24 hours with no response |

These thresholds can be adjusted. Ada monitors staleness and should flag items in the CEO briefing before they reach the escalation threshold.

---

## Voice Profile

> **Instructions for users:** Replace this section with your own voice profile. Feed your AI tool 5-10 of your best writing samples (emails, blog posts, LinkedIn posts, tweets) and ask it to identify patterns. Paste the output here.

### Tone
- [Example: Direct, conversational, no corporate speak]
- [Example: Occasional dry humor, never sarcastic]

### Writing Patterns
- [Example: Short sentences. Punchy paragraphs. Rarely more than 3 sentences per paragraph.]
- [Example: Uses analogies to explain complex ideas]

### Things I Never Do
- [Example: No emojis in professional content]
- [Example: No hashtags]
- [Example: Never use "leverage" as a verb]

### Things I Always Do
- [Example: Always include a concrete next step]
- [Example: Address the reader directly — "you" not "one"]

---

## Direct Access Clause

The CEO may talk to any agent directly at any time, bypassing Ada. This is the CEO's prerogative. Ada does not gatekeep the CEO — she gatekeeps the agents.

If the CEO works with an agent directly, that agent should log the interaction in their daily memory. Ada will pick it up next session.

---

## Priority Override

Only the CEO can change project priorities in `PROJECTS.md`. If the CEO tells Ada to shift priorities, Ada updates the file and informs the affected agents in her next coordination pass.
