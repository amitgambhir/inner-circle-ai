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
