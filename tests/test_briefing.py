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
