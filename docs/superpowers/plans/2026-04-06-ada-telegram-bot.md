# Ada Telegram Bot — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Telegram bot that IS Ada — the CEO's single point of contact for triggering agent runs, receiving briefings, and making approval decisions.

**Architecture:** Python bot using `python-telegram-bot` with long-polling. Messages route through handlers to three backends: an agent runner (spawns `claude -p` subprocesses), a file router (writes approval/feedback files), and an Ada intelligence layer (spawns Claude sessions for free-text). An escalation watcher runs on a 30-minute interval.

**Tech Stack:** Python 3.9+, `python-telegram-bot` v21+, `python-dotenv`, Claude CLI (`claude -p`)

**Spec:** `docs/superpowers/specs/2026-04-06-ada-telegram-bot-design.md`

---

## File Structure

```text
bot/
├── __init__.py          # Empty — makes bot/ a package
├── main.py              # Entry point — bot setup, polling loop, startup checks
├── config.py            # Loads .env, constants, agent definitions, paths
├── handlers.py          # Telegram command/message/callback dispatching
├── runner.py            # Agent runner — spawns claude -p sessions sequentially
├── briefing.py          # Parses briefing markdown, formats for Telegram messages
├── router.py            # Writes .approved.md / .feedback.md files to agent outboxes
├── ada.py               # Free-text handler — spawns Ada Claude session for questions/commands
├── watcher.py           # Escalation directory watcher on interval

tests/
├── __init__.py
├── test_config.py       # Config loading, path resolution
├── test_runner.py       # Agent runner command building, ordering
├── test_briefing.py     # Briefing parsing and formatting
├── test_router.py       # Approval/feedback file writing
├── test_handlers.py     # Message routing, auth check

.env.example             # Template with placeholder values
requirements.txt         # Dependencies
```

---

### Task 1: Project Setup and Configuration

**Files:**

- Create: `bot/__init__.py`
- Create: `bot/config.py`
- Create: `requirements.txt`
- Create: `.env.example`
- Create: `tests/__init__.py`
- Create: `tests/test_config.py`

- [ ] **Step 1: Create requirements.txt**

```text
python-telegram-bot>=21.0
python-dotenv>=1.0.0
```

- [ ] **Step 2: Create .env.example**

```bash
TELEGRAM_BOT_TOKEN=your-bot-token-from-botfather
TELEGRAM_CEO_CHAT_ID=your-telegram-chat-id
DEFAULT_PROJECT=inner-circle-mgmt
```

- [ ] **Step 3: Install dependencies**

Run: `pip3 install -r requirements.txt`

- [ ] **Step 4: Create bot/__init__.py**

```python
# Empty — makes bot/ a package
```

- [ ] **Step 5: Create tests/__init__.py**

```python
# Empty — makes tests/ a package
```

- [ ] **Step 6: Write failing test for config**

Create `tests/test_config.py`:

```python
import os
import pytest
from unittest.mock import patch


def test_load_config_from_env():
    env = {
        "TELEGRAM_BOT_TOKEN": "test-token-123",
        "TELEGRAM_CEO_CHAT_ID": "99999",
        "DEFAULT_PROJECT": "my-project",
    }
    with patch.dict(os.environ, env, clear=False):
        from bot.config import load_config

        cfg = load_config()
        assert cfg.bot_token == "test-token-123"
        assert cfg.ceo_chat_id == 99999
        assert cfg.default_project == "my-project"


def test_load_config_defaults():
    env = {
        "TELEGRAM_BOT_TOKEN": "test-token-123",
        "TELEGRAM_CEO_CHAT_ID": "99999",
    }
    with patch.dict(os.environ, env, clear=False):
        # Remove DEFAULT_PROJECT if set
        os.environ.pop("DEFAULT_PROJECT", None)
        from importlib import reload
        import bot.config

        reload(bot.config)
        cfg = bot.config.load_config()
        assert cfg.default_project == "inner-circle-mgmt"


def test_load_config_missing_token():
    env = {"TELEGRAM_CEO_CHAT_ID": "99999"}
    with patch.dict(os.environ, env, clear=True):
        os.environ.pop("TELEGRAM_BOT_TOKEN", None)
        from importlib import reload
        import bot.config

        reload(bot.config)
        with pytest.raises(ValueError, match="TELEGRAM_BOT_TOKEN"):
            bot.config.load_config()


def test_load_config_missing_chat_id():
    env = {"TELEGRAM_BOT_TOKEN": "test-token"}
    with patch.dict(os.environ, env, clear=True):
        os.environ.pop("TELEGRAM_CEO_CHAT_ID", None)
        from importlib import reload
        import bot.config

        reload(bot.config)
        with pytest.raises(ValueError, match="TELEGRAM_CEO_CHAT_ID"):
            bot.config.load_config()


def test_agent_definitions():
    from bot.config import AGENTS, AGENT_ORDER

    assert len(AGENTS) == 5
    assert AGENT_ORDER == ["curie", "tesla", "ogilvy", "nightingale", "ada"]
    assert AGENTS["ada"]["title"] == "Ada, Chief of Staff"
    assert AGENTS["curie"]["title"] == "Curie, Head of Research"


def test_project_paths(tmp_path):
    from bot.config import project_paths

    paths = project_paths("inner-circle-mgmt", base_dir=str(tmp_path))
    assert paths["project_dir"] == str(tmp_path / "projects" / "inner-circle-mgmt")
    assert paths["outbox_ada"] == str(
        tmp_path / "projects" / "inner-circle-mgmt" / "outbox" / "ada"
    )
    assert paths["escalations"] == str(
        tmp_path / "projects" / "inner-circle-mgmt" / "escalations"
    )
```

- [ ] **Step 7: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_config.py -v`

Expected: FAIL — `ModuleNotFoundError: No module named 'bot.config'`

- [ ] **Step 8: Implement config.py**

Create `bot/config.py`:

```python
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

AGENT_ORDER = ["curie", "tesla", "ogilvy", "nightingale", "ada"]

AGENTS = {
    "curie": {"title": "Curie, Head of Research"},
    "tesla": {"title": "Tesla, Head of Engineering"},
    "ogilvy": {"title": "Ogilvy, Head of Growth"},
    "nightingale": {"title": "Nightingale, Head of Operations"},
    "ada": {"title": "Ada, Chief of Staff"},
}


@dataclass
class Config:
    bot_token: str
    ceo_chat_id: int
    default_project: str
    base_dir: str


def load_config() -> Config:
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN is required")

    chat_id = os.environ.get("TELEGRAM_CEO_CHAT_ID")
    if not chat_id:
        raise ValueError("TELEGRAM_CEO_CHAT_ID is required")

    return Config(
        bot_token=bot_token,
        ceo_chat_id=int(chat_id),
        default_project=os.environ.get("DEFAULT_PROJECT", "inner-circle-mgmt"),
        base_dir=os.environ.get("INNER_CIRCLE_DIR", str(Path.cwd())),
    )


def project_paths(project_slug: str, base_dir: str = None) -> dict:
    base = Path(base_dir) if base_dir else Path.cwd()
    project_dir = base / "projects" / project_slug
    return {
        "project_dir": str(project_dir),
        "outbox_ada": str(project_dir / "outbox" / "ada"),
        "escalations": str(project_dir / "escalations"),
    }
```

- [ ] **Step 9: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_config.py -v`

Expected: All 6 tests PASS

- [ ] **Step 10: Commit**

```bash
git add bot/__init__.py bot/config.py tests/__init__.py tests/test_config.py requirements.txt .env.example
git commit -m "feat(bot): add config module with env loading and agent definitions"
```

---

### Task 2: Agent Runner

**Files:**

- Create: `bot/runner.py`
- Create: `tests/test_runner.py`

- [ ] **Step 1: Write failing tests for runner**

Create `tests/test_runner.py`:

```python
import pytest
from bot.runner import build_agent_prompt, resolve_run_order


def test_build_agent_prompt():
    prompt = build_agent_prompt(
        agent="curie",
        agent_title="Curie, Head of Research",
        project="inner-circle-mgmt",
        date="2026-04-06",
    )
    assert "You are Curie, Head of Research." in prompt
    assert "agents/curie/SOUL.md" in prompt
    assert "AGENTS.md" in prompt
    assert "CEO.md" in prompt
    assert "PROJECTS.md" in prompt
    assert "projects/inner-circle-mgmt/PROJECT.md" in prompt
    assert "agents/curie/MEMORY.md" in prompt
    assert "2026-04-06" in prompt
    assert "inner-circle-mgmt" in prompt
    assert ".feedback.md" in prompt


def test_resolve_run_order_full_team():
    order = resolve_run_order(["all"])
    assert order == ["curie", "tesla", "ogilvy", "nightingale", "ada"]


def test_resolve_run_order_single():
    order = resolve_run_order(["curie"])
    assert order == ["curie"]


def test_resolve_run_order_multiple_respects_dependency():
    order = resolve_run_order(["ada", "curie", "tesla"])
    assert order == ["curie", "tesla", "ada"]


def test_resolve_run_order_invalid_agent():
    with pytest.raises(ValueError, match="Unknown agent"):
        resolve_run_order(["curie", "unknown"])
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_runner.py -v`

Expected: FAIL — `ModuleNotFoundError: No module named 'bot.runner'`

- [ ] **Step 3: Implement runner.py**

Create `bot/runner.py`:

```python
import asyncio
import subprocess
from datetime import date
from typing import Callable

from bot.config import AGENTS, AGENT_ORDER


def build_agent_prompt(
    agent: str, agent_title: str, project: str, date: str
) -> str:
    return f"""You are {agent_title}.

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

When done, write your daily memory log to agents/{agent}/memory/{date}.md."""


def resolve_run_order(requested: list[str]) -> list[str]:
    if "all" in requested or "team" in requested:
        return list(AGENT_ORDER)

    for agent in requested:
        if agent not in AGENTS:
            raise ValueError(f"Unknown agent: {agent}")

    return [a for a in AGENT_ORDER if a in requested]


async def run_agents(
    agents: list[str],
    project: str,
    base_dir: str,
    on_status: Callable = None,
):
    today = date.today().isoformat()
    results = []

    for agent in agents:
        title = AGENTS[agent]["title"]
        prompt = build_agent_prompt(agent, title, project, today)

        if on_status:
            await on_status(f"Running {title}...")

        try:
            proc = await asyncio.create_subprocess_exec(
                "claude", "-p", prompt, "--output-format", "text",
                cwd=base_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()

            if proc.returncode == 0:
                msg = f"✓ {title} complete"
                results.append({"agent": agent, "ok": True, "msg": msg})
            else:
                err = stderr.decode().strip()[:200]
                msg = f"✗ {title} failed — {err}"
                results.append({"agent": agent, "ok": False, "msg": msg})
        except FileNotFoundError:
            msg = f"✗ {title} failed — claude CLI not found"
            results.append({"agent": agent, "ok": False, "msg": msg})

        if on_status:
            await on_status(results[-1]["msg"])

    return results
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_runner.py -v`

Expected: All 5 tests PASS

- [ ] **Step 5: Commit**

```bash
git add bot/runner.py tests/test_runner.py
git commit -m "feat(bot): add agent runner with prompt builder and dependency ordering"
```

---

### Task 3: Briefing Parser

**Files:**

- Create: `bot/briefing.py`
- Create: `tests/test_briefing.py`

- [ ] **Step 1: Write failing tests for briefing parser**

Create `tests/test_briefing.py`:

```python
import pytest
from bot.briefing import parse_briefing, BriefingItem


SAMPLE_BRIEFING = """---
agent: ada
type: briefing
project: inner-circle-mgmt
priority: P0
created: 2026-04-06
status: pending-review
---

# CEO Briefing — 2026-04-06

## Decisions Needed (3 items)

### 1. [URGENT] Release Notes v0.2.0 — from Ogilvy
**Bottom line:** Draft ready for the SOUL.md restructuring release.
**Ada's recommendation:** Approve — clear, user-focused, matches our voice.
**File:** `outbox/ogilvy/release-notes-v0.2.0.md`

### 2. Issue Triage Report — from Tesla
**Bottom line:** 4 new issues, 2 bugs (P1), 1 feature request (P2), 1 question.
**Ada's recommendation:** Approve triage. Assign bugs to Tesla for next session.
**File:** `outbox/tesla/triage-2026-04-06.md`

### 3. Competitor Brief — from Curie
**Bottom line:** CrewAI shipped v0.5 with memory support. Relevant to our positioning.
**Ada's recommendation:** Approve brief. Flag for Ogilvy to draft a comparison post.
**File:** `outbox/curie/competitor-update-2026-04-06.md`

## Status Update
- Curie: Delivered daily intel brief. Tracking 6 competitor frameworks.
- Tesla: Reviewed 2 PRs, triaged 4 issues.
- Ogilvy: Drafted release notes for v0.2.0.
- Nightingale: Updated GETTING-STARTED.md with new session workflow.

## Flags
- No flags today.
"""


def test_parse_briefing_items():
    result = parse_briefing(SAMPLE_BRIEFING)
    assert len(result.items) == 3


def test_parse_briefing_item_fields():
    result = parse_briefing(SAMPLE_BRIEFING)
    item = result.items[0]
    assert item.number == 1
    assert item.title == "[URGENT] Release Notes v0.2.0 — from Ogilvy"
    assert "SOUL.md restructuring" in item.bottom_line
    assert "Approve" in item.recommendation
    assert item.file_path == "outbox/ogilvy/release-notes-v0.2.0.md"
    assert item.agent == "ogilvy"


def test_parse_briefing_extracts_agent_from_title():
    result = parse_briefing(SAMPLE_BRIEFING)
    assert result.items[0].agent == "ogilvy"
    assert result.items[1].agent == "tesla"
    assert result.items[2].agent == "curie"


def test_parse_briefing_summary():
    result = parse_briefing(SAMPLE_BRIEFING)
    assert "Curie: Delivered daily intel" in result.summary
    assert "No flags today" in result.summary


def test_parse_briefing_date():
    result = parse_briefing(SAMPLE_BRIEFING)
    assert result.date == "2026-04-06"


def test_format_item_for_telegram():
    result = parse_briefing(SAMPLE_BRIEFING)
    item = result.items[0]
    text = item.format_telegram()
    assert "Release Notes v0.2.0" in text
    assert "Bottom line:" in text
    assert "Recommendation:" in text
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_briefing.py -v`

Expected: FAIL — `ModuleNotFoundError: No module named 'bot.briefing'`

- [ ] **Step 3: Implement briefing.py**

Create `bot/briefing.py`:

```python
import re
from dataclasses import dataclass, field


@dataclass
class BriefingItem:
    number: int
    title: str
    bottom_line: str
    recommendation: str
    file_path: str
    agent: str

    def format_telegram(self) -> str:
        urgent = "🚨 " if "[URGENT]" in self.title else ""
        return (
            f"{urgent}*Item {self.number}: {self._escape(self.title)}*\n\n"
            f"*Bottom line:* {self._escape(self.bottom_line)}\n"
            f"*Recommendation:* {self._escape(self.recommendation)}\n"
            f"📁 `{self.file_path}`"
        )

    @staticmethod
    def _escape(text: str) -> str:
        # Escape markdown v1 special chars for Telegram
        for char in ["_", "[", "]", "(", ")", "~", ">", "#", "+", "-", "=", "|", "{", "}", ".", "!"]:
            text = text.replace(char, f"\\{char}")
        return text


@dataclass
class Briefing:
    date: str
    items: list[BriefingItem] = field(default_factory=list)
    summary: str = ""


def parse_briefing(content: str) -> Briefing:
    # Extract date from heading
    date_match = re.search(r"# CEO Briefing — (\d{4}-\d{2}-\d{2})", content)
    date = date_match.group(1) if date_match else ""

    # Extract decision items
    item_pattern = re.compile(
        r"### (\d+)\. (.+)\n"
        r"\*\*Bottom line:\*\* (.+)\n"
        r"\*\*Ada's recommendation:\*\* (.+)\n"
        r"\*\*File:\*\* `(.+?)`",
        re.MULTILINE,
    )

    items = []
    for match in item_pattern.finditer(content):
        number = int(match.group(1))
        title = match.group(2).strip()
        bottom_line = match.group(3).strip()
        recommendation = match.group(4).strip()
        file_path = match.group(5).strip()

        # Extract agent name from file path (outbox/{agent}/...)
        agent_match = re.search(r"outbox/(\w+)/", file_path)
        agent = agent_match.group(1) if agent_match else ""

        items.append(BriefingItem(
            number=number,
            title=title,
            bottom_line=bottom_line,
            recommendation=recommendation,
            file_path=file_path,
            agent=agent,
        ))

    # Extract summary (Status Update + Flags sections)
    summary = ""
    status_match = re.search(
        r"## Status Update\n(.*?)(?=\n## |\Z)", content, re.DOTALL
    )
    if status_match:
        summary += status_match.group(1).strip()

    flags_match = re.search(
        r"## Flags\n(.*?)(?=\n## |\Z)", content, re.DOTALL
    )
    if flags_match:
        summary += "\n\n" + flags_match.group(1).strip()

    return Briefing(date=date, items=items, summary=summary.strip())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_briefing.py -v`

Expected: All 6 tests PASS

- [ ] **Step 5: Commit**

```bash
git add bot/briefing.py tests/test_briefing.py
git commit -m "feat(bot): add briefing parser with markdown extraction and telegram formatting"
```

---

### Task 4: File Router (Approvals and Feedback)

**Files:**

- Create: `bot/router.py`
- Create: `tests/test_router.py`

- [ ] **Step 1: Write failing tests for router**

Create `tests/test_router.py`:

```python
import os
import pytest
from bot.router import write_approval, write_feedback, write_rejection


def test_write_approval(tmp_path):
    outbox = tmp_path / "projects" / "test" / "outbox" / "ogilvy"
    outbox.mkdir(parents=True)

    write_approval(
        base_dir=str(tmp_path),
        project="test",
        agent="ogilvy",
        filename="release-notes-v0.2.0.md",
    )

    approved = outbox / "release-notes-v0.2.0.approved.md"
    assert approved.exists()
    content = approved.read_text()
    assert "verdict: approved" in content
    assert "ogilvy" in content


def test_write_feedback(tmp_path):
    outbox = tmp_path / "projects" / "test" / "outbox" / "tesla"
    outbox.mkdir(parents=True)

    write_feedback(
        base_dir=str(tmp_path),
        project="test",
        agent="tesla",
        filename="triage-2026-04-06.md",
        feedback="Too formal, make it conversational.",
    )

    fb = outbox / "triage-2026-04-06.feedback.md"
    assert fb.exists()
    content = fb.read_text()
    assert "verdict: revise" in content
    assert "Too formal, make it conversational." in content


def test_write_rejection(tmp_path):
    outbox = tmp_path / "projects" / "test" / "outbox" / "curie"
    outbox.mkdir(parents=True)

    write_rejection(
        base_dir=str(tmp_path),
        project="test",
        agent="curie",
        filename="competitor-update.md",
    )

    fb = outbox / "competitor-update.feedback.md"
    assert fb.exists()
    content = fb.read_text()
    assert "verdict: rejected" in content


def test_write_approval_extracts_filename_from_path(tmp_path):
    outbox = tmp_path / "projects" / "test" / "outbox" / "ogilvy"
    outbox.mkdir(parents=True)

    # Should handle full path like "outbox/ogilvy/release-notes.md"
    write_approval(
        base_dir=str(tmp_path),
        project="test",
        agent="ogilvy",
        filename="outbox/ogilvy/release-notes.md",
    )

    approved = outbox / "release-notes.approved.md"
    assert approved.exists()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_router.py -v`

Expected: FAIL — `ModuleNotFoundError: No module named 'bot.router'`

- [ ] **Step 3: Implement router.py**

Create `bot/router.py`:

```python
from datetime import date
from pathlib import Path


def _resolve_filename(filename: str) -> str:
    """Extract just the filename if a full path like outbox/agent/file.md is given."""
    return Path(filename).name


def _stem(filename: str) -> str:
    """Get filename without .md extension."""
    name = _resolve_filename(filename)
    if name.endswith(".md"):
        return name[:-3]
    return name


def write_approval(base_dir: str, project: str, agent: str, filename: str):
    stem = _stem(filename)
    outbox = Path(base_dir) / "projects" / project / "outbox" / agent
    outbox.mkdir(parents=True, exist_ok=True)

    path = outbox / f"{stem}.approved.md"
    today = date.today().isoformat()

    path.write_text(
        f"---\n"
        f"from: ceo\n"
        f"re: {_resolve_filename(filename)}\n"
        f"date: {today}\n"
        f"verdict: approved\n"
        f"agent: {agent}\n"
        f"---\n\n"
        f"Approved by CEO.\n"
    )


def write_feedback(
    base_dir: str, project: str, agent: str, filename: str, feedback: str
):
    stem = _stem(filename)
    outbox = Path(base_dir) / "projects" / project / "outbox" / agent
    outbox.mkdir(parents=True, exist_ok=True)

    path = outbox / f"{stem}.feedback.md"
    today = date.today().isoformat()

    path.write_text(
        f"---\n"
        f"from: ceo\n"
        f"re: {_resolve_filename(filename)}\n"
        f"date: {today}\n"
        f"verdict: revise\n"
        f"agent: {agent}\n"
        f"---\n\n"
        f"## Feedback\n\n"
        f"{feedback}\n"
    )


def write_rejection(base_dir: str, project: str, agent: str, filename: str):
    stem = _stem(filename)
    outbox = Path(base_dir) / "projects" / project / "outbox" / agent
    outbox.mkdir(parents=True, exist_ok=True)

    path = outbox / f"{stem}.feedback.md"
    today = date.today().isoformat()

    path.write_text(
        f"---\n"
        f"from: ceo\n"
        f"re: {_resolve_filename(filename)}\n"
        f"date: {today}\n"
        f"verdict: rejected\n"
        f"agent: {agent}\n"
        f"---\n\n"
        f"Rejected by CEO.\n"
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_router.py -v`

Expected: All 4 tests PASS

- [ ] **Step 5: Commit**

```bash
git add bot/router.py tests/test_router.py
git commit -m "feat(bot): add file router for approval/feedback/rejection writing"
```

---

### Task 5: Escalation Watcher

**Files:**

- Create: `bot/watcher.py`
- Create: `tests/test_watcher.py`

- [ ] **Step 1: Write failing tests for watcher**

Create `tests/test_watcher.py`:

```python
import pytest
from bot.watcher import scan_escalations


def test_scan_escalations_empty(tmp_path):
    esc = tmp_path / "projects" / "test" / "escalations"
    esc.mkdir(parents=True)
    (esc / ".gitkeep").touch()

    result = scan_escalations(str(tmp_path), ["test"])
    assert result == []


def test_scan_escalations_finds_files(tmp_path):
    esc = tmp_path / "projects" / "test" / "escalations"
    esc.mkdir(parents=True)
    (esc / "tesla-escalation-2026-04-06.md").write_text(
        "---\nagent: tesla\nstuck-item: outbox/tesla/pr-review-142.md\n---\n\n"
        "## What's Stuck\nPR #142 review waiting 3 days.\n"
    )

    result = scan_escalations(str(tmp_path), ["test"])
    assert len(result) == 1
    assert result[0]["agent"] == "tesla"
    assert result[0]["project"] == "test"
    assert "PR #142" in result[0]["summary"]


def test_scan_escalations_multiple_projects(tmp_path):
    for proj in ["proj-a", "proj-b"]:
        esc = tmp_path / "projects" / proj / "escalations"
        esc.mkdir(parents=True)
    (tmp_path / "projects" / "proj-a" / "escalations" / "curie-escalation.md").write_text(
        "---\nagent: curie\n---\n\n## What's Stuck\nIntel stale.\n"
    )

    result = scan_escalations(str(tmp_path), ["proj-a", "proj-b"])
    assert len(result) == 1
    assert result[0]["project"] == "proj-a"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_watcher.py -v`

Expected: FAIL — `ModuleNotFoundError: No module named 'bot.watcher'`

- [ ] **Step 3: Implement watcher.py**

Create `bot/watcher.py`:

```python
import re
from pathlib import Path


def scan_escalations(base_dir: str, projects: list[str]) -> list[dict]:
    results = []
    base = Path(base_dir)

    for project in projects:
        esc_dir = base / "projects" / project / "escalations"
        if not esc_dir.exists():
            continue

        for f in esc_dir.iterdir():
            if f.name == ".gitkeep" or not f.suffix == ".md":
                continue

            content = f.read_text()

            # Extract agent from frontmatter
            agent_match = re.search(r"^agent:\s*(\w+)", content, re.MULTILINE)
            agent = agent_match.group(1) if agent_match else "unknown"

            # Extract summary from "What's Stuck" section
            stuck_match = re.search(
                r"## What's Stuck\n(.+?)(?=\n## |\Z)", content, re.DOTALL
            )
            summary = stuck_match.group(1).strip() if stuck_match else f.name

            results.append({
                "agent": agent,
                "project": project,
                "file": str(f),
                "summary": summary,
            })

    return results
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_watcher.py -v`

Expected: All 3 tests PASS

- [ ] **Step 5: Commit**

```bash
git add bot/watcher.py tests/test_watcher.py
git commit -m "feat(bot): add escalation watcher scanning project directories"
```

---

### Task 6: Ada Intelligence (Free-text Handler)

**Files:**

- Create: `bot/ada.py`
- Create: `tests/test_ada.py`

- [ ] **Step 1: Write failing tests for ada**

Create `tests/test_ada.py`:

```python
import pytest
from bot.ada import build_ada_prompt


def test_build_ada_prompt():
    prompt = build_ada_prompt(
        message="what did Curie find on CrewAI?",
        project="inner-circle-mgmt",
    )
    assert "You are Ada, Chief of Staff." in prompt
    assert "agents/ada/SOUL.md" in prompt
    assert "AGENTS.md" in prompt
    assert "CEO.md" in prompt
    assert "what did Curie find on CrewAI?" in prompt
    assert "inner-circle-mgmt" in prompt
    assert "reading on a phone" in prompt


def test_build_ada_prompt_includes_project_scoping():
    prompt = build_ada_prompt(
        message="move content-engine to P0",
        project="inner-circle-mgmt",
    )
    assert "Scope to" in prompt or "inner-circle-mgmt" in prompt
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_ada.py -v`

Expected: FAIL — `ModuleNotFoundError: No module named 'bot.ada'`

- [ ] **Step 3: Implement ada.py**

Create `bot/ada.py`:

```python
import asyncio
import subprocess


def build_ada_prompt(message: str, project: str) -> str:
    return f"""You are Ada, Chief of Staff.

Read: agents/ada/SOUL.md, AGENTS.md, CEO.md, PROJECTS.md

The CEO sent you this message via Telegram:
"{message}"

Scope to the project "{project}" unless the CEO names a different project.
Based on the current state of the project files, respond to the CEO.

If the CEO is:
- Asking a question: read the relevant files and answer concisely.
- Giving a command (e.g., "move X to P0"): execute it by writing to the appropriate file, then confirm.
- Giving feedback on a specific item: write the feedback file to the correct agent's outbox.

Keep responses short — this is a chat, not a document. The CEO is reading on a phone."""


async def ask_ada(message: str, project: str, base_dir: str) -> str:
    prompt = build_ada_prompt(message, project)

    try:
        proc = await asyncio.create_subprocess_exec(
            "claude", "-p", prompt, "--output-format", "text",
            cwd=base_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

        if proc.returncode == 0:
            return stdout.decode().strip()
        else:
            return f"Ada encountered an error: {stderr.decode().strip()[:200]}"
    except FileNotFoundError:
        return "Error: claude CLI not found. Make sure it's installed and in PATH."
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_ada.py -v`

Expected: All 2 tests PASS

- [ ] **Step 5: Commit**

```bash
git add bot/ada.py tests/test_ada.py
git commit -m "feat(bot): add Ada intelligence layer with prompt builder and Claude session"
```

---

### Task 7: Telegram Handlers

**Files:**

- Create: `bot/handlers.py`
- Create: `tests/test_handlers.py`

- [ ] **Step 1: Write failing tests for handlers**

Create `tests/test_handlers.py`:

```python
import pytest
from bot.handlers import parse_run_command, is_run_command


def test_is_run_command():
    assert is_run_command("run the team") is True
    assert is_run_command("Run the team") is True
    assert is_run_command("run curie") is True
    assert is_run_command("run curie tesla ada") is True
    assert is_run_command("what did curie find?") is False
    assert is_run_command("approve item 1") is False


def test_parse_run_command_full_team():
    agents = parse_run_command("run the team")
    assert agents == ["all"]


def test_parse_run_command_single():
    agents = parse_run_command("run curie")
    assert agents == ["curie"]


def test_parse_run_command_multiple():
    agents = parse_run_command("run curie tesla ada")
    assert agents == ["curie", "tesla", "ada"]


def test_parse_run_command_case_insensitive():
    agents = parse_run_command("Run Curie Tesla")
    assert agents == ["curie", "tesla"]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_handlers.py -v`

Expected: FAIL — `ModuleNotFoundError: No module named 'bot.handlers'`

- [ ] **Step 3: Implement handlers.py**

Create `bot/handlers.py`:

```python
import json
import logging
from pathlib import Path

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from bot.ada import ask_ada
from bot.briefing import parse_briefing
from bot.config import Config, project_paths
from bot.router import write_approval, write_feedback, write_rejection
from bot.runner import resolve_run_order, run_agents
from bot.watcher import scan_escalations

logger = logging.getLogger(__name__)


def is_run_command(text: str) -> bool:
    return text.strip().lower().startswith("run ")


def parse_run_command(text: str) -> list[str]:
    lower = text.strip().lower()
    parts = lower.split()
    # "run the team" or "run team"
    if "team" in parts:
        return ["all"]
    # "run curie tesla ada"
    return [p for p in parts[1:] if p != "the"]


def _auth_check(update: Update, cfg: Config) -> bool:
    return update.effective_chat.id == cfg.ceo_chat_id


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cfg: Config = context.bot_data["config"]

    if not _auth_check(update, cfg):
        return

    text = update.message.text.strip()

    # Check if waiting for feedback text
    if "awaiting_feedback" in context.user_data:
        item_data = context.user_data.pop("awaiting_feedback")
        write_feedback(
            base_dir=cfg.base_dir,
            project=item_data["project"],
            agent=item_data["agent"],
            filename=item_data["filename"],
            feedback=text,
        )
        await update.message.reply_text(
            f"Feedback routed to {item_data['agent'].capitalize()}."
        )
        return

    # Run command
    if is_run_command(text):
        requested = parse_run_command(text)
        try:
            agents = resolve_run_order(requested)
        except ValueError as e:
            await update.message.reply_text(str(e))
            return

        project = cfg.default_project

        async def on_status(msg):
            await update.message.reply_text(msg)

        await update.message.reply_text(
            f"Running agents for {project}..."
        )

        results = await run_agents(agents, project, cfg.base_dir, on_status)

        # If ada was in the run, send the briefing
        if "ada" in agents:
            await _send_briefing(update, cfg, project)

        return

    # Free text — ask Ada
    response = await ask_ada(text, cfg.default_project, cfg.base_dir)
    await update.message.reply_text(response)


async def _send_briefing(update: Update, cfg: Config, project: str):
    from datetime import date

    paths = project_paths(project, cfg.base_dir)
    ada_outbox = Path(paths["outbox_ada"])
    today = date.today().isoformat()
    briefing_file = ada_outbox / f"ceo-briefing-{today}.md"

    if not briefing_file.exists():
        await update.message.reply_text(
            "Ada completed but no briefing file found — check logs."
        )
        return

    content = briefing_file.read_text()
    briefing = parse_briefing(content)

    # Send summary
    if briefing.summary:
        await update.message.reply_text(f"📋 *Status & Flags*\n\n{briefing.summary}", parse_mode=None)

    # Send each item with buttons
    for item in briefing.items:
        callback_data = json.dumps({
            "project": project,
            "agent": item.agent,
            "filename": item.file_path,
            "number": item.number,
        })
        # Telegram callback_data max is 64 bytes — use item number as key
        # and store full data in bot_data
        item_key = f"item_{briefing.date}_{item.number}"
        update.message.chat  # ensure chat context

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve:{item_key}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject:{item_key}"),
                InlineKeyboardButton("💬 Feedback", callback_data=f"feedback:{item_key}"),
            ]
        ])

        # Store item metadata for callback lookup
        if "briefing_items" not in update.message._bot._bot_data:
            update.message._bot._bot_data["briefing_items"] = {}
        update.message._bot._bot_data["briefing_items"][item_key] = {
            "project": project,
            "agent": item.agent,
            "filename": item.file_path,
            "title": item.title,
        }

        await update.message.reply_text(
            item.format_telegram(),
            reply_markup=keyboard,
            parse_mode=None,
        )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cfg: Config = context.bot_data["config"]
    query = update.callback_query
    await query.answer()

    if not query.from_user or query.message.chat.id != cfg.ceo_chat_id:
        return

    data = query.data  # e.g. "approve:item_2026-04-06_1"
    action, item_key = data.split(":", 1)

    items = context.bot_data.get("briefing_items", {})
    item_data = items.get(item_key)

    if not item_data:
        await query.edit_message_reply_markup(reply_markup=None)
        await query.message.reply_text("Item not found — briefing may have expired.")
        return

    if action == "approve":
        write_approval(
            base_dir=cfg.base_dir,
            project=item_data["project"],
            agent=item_data["agent"],
            filename=item_data["filename"],
        )
        await query.edit_message_reply_markup(reply_markup=None)
        await query.message.reply_text(
            f"✅ Item approved. Routing to {item_data['agent'].capitalize()}."
        )

    elif action == "reject":
        write_rejection(
            base_dir=cfg.base_dir,
            project=item_data["project"],
            agent=item_data["agent"],
            filename=item_data["filename"],
        )
        await query.edit_message_reply_markup(reply_markup=None)
        await query.message.reply_text(
            f"❌ Item rejected. Routed to {item_data['agent'].capitalize()}."
        )

    elif action == "feedback":
        context.user_data["awaiting_feedback"] = item_data
        await query.edit_message_reply_markup(reply_markup=None)
        await query.message.reply_text(
            f"💬 What's your feedback on: *{item_data['title']}*?",
            parse_mode=None,
        )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_handlers.py -v`

Expected: All 5 tests PASS

- [ ] **Step 5: Commit**

```bash
git add bot/handlers.py tests/test_handlers.py
git commit -m "feat(bot): add Telegram handlers with run commands, briefing display, and callbacks"
```

---

### Task 8: Main Entry Point

**Files:**

- Create: `bot/main.py`

- [ ] **Step 1: Implement main.py**

Create `bot/main.py`:

```python
import asyncio
import logging
import shutil
import sys

from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from bot.config import load_config, project_paths
from bot.handlers import handle_message, handle_callback
from bot.watcher import scan_escalations

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def check_escalations(context):
    """Periodic job to scan for escalations."""
    cfg = context.bot_data["config"]
    # Get active projects from PROJECTS.md (simplified — just use default for now)
    projects = [cfg.default_project]

    escalations = scan_escalations(cfg.base_dir, projects)
    for esc in escalations:
        await context.bot.send_message(
            chat_id=cfg.ceo_chat_id,
            text=(
                f"🚨 *Escalation from {esc['agent'].capitalize()}*\n"
                f"Project: {esc['project']}\n\n"
                f"{esc['summary']}"
            ),
            parse_mode=None,
        )


def main():
    # Preflight checks
    if not shutil.which("claude"):
        print("Error: claude CLI not found in PATH. Install it first.")
        sys.exit(1)

    try:
        cfg = load_config()
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    logger.info("Starting Ada Telegram Bot...")
    logger.info(f"Project: {cfg.default_project}")
    logger.info(f"Base dir: {cfg.base_dir}")

    app = ApplicationBuilder().token(cfg.bot_token).build()

    # Store config in bot_data for handlers
    app.bot_data["config"] = cfg
    app.bot_data["briefing_items"] = {}

    # Register handlers
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Schedule escalation watcher every 30 minutes
    app.job_queue.run_repeating(
        check_escalations, interval=1800, first=10
    )

    # Run initial escalation check
    logger.info("Bot ready. Polling for messages...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Verify the bot starts (smoke test)**

Create a `.env` file with your actual bot token and chat ID, then:

Run: `python3 -m bot.main`

Expected: Bot starts, logs "Bot ready. Polling for messages..." — Ctrl+C to stop.

- [ ] **Step 3: Commit**

```bash
git add bot/main.py
git commit -m "feat(bot): add main entry point with polling, escalation watcher, and handler registration"
```

---

### Task 9: End-to-End Manual Testing

- [ ] **Step 1: Set up .env with real credentials**

1. Create a bot via BotFather in Telegram — save the token
2. Get your chat ID (message @userinfobot in Telegram)
3. Create `.env`:

```bash
TELEGRAM_BOT_TOKEN=<your-token>
TELEGRAM_CEO_CHAT_ID=<your-chat-id>
DEFAULT_PROJECT=inner-circle-mgmt
```

- [ ] **Step 2: Start the bot**

Run: `python3 -m bot.main`

- [ ] **Step 3: Test "run the team"**

Send in Telegram: `run the team`

Expected: Status messages appear as each agent runs, then Ada's briefing with inline buttons.

- [ ] **Step 4: Test approve/reject/feedback buttons**

- Tap "Approve" on one item → should confirm and write `.approved.md`
- Tap "Reject" on one item → should confirm and write `.feedback.md` with rejected verdict
- Tap "Feedback" on one item → bot asks for text → send feedback → should write `.feedback.md`

Verify files exist:

Run: `find projects/inner-circle-mgmt/outbox -name "*.approved.md" -o -name "*.feedback.md"`

- [ ] **Step 5: Test single agent run**

Send in Telegram: `run curie`

Expected: Only Curie runs, status message sent.

- [ ] **Step 6: Test free-text question**

Send in Telegram: `what did Curie find today?`

Expected: Ada responds with information from the latest intel brief.

- [ ] **Step 7: Test free-text command**

Send in Telegram: `move inner-circle-mgmt to P1`

Expected: Ada confirms the priority change, PROJECTS.md updated.

- [ ] **Step 8: Run full test suite**

Run: `python3 -m pytest tests/ -v`

Expected: All tests PASS.

- [ ] **Step 9: Commit any fixes from testing**

```bash
git add -A
git commit -m "test: end-to-end manual testing complete, fixes applied"
```

---

### Task 10: Update .gitignore and Documentation

**Files:**

- Modify: `.gitignore`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Update .gitignore**

Add to `.gitignore`:

```text
# Bot
.env
__pycache__/
*.pyc
```

- [ ] **Step 2: Update CLAUDE.md with bot context**

Add a section to `CLAUDE.md`:

```markdown
## Telegram Bot

- The bot lives in `bot/` — Python, using `python-telegram-bot`
- Run with `python3 -m bot.main`
- Config via `.env` (see `.env.example`)
- The bot IS Ada's Telegram interface — it reads/writes the same files the framework uses
- Agent runs are triggered via `claude -p` subprocesses, one per agent
- Tests in `tests/` — run with `python3 -m pytest tests/ -v`
```

- [ ] **Step 3: Commit**

```bash
git add .gitignore CLAUDE.md
git commit -m "docs: update gitignore and CLAUDE.md for telegram bot"
```
