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

    write_approval(
        base_dir=str(tmp_path),
        project="test",
        agent="ogilvy",
        filename="outbox/ogilvy/release-notes.md",
    )

    approved = outbox / "release-notes.approved.md"
    assert approved.exists()
