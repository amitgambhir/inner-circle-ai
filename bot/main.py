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
from bot.projects import get_active_projects
from bot.watcher import scan_escalations

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def _seen_escalations_path(base_dir: str) -> Path:
    return Path(base_dir) / ".escalations-seen"


def _load_seen_escalations(base_dir: str) -> set:
    path = _seen_escalations_path(base_dir)
    if path.exists():
        return set(path.read_text().splitlines())
    return set()


def _save_seen_escalation(base_dir: str, file_path: str):
    path = _seen_escalations_path(base_dir)
    with open(path, "a") as f:
        f.write(file_path + "\n")


async def check_escalations(context):
    cfg = context.bot_data["config"]
    projects = get_active_projects(cfg.base_dir)
    seen = context.bot_data.setdefault("seen_escalations", _load_seen_escalations(cfg.base_dir))

    escalations = scan_escalations(cfg.base_dir, projects)
    for esc in escalations:
        if esc["file"] in seen:
            continue
        seen.add(esc["file"])
        _save_seen_escalation(cfg.base_dir, esc["file"])
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
