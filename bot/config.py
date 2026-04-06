import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

AGENT_ORDER = ["curie", "tesla", "ogilvy", "nightingale", "ada"]

AGENTS = {
    "curie": {"title": "Curie, Head of Research"},
    "tesla": {"title": "Tesla, Head of Engineering"},
    "ogilvy": {"title": "Ogilvy, Head of Growth"},
    "nightingale": {"title": "Nightingale, Head of Operations"},
    "ada": {"title": "Ada, Chief of Staff"},
}


@dataclass
class Config:
    bot_token: str
    ceo_chat_id: int
    default_project: str
    base_dir: str


def load_config() -> Config:
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN is required")

    chat_id = os.environ.get("TELEGRAM_CEO_CHAT_ID")
    if not chat_id:
        raise ValueError("TELEGRAM_CEO_CHAT_ID is required")

    return Config(
        bot_token=bot_token,
        ceo_chat_id=int(chat_id),
        default_project=os.environ.get("DEFAULT_PROJECT", "inner-circle-mgmt"),
        base_dir=os.environ.get("INNER_CIRCLE_DIR", str(Path.cwd())),
    )


def project_paths(project_slug: str, base_dir: str = None) -> dict:
    base = Path(base_dir) if base_dir else Path.cwd()
    project_dir = base / "projects" / project_slug
    return {
        "project_dir": str(project_dir),
        "outbox_ada": str(project_dir / "outbox" / "ada"),
        "escalations": str(project_dir / "escalations"),
    }
