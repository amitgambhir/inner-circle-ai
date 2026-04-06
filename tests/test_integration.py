"""End-to-end integration test: briefing file → parse → buttons → approval/feedback files."""

import pytest
from datetime import date
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

from bot.briefing import parse_briefing
from bot.config import Config
from bot.handlers import handle_callback
from bot.router import write_approval, write_feedback, write_rejection


SAMPLE_BRIEFING = """---
agent: ada
type: briefing
project: test-proj
priority: P0
created: {date}
status: pending-review
---

# CEO Briefing — {date}

## Decisions Needed (2 items)

### 1. [URGENT] Release Notes v0.2.0 — from Ogilvy
**Bottom line:** Draft ready for review.
**Ada's recommendation:** Approve — matches voice profile.
**File:** `outbox/ogilvy/release-notes-v0.2.0.md`

### 2. Issue Triage — from Tesla
**Bottom line:** 3 bugs triaged, 1 needs CEO decision.
**Ada's recommendation:** Approve triage, assign P1 bug to Tesla.
**File:** `outbox/tesla/triage-{date}.md`

## Status Update
- Curie: Delivered intel brief.
- Tesla: Triaged 3 issues.
- Ogilvy: Drafted release notes.
- Nightingale: No activity.

## Flags
- None.
"""


def _make_briefing(tmp_path, today):
    """Write a briefing file and return its path."""
    outbox = tmp_path / "projects" / "test-proj" / "outbox" / "ada"
    outbox.mkdir(parents=True)
    content = SAMPLE_BRIEFING.replace("{date}", today)
    path = outbox / f"ceo-briefing-{today}.md"
    path.write_text(content)
    return path


def test_full_briefing_parse_to_approval_flow(tmp_path):
    """Briefing file → parse → approve item 1 → .approved.md exists with correct content."""
    today = date.today().isoformat()
    briefing_path = _make_briefing(tmp_path, today)

    # Step 1: Parse the briefing
    content = briefing_path.read_text()
    briefing = parse_briefing(content)

    assert len(briefing.items) == 2
    assert briefing.items[0].agent == "ogilvy"
    assert briefing.items[1].agent == "tesla"

    # Step 2: Approve item 1
    item = briefing.items[0]
    write_approval(
        base_dir=str(tmp_path),
        project="test-proj",
        agent=item.agent,
        filename=item.file_path,
    )

    # Step 3: Verify .approved.md was written
    approved = tmp_path / "projects" / "test-proj" / "outbox" / "ogilvy" / "release-notes-v0.2.0.approved.md"
    assert approved.exists()
    content = approved.read_text()
    assert "verdict: approved" in content
    assert "agent: ogilvy" in content


def test_full_briefing_parse_to_feedback_flow(tmp_path):
    """Briefing file → parse → feedback on item 2 → .feedback.md exists with CEO's words."""
    today = date.today().isoformat()
    briefing_path = _make_briefing(tmp_path, today)

    briefing = parse_briefing(briefing_path.read_text())
    item = briefing.items[1]

    write_feedback(
        base_dir=str(tmp_path),
        project="test-proj",
        agent=item.agent,
        filename=item.file_path,
        feedback="Assign the P1 bug to Tesla, deprioritize the P2.",
    )

    feedback_file = tmp_path / "projects" / "test-proj" / "outbox" / "tesla" / f"triage-{today}.feedback.md"
    assert feedback_file.exists()
    content = feedback_file.read_text()
    assert "verdict: revise" in content
    assert "Assign the P1 bug to Tesla" in content


def test_full_briefing_parse_to_rejection_flow(tmp_path):
    """Briefing file → parse → reject item 1 → .feedback.md with rejected verdict."""
    today = date.today().isoformat()
    briefing_path = _make_briefing(tmp_path, today)

    briefing = parse_briefing(briefing_path.read_text())
    item = briefing.items[0]

    write_rejection(
        base_dir=str(tmp_path),
        project="test-proj",
        agent=item.agent,
        filename=item.file_path,
    )

    rejected = tmp_path / "projects" / "test-proj" / "outbox" / "ogilvy" / "release-notes-v0.2.0.feedback.md"
    assert rejected.exists()
    assert "verdict: rejected" in rejected.read_text()


@pytest.mark.asyncio
async def test_callback_approve_writes_correct_file(tmp_path):
    """Full callback flow: button press → handle_callback → .approved.md on disk."""
    today = date.today().isoformat()
    _make_briefing(tmp_path, today)

    # Also create the agent outbox dir
    (tmp_path / "projects" / "test-proj" / "outbox" / "ogilvy").mkdir(parents=True, exist_ok=True)

    cfg = Config(bot_token="x", ceo_chat_id=11111, default_project="test-proj", base_dir=str(tmp_path))

    item_key = f"item_{today}_1"
    briefing_items = {
        item_key: {
            "project": "test-proj",
            "agent": "ogilvy",
            "file_path": "outbox/ogilvy/release-notes-v0.2.0.md",
            "title": "[URGENT] Release Notes v0.2.0",
        }
    }

    query = AsyncMock()
    query.from_user = MagicMock()
    query.from_user.id = 11111  # authorized CEO
    query.data = f"approve:{item_key}"

    update = MagicMock()
    update.callback_query = query

    context = MagicMock()
    context.bot_data = {"config": cfg, "briefing_items": briefing_items}
    context.user_data = {}

    await handle_callback(update, context)

    # Verify the file was written
    approved = tmp_path / "projects" / "test-proj" / "outbox" / "ogilvy" / "release-notes-v0.2.0.approved.md"
    assert approved.exists()
    assert "verdict: approved" in approved.read_text()
