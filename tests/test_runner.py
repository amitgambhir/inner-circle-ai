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
