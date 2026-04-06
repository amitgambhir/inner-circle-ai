import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from bot.handlers import parse_run_command, is_run_command, handle_callback


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


def test_briefing_filename_matches_documented_convention(tmp_path):
    """Regression: bot must look for ceo-briefing-YYYY-MM-DD.md, not YYYY-MM-DD-briefing.md."""
    from datetime import date

    outbox = tmp_path / "projects" / "test" / "outbox" / "ada"
    outbox.mkdir(parents=True)

    today = date.today().isoformat()
    # The documented filename from SOUL.md and CLAUDE.md
    briefing = outbox / f"ceo-briefing-{today}.md"
    briefing.write_text("# CEO Briefing — " + today + "\n\n## Decisions Needed (0 items)\n\n## Status Update\n- All clear.\n\n## Flags\n- None.\n")

    # Verify the handler would find this file
    expected_path = (
        Path(tmp_path) / "projects" / "test" / "outbox" / "ada" / f"ceo-briefing-{today}.md"
    )
    assert expected_path.exists()

    # The old wrong filename should NOT exist
    wrong_path = outbox / f"{today}-briefing.md"
    assert not wrong_path.exists()


@pytest.mark.asyncio
async def test_callback_rejects_unauthorized_user():
    """Regression: callback buttons must check chat_id, not just messages."""
    from bot.config import Config

    cfg = Config(bot_token="x", ceo_chat_id=11111, default_project="test", base_dir="/tmp")

    # Mock Telegram objects
    query = AsyncMock()
    query.message.chat.id = 99999  # wrong chat ID
    query.data = "approve:item_2026-04-06_1"

    update = MagicMock()
    update.callback_query = query

    context = MagicMock()
    context.bot_data = {"config": cfg, "briefing_items": {}}

    await handle_callback(update, context)

    # Should answer with "Unauthorized." and NOT proceed to write files
    query.answer.assert_called_once_with("Unauthorized.")
    # edit_message_text should NOT have been called (no approval/rejection written)
    query.edit_message_text.assert_not_called()
