"""Format-drift guard: verifies the briefing parser handles the exact format
documented in Ada's SOUL.md. If someone changes the SOUL.md briefing template,
this test breaks — flagging that the parser needs updating too."""

import re
from pathlib import Path

from bot.briefing import parse_briefing


def _extract_briefing_template_from_soul():
    """Read the briefing format block from Ada's SOUL.md."""
    soul = Path("agents/ada/SOUL.md").read_text()
    # Extract the markdown code block after "## CEO Briefing Format"
    match = re.search(
        r"## CEO Briefing Format\s+```markdown\n(.*?)```",
        soul,
        re.DOTALL,
    )
    assert match, "Could not find '## CEO Briefing Format' code block in Ada's SOUL.md"
    return match.group(1)


def _hydrate_template(template: str) -> str:
    """Replace template placeholders with concrete values so the parser can parse it."""
    result = template
    # Replace all date placeholders first (appears multiple times)
    result = result.replace("YYYY-MM-DD", "2026-04-06")

    # Order matters: replace the more specific [URGENT] pattern before the generic one
    one_shot = [
        ("{project-slug} (or \"multi-project\" if spanning several)", "inner-circle-mgmt"),
        ("X items", "2 items"),
        ("[URGENT] {title} — from {agent}", "[URGENT] Security Fix — from Tesla"),
        ("{title} — from {agent}", "Release Notes v1.0 — from Ogilvy"),
    ]
    for old, new in one_shot:
        result = result.replace(old, new, 1)

    # Replace repeated placeholders (appear in both items)
    result = result.replace("{one sentence}", "Ready for review.")
    result = result.replace(
        "Approve / Revise / Reject — because {reason}", "Approve — looks good."
    )

    # File paths: first is tesla (URGENT item), second is ogilvy
    result = result.replace("outbox/{agent}/filename.md", "outbox/tesla/security-fix.md", 1)
    result = result.replace("outbox/{agent}/filename.md", "outbox/ogilvy/release-notes.md", 1)

    # Status update lines
    result = result.replace(
        "{one line — what she delivered or is working on}", "Delivered daily brief."
    )
    result = result.replace("{one line}", "Active.")

    # Flags and routed decisions
    result = result.replace(
        "{any coordination issues, approaching deadlines, or staleness warnings}", "None."
    )
    result = result.replace(
        "{list of approvals/feedback you relayed from the CEO's last response}",
        "Approved item 1.",
    )
    return result


def test_parser_handles_soul_md_template():
    """The parser must successfully parse a briefing that follows Ada's SOUL.md format."""
    template = _extract_briefing_template_from_soul()
    content = _hydrate_template(template)

    briefing = parse_briefing(content)

    assert briefing.date == "2026-04-06"
    assert len(briefing.items) >= 1
    # First item should have been parsed with correct fields
    item = briefing.items[0]
    assert item.number == 1
    assert item.bottom_line  # not empty
    assert item.recommendation  # not empty
    assert item.file_path  # not empty
    assert item.agent  # extracted from file path


def test_soul_md_template_has_required_sections():
    """Guard: Ada's SOUL.md must contain the sections the parser depends on."""
    template = _extract_briefing_template_from_soul()

    assert "# CEO Briefing —" in template
    assert "## Decisions Needed" in template
    assert "**Bottom line:**" in template
    assert "**Ada's recommendation:**" in template
    assert "**File:**" in template
    assert "## Status Update" in template
    assert "## Flags" in template
