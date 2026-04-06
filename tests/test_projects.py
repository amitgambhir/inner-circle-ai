import pytest
from bot.projects import get_active_projects


STANDARD_TABLE = """\
## Active Projects

| Priority | Project | Slug | Status | Lead Agents | Notes |
|----------|---------|------|--------|-------------|-------|
| **P0** | Alpha | `proj-alpha` | Active | All | main project |
| **P2** | Beta | `proj-beta` | Active | Curie | secondary |
| **Paused** | Gamma | `proj-gamma` | Paused | None | frozen |
"""


def test_parses_active_projects(tmp_path):
    (tmp_path / "PROJECTS.md").write_text(STANDARD_TABLE)
    result = get_active_projects(str(tmp_path))
    assert result == ["proj-alpha", "proj-beta"]


def test_excludes_paused(tmp_path):
    (tmp_path / "PROJECTS.md").write_text(STANDARD_TABLE)
    result = get_active_projects(str(tmp_path))
    assert "proj-gamma" not in result


def test_missing_file(tmp_path):
    result = get_active_projects(str(tmp_path))
    assert result == []


def test_empty_table(tmp_path):
    (tmp_path / "PROJECTS.md").write_text(
        "## Active Projects\n\n"
        "| Priority | Project | Slug | Status | Lead Agents | Notes |\n"
        "|----------|---------|------|--------|-------------|-------|\n"
    )
    result = get_active_projects(str(tmp_path))
    assert result == []


def test_extra_whitespace(tmp_path):
    (tmp_path / "PROJECTS.md").write_text(
        "## Active Projects\n\n"
        "|  Priority  |  Project  |  Slug  |  Status  | Lead | Notes |\n"
        "|----------|---------|------|--------|-------------|-------|\n"
        "|  **P0**  |  My Project  |  `my-proj`  |  Active  | All | |\n"
    )
    result = get_active_projects(str(tmp_path))
    assert result == ["my-proj"]


def test_case_insensitive_paused(tmp_path):
    (tmp_path / "PROJECTS.md").write_text(
        "## Active Projects\n\n"
        "| Priority | Project | Slug | Status | Lead | Notes |\n"
        "|----------|---------|------|--------|------|-------|\n"
        "| P1 | A | `proj-a` | PAUSED | All | |\n"
        "| P2 | B | `proj-b` | paused | All | |\n"
        "| P0 | C | `proj-c` | Active | All | |\n"
    )
    result = get_active_projects(str(tmp_path))
    assert result == ["proj-c"]


def test_missing_backticks_skips_row(tmp_path):
    (tmp_path / "PROJECTS.md").write_text(
        "## Active Projects\n\n"
        "| Priority | Project | Slug | Status | Lead | Notes |\n"
        "|----------|---------|------|--------|------|-------|\n"
        "| P0 | Good | `valid-slug` | Active | All | |\n"
        "| P1 | Bad | no-backticks | Active | All | |\n"
    )
    result = get_active_projects(str(tmp_path))
    assert result == ["valid-slug"]


def test_too_few_columns_skips_row(tmp_path):
    (tmp_path / "PROJECTS.md").write_text(
        "## Active Projects\n\n"
        "| Priority | Project | Slug | Status | Lead | Notes |\n"
        "|----------|---------|------|--------|------|-------|\n"
        "| P0 | Good | `valid` | Active | All | |\n"
        "| P1 | Broken |\n"
    )
    result = get_active_projects(str(tmp_path))
    assert result == ["valid"]
