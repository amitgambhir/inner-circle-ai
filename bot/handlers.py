from __future__ import annotations

import logging
from datetime import date
from pathlib import Path
from typing import List

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot.ada import ask_ada
from bot.briefing import parse_briefing
from bot.router import write_approval, write_feedback, write_rejection
from bot.runner import resolve_run_order, run_agents

logger = logging.getLogger(__name__)


def is_run_command(text: str) -> bool:
    return text.strip().lower().startswith("run ")


def parse_run_command(text: str) -> List[str]:
    parts = text.strip().lower().split()
    # parts[0] is "run"
    rest = parts[1:]

    if not rest or rest == ["the", "team"] or "team" in rest:
        return ["all"]

    return rest


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cfg = context.bot_data["config"]
    chat_id = update.effective_chat.id

    if chat_id != cfg.ceo_chat_id:
        return

    text = update.message.text.strip()
    user_data = context.user_data

    # If we're awaiting feedback text from the CEO
    if user_data.get("awaiting_feedback"):
        item_key = user_data["awaiting_feedback"]
        items = context.bot_data.get("briefing_items", {})
        item = items.get(item_key)

        if item:
            write_feedback(
                base_dir=cfg.base_dir,
                project=item["project"],
                agent=item["agent"],
                filename=item["file_path"],
                feedback=text,
            )
            await update.message.reply_text(
                f"Feedback sent to {item['agent'].capitalize()} for: {item['title']}"
            )
        else:
            await update.message.reply_text("Could not find item to attach feedback to.")

        user_data.pop("awaiting_feedback", None)
        return

    if is_run_command(text):
        requested = parse_run_command(text)
        try:
            agents = resolve_run_order(requested)
        except ValueError as e:
            await update.message.reply_text(str(e))
            return

        async def on_status(msg: str) -> None:
            await update.message.reply_text(msg)

        await run_agents(
            agents=agents,
            project=cfg.default_project,
            base_dir=cfg.base_dir,
            on_status=on_status,
        )

        await _send_briefing(update, context, cfg, cfg.default_project)
        return

    # Default: ask Ada
    response = await ask_ada(
        message=text,
        project=cfg.default_project,
        base_dir=cfg.base_dir,
    )
    await update.message.reply_text(response)


async def _send_briefing(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    cfg,
    project: str,
) -> None:
    today = date.today().isoformat()
    briefing_path = (
        Path(cfg.base_dir) / "projects" / project / "outbox" / "ada" / f"{today}-briefing.md"
    )

    if not briefing_path.exists():
        await update.message.reply_text("No briefing file found for today.")
        return

    content = briefing_path.read_text()
    briefing = parse_briefing(content)

    if briefing.summary:
        await update.message.reply_text(briefing.summary, parse_mode=None)

    if not briefing.items:
        await update.message.reply_text("No action items in today's briefing.", parse_mode=None)
        return

    for item in briefing.items:
        item_key = f"item_{briefing.date}_{item.number}"

        context.bot_data["briefing_items"][item_key] = {
            "title": item.title,
            "agent": item.agent,
            "file_path": item.file_path,
            "project": project,
        }

        text = (
            f"Item {item.number}: {item.title}\n\n"
            f"Bottom line: {item.bottom_line}\n"
            f"Recommendation: {item.recommendation}\n"
            f"File: {item.file_path}"
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Approve", callback_data=f"approve:{item_key}"),
                InlineKeyboardButton("Reject", callback_data=f"reject:{item_key}"),
                InlineKeyboardButton("Feedback", callback_data=f"feedback:{item_key}"),
            ]
        ])

        await update.message.reply_text(text, reply_markup=keyboard, parse_mode=None)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data
    action, item_key = data.split(":", 1)

    cfg = context.bot_data["config"]
    items = context.bot_data.get("briefing_items", {})
    item = items.get(item_key)

    if not item:
        await query.edit_message_text("Item not found — it may have already been actioned.")
        return

    if action == "approve":
        write_approval(
            base_dir=cfg.base_dir,
            project=item["project"],
            agent=item["agent"],
            filename=item["file_path"],
        )
        await query.edit_message_text(
            f"Approved: {item['title']}", parse_mode=None
        )

    elif action == "reject":
        write_rejection(
            base_dir=cfg.base_dir,
            project=item["project"],
            agent=item["agent"],
            filename=item["file_path"],
        )
        await query.edit_message_text(
            f"Rejected: {item['title']}", parse_mode=None
        )

    elif action == "feedback":
        context.user_data["awaiting_feedback"] = item_key
        await query.edit_message_text(
            f"Send your feedback for: {item['title']}", parse_mode=None
        )
