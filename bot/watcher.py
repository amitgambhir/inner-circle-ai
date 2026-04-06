import re
from pathlib import Path


def scan_escalations(base_dir: str, projects: list) -> list:
    results = []
    base = Path(base_dir)

    for project in projects:
        esc_dir = base / "projects" / project / "escalations"
        if not esc_dir.exists():
            continue

        for f in esc_dir.iterdir():
            if f.name == ".gitkeep" or not f.suffix == ".md":
                continue

            content = f.read_text()

            agent_match = re.search(r"^agent:\s*(\w+)", content, re.MULTILINE)
            agent = agent_match.group(1) if agent_match else "unknown"

            stuck_match = re.search(
                r"## What's Stuck\n(.+?)(?=\n## |\Z)", content, re.DOTALL
            )
            summary = stuck_match.group(1).strip() if stuck_match else f.name

            results.append({
                "agent": agent,
                "project": project,
                "file": str(f),
                "summary": summary,
            })

    return results
