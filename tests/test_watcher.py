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


def test_get_active_projects_parses_projects_md(tmp_path):
    """Regression: escalation watcher must use PROJECTS.md, not directory scan."""
    from bot.main import _get_active_projects

    (tmp_path / "PROJECTS.md").write_text(
        "## Active Projects\n\n"
        "| Priority | Project | Slug | Status | Lead Agents | Notes |\n"
        "|----------|---------|------|--------|-------------|-------|\n"
        "| **P0** | Alpha | `proj-alpha` | Active | All | |\n"
        "| **P2** | Beta | `proj-beta` | Active | Curie | |\n"
        "| **Paused** | Gamma | `proj-gamma` | Paused | None | frozen |\n"
    )
    # Also create a scratch dir that should NOT appear
    (tmp_path / "projects" / "scratch-test").mkdir(parents=True)

    result = _get_active_projects(str(tmp_path))
    assert "proj-alpha" in result
    assert "proj-beta" in result
    assert "proj-gamma" not in result  # paused = excluded
    assert "scratch-test" not in result  # not in PROJECTS.md = excluded
    assert len(result) == 2


def test_get_active_projects_missing_file(tmp_path):
    """Returns empty list if PROJECTS.md doesn't exist."""
    from bot.main import _get_active_projects

    result = _get_active_projects(str(tmp_path))
    assert result == []
