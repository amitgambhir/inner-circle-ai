"""Parse PROJECTS.md to extract active project slugs."""

import re
from pathlib import Path


def get_active_projects(base_dir: str) -> list:
    """Parse PROJECTS.md for non-paused project slugs.

    Expects a markdown table with columns: Priority | Project | Slug | Status | ...
    Slug values must be wrapped in backticks: `my-project`
    Projects with status "Paused" (case-insensitive) are excluded.
    """
    projects_md = Path(base_dir) / "PROJECTS.md"
    if not projects_md.exists():
        return []

    content = projects_md.read_text()
    slugs = []

    in_table = False
    for line in content.splitlines():
        stripped = line.strip()

        # Skip empty lines and non-table lines
        if not stripped.startswith("|"):
            in_table = False
            continue

        # Skip separator rows (|---|---|...)
        if re.match(r"\|[\s\-|]+\|$", stripped):
            in_table = True
            continue

        # Skip header row (first row after we see a table start)
        if not in_table:
            in_table = True
            continue

        # Parse data rows: extract backtick-wrapped slug and status
        cells = [c.strip() for c in stripped.split("|")]
        # Split gives empty strings at start/end from leading/trailing pipes
        cells = [c for c in cells if c]

        if len(cells) < 4:
            continue

        # Slug is column 3 (0-indexed: 2), Status is column 4 (0-indexed: 3)
        slug_cell = cells[2]
        status_cell = cells[3]

        slug_match = re.search(r"`([^`]+)`", slug_cell)
        if not slug_match:
            continue

        slug = slug_match.group(1)
        if status_cell.lower().strip() == "paused":
            continue

        slugs.append(slug)

    return slugs
