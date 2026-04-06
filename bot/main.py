import asyncio
import logging
import shutil
import sys
from pathlib import Path

from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from bot.config import load_config, project_paths
from bot.handlers import handle_message, handle_callback
from bot.watcher import scan_escalations

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def _get_active_projects(base_dir: str) -> list:
    """Parse PROJECTS.md for active (non-paused) project slugs."""
    import re
    projects_md = Path(base_dir) / "PROJECTS.md"
    if not projects_md.exists():
        return []

    content = projects_md.read_text()
    slugs = []
    for line in content.splitlines():
        # Match table rows: | Priority | Name | `slug` | Status | ...
        match = re.match(r"\|[^|]+\|[^|]+\|\s*`([^`]+)`\s*\|\s*(\w+)", line)
        if match:
            slug, status = match.group(1), match.group(2)
            if status.lower() != "paused":
                slugs.append(slug)
    return slugs


async def check_escalations(context):
    cfg = context.bot_data["config"]
    projects = _get_active_projects(cfg.base_dir)

    escalations = scan_escalations(cfg.base_dir, projects)
    for esc in escalations:
        await context.bot.send_message(
            chat_id=cfg.ceo_chat_id,
            text=(
                f"🚨 Escalation from {esc['agent'].capitalize()}\n"
                f"Project: {esc['project']}\n\n"
                f"{esc['summary']}"
            ),
        )


def main():
    if not shutil.which("claude"):
        print("Error: claude CLI not found in PATH. Install it first.")
        sys.exit(1)

    try:
        cfg = load_config()
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    logger.info("Starting Ada Telegram Bot...")
    logger.info(f"Project: {cfg.default_project}")
    logger.info(f"Base dir: {cfg.base_dir}")

    app = ApplicationBuilder().token(cfg.bot_token).build()

    app.bot_data["config"] = cfg
    app.bot_data["briefing_items"] = {}

    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.job_queue.run_repeating(
        check_escalations, interval=1800, first=10
    )

    logger.info("Bot ready. Polling for messages...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
