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



# PROJECTS.md parser tests moved to tests/test_projects.py
