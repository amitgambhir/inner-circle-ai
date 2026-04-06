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
