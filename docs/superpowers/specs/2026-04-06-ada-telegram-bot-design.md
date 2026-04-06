# Ada Telegram Bot — Design Spec

**Date:** 2026-04-06
**Status:** Draft
**Purpose:** Telegram bot that serves as Ada's interface to the CEO — two-way communication for briefings, approvals, follow-ups, and agent management.

---

## 1. Overview

The bot IS Ada in Telegram. One conversation, one contact. The file-based framework underneath stays identical — the bot is a read/write layer on top of the existing file structure.

**Single user:** Hardcoded CEO chat ID. Rejects all other senders.
**Local first:** Runs on the CEO's machine via long-polling. No webhook, no server.
**Phase 2 (later):** Cron-based scheduling, cloud deployment.

---

## 2. Components

### 2.1 Telegram Bot (Entry Point)

- Python, using `python-telegram-bot` (async, long-polling)
- Single `.env` file for config: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CEO_CHAT_ID`
- Rejects messages from any chat ID that doesn't match `TELEGRAM_CEO_CHAT_ID`
- Runs as a foreground process: `python bot/main.py`

### 2.2 Agent Runner

Spawns `claude -p` sessions as subprocesses, one per agent, in dependency order.

**Execution order:**

1. Curie (no dependencies)
2. Tesla (reads Curie's intel)
3. Ogilvy (reads Curie's intel + Tesla's output)
4. Nightingale (reads Curie's intel + Tesla's output)
5. Ada (reads everyone's output)

**Per-agent prompt template:**

```text
You are {agent_title}.

Read these files to load your context:
1. agents/{agent}/SOUL.md
2. AGENTS.md
3. CEO.md
4. PROJECTS.md
5. projects/{project}/PROJECT.md
6. agents/{agent}/MEMORY.md

Check agents/{agent}/memory/ for recent session logs.
Check projects/{project}/outbox/{agent}/ for .feedback.md files — address those first.

Today's date is {date}. Your active project is {project}.

Run your full session workflow as defined in your SOUL.md.

When done, write your daily memory log to agents/{agent}/memory/{date}.md.
```

**Status updates:** After each agent completes, send a Telegram message:

- `"✓ Curie complete — brief written to intel/research/{date}-brief.md"`
- On failure: `"✗ Tesla failed — {error summary}"`

**Run modes:**

- `run the team` — all 5 agents in order
- `run {agent}` — single agent only
- `run {agent1} {agent2}` — specific agents in dependency order

### 2.3 Briefing Presenter

After Ada completes, read `projects/{project}/outbox/ada/ceo-briefing-{date}.md` and send it to Telegram.

**Format in Telegram:**

- Parse the briefing markdown
- Send each "Decisions Needed" item as a separate message with inline buttons
- Send the "Status Update" and "Flags" sections as a single summary message

**Inline buttons per decision item:**

```text
[✅ Approve]  [❌ Reject]  [💬 Feedback]
```

**Button behavior:**

- **Approve:** Immediately write `{filename}.approved.md` to the agent's outbox. Confirm in chat: "Item {n} approved. Routing to {agent}."
- **Reject:** Write `{filename}.feedback.md` with verdict `rejected`. Confirm in chat.
- **Feedback:** Reply with "What's your feedback on item {n}?" — wait for the CEO's next message, write it as `{filename}.feedback.md` with the CEO's exact words.

### 2.4 Conversation Handler (Ada Intelligence)

Free-text messages that aren't button callbacks go through a Claude session with Ada's context.

**Prompt template for free-text:**

```text
You are Ada, Chief of Staff.

Read: agents/ada/SOUL.md, AGENTS.md, CEO.md, PROJECTS.md

The CEO sent you this message via Telegram:
"{message}"

Scope to the current P0 project in PROJECTS.md unless the CEO names a different project.
Based on the current state of the project files, respond to the CEO.

If the CEO is:
- Asking a question: read the relevant files and answer concisely.
- Giving a command (e.g., "move X to P0"): execute it by writing to the appropriate file, then confirm.
- Giving feedback on a specific item: write the feedback file to the correct agent's outbox.

Keep responses short — this is a chat, not a document. The CEO is reading on a phone.
```

**What this handles:**

- Follow-up questions: "what did Curie find on CrewAI?" → Ada reads intel, responds
- Priority changes: "move content-engine to P0" → Ada updates PROJECTS.md, confirms
- Ad-hoc requests: "tell Tesla to focus on issue #42 tomorrow" → Ada writes a note to Tesla's outbox
- Bulk decisions: "approve 1 and 3, reject 2" → Ada parses and writes files

### 2.5 Escalation Watcher

On bot startup and every 30 minutes while running:

- Scan `projects/*/escalations/` for any files
- If found, send an alert to Telegram immediately: "🚨 Escalation from {agent}: {summary}"

---

## 3. Project Structure

```text
bot/
├── main.py              # Entry point — bot setup, polling loop
├── handlers.py          # Telegram message/callback handlers
├── runner.py            # Agent runner — spawns claude -p sessions
├── briefing.py          # Parses briefing files, formats for Telegram
├── router.py            # Writes approval/feedback/rejection files
├── ada.py               # Free-text handler — spawns Ada Claude session
├── watcher.py           # Escalation directory watcher
└── config.py            # Loads .env, constants, paths
```

**Root-level files:**

```text
.env                     # TELEGRAM_BOT_TOKEN, TELEGRAM_CEO_CHAT_ID
requirements.txt         # python-telegram-bot, python-dotenv
```

---

## 4. Message Types and Routing

| CEO Input | Bot Behavior |
| --- | --- |
| "run the team" | Spawn all 5 agents sequentially, stream status, send briefing |
| "run curie" | Spawn Curie only, stream status |
| "run curie tesla ada" | Spawn specified agents in dependency order |
| [Approve button] | Write `.approved.md`, confirm |
| [Reject button] | Write `.feedback.md` with `rejected` verdict, confirm |
| [Feedback button] → text | Write `.feedback.md` with CEO's exact words, confirm |
| Free text question | Spawn Ada Claude session, return response |
| Free text command | Spawn Ada Claude session, Ada executes and confirms |

---

## 5. File Interactions

**Bot reads:**

- `projects/{project}/outbox/ada/ceo-briefing-*.md` — to present briefings
- `projects/*/escalations/` — to watch for fire alarms
- `PROJECTS.md` — to know active projects and their slugs

**Bot writes (via router.py):**

- `projects/{project}/outbox/{agent}/{filename}.approved.md`
- `projects/{project}/outbox/{agent}/{filename}.feedback.md`

**Bot delegates writing to Ada (via ada.py → Claude session):**

- `PROJECTS.md` — priority changes
- `projects/{project}/outbox/{agent}/` — ad-hoc notes
- Any other file Ada would normally write per her SOUL.md

---

## 6. Error Handling

- **Agent fails mid-run:** Send error message to Telegram, skip to next agent, flag in summary. Don't abort the whole run.
- **Claude CLI not found:** Fail fast on startup with clear error message.
- **Bot token invalid:** Fail fast on startup.
- **Chat ID mismatch:** Silently ignore messages from non-CEO users.
- **Briefing file not found after Ada runs:** Send "Ada completed but no briefing file found — check logs."
- **Network loss:** `python-telegram-bot` handles reconnection automatically with long-polling.

---

## 7. Configuration

`.env` file:

```bash
TELEGRAM_BOT_TOKEN=your-bot-token-from-botfather
TELEGRAM_CEO_CHAT_ID=your-telegram-chat-id
INNER_CIRCLE_DIR=/path/to/inner-circle-ai
DEFAULT_PROJECT=inner-circle-mgmt
```

---

## 8. Constraints

- **No cron/scheduling** — phase 2.
- **No multi-user** — CEO only.
- **No file preview in Telegram** — detailed output reviewed locally in files.
- **No message persistence** — Telegram's own history is sufficient.
- **No web UI** — Telegram is the only interface.
- **Agent sessions are sequential** — no parallel execution in v1.

---

## 9. Success Criteria

1. CEO can trigger a full team run from Telegram with one message
2. CEO receives Ada's briefing in Telegram with approve/reject/feedback buttons
3. Approve/reject writes the correct files immediately — agents pick them up next run
4. CEO can ask Ada follow-up questions and get answers based on current file state
5. CEO can request single-agent runs
6. Escalations surface as alerts without CEO having to check a directory
7. The entire interaction — trigger to decisions routed — takes under 15 minutes of CEO time
