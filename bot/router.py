from datetime import date
from pathlib import Path


def _resolve_filename(filename: str) -> str:
    return Path(filename).name


def _stem(filename: str) -> str:
    name = _resolve_filename(filename)
    if name.endswith(".md"):
        return name[:-3]
    return name


def write_approval(base_dir: str, project: str, agent: str, filename: str):
    stem = _stem(filename)
    outbox = Path(base_dir) / "projects" / project / "outbox" / agent
    outbox.mkdir(parents=True, exist_ok=True)

    path = outbox / f"{stem}.approved.md"
    today = date.today().isoformat()

    path.write_text(
        f"---\n"
        f"from: ceo\n"
        f"re: {_resolve_filename(filename)}\n"
        f"date: {today}\n"
        f"verdict: approved\n"
        f"agent: {agent}\n"
        f"---\n\n"
        f"Approved by CEO.\n"
    )


def write_feedback(
    base_dir: str, project: str, agent: str, filename: str, feedback: str
):
    stem = _stem(filename)
    outbox = Path(base_dir) / "projects" / project / "outbox" / agent
    outbox.mkdir(parents=True, exist_ok=True)

    path = outbox / f"{stem}.feedback.md"
    today = date.today().isoformat()

    path.write_text(
        f"---\n"
        f"from: ceo\n"
        f"re: {_resolve_filename(filename)}\n"
        f"date: {today}\n"
        f"verdict: revise\n"
        f"agent: {agent}\n"
        f"---\n\n"
        f"## Feedback\n\n"
        f"{feedback}\n"
    )


def write_rejection(base_dir: str, project: str, agent: str, filename: str):
    stem = _stem(filename)
    outbox = Path(base_dir) / "projects" / project / "outbox" / agent
    outbox.mkdir(parents=True, exist_ok=True)

    path = outbox / f"{stem}.feedback.md"
    today = date.today().isoformat()

    path.write_text(
        f"---\n"
        f"from: ceo\n"
        f"re: {_resolve_filename(filename)}\n"
        f"date: {today}\n"
        f"verdict: rejected\n"
        f"agent: {agent}\n"
        f"---\n\n"
        f"Rejected by CEO.\n"
    )
