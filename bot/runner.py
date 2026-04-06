import asyncio
import subprocess
from datetime import date
from typing import Callable

from bot.config import AGENTS, AGENT_ORDER


def build_agent_prompt(
    agent: str, agent_title: str, project: str, date: str
) -> str:
    return f"""You are {agent_title}.

Read these files to load your context:
1. agents/{agent}/SOUL.md
2. AGENTS.md
3. CEO.md
4. PROJECTS.md
5. projects/{project}/PROJECT.md
6. agents/{agent}/MEMORY.md

Check agents/{agent}/memory/ for recent session logs.
Check projects/{project}/outbox/{agent}/ for .feedback.md files — address those first.

Today's date is {date}. Your active project is {project}.

Run your full session workflow as defined in your SOUL.md.

When done, write your daily memory log to agents/{agent}/memory/{date}.md."""


def resolve_run_order(requested: list) -> list:
    if "all" in requested or "team" in requested:
        return list(AGENT_ORDER)

    for agent in requested:
        if agent not in AGENTS:
            raise ValueError(f"Unknown agent: {agent}")

    return [a for a in AGENT_ORDER if a in requested]


async def run_agents(
    agents: list,
    project: str,
    base_dir: str,
    on_status: Callable = None,
):
    today = date.today().isoformat()
    results = []

    for agent in agents:
        title = AGENTS[agent]["title"]
        prompt = build_agent_prompt(agent, title, project, today)

        if on_status:
            await on_status(f"Running {title}...")

        try:
            tools = AGENTS[agent].get("tools", [])
            cmd = ["claude", "-p", prompt, "--output-format", "text"]
            if tools:
                cmd += ["--allowedTools"] + tools

            proc = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=base_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()

            if proc.returncode == 0:
                msg = f"✓ {title} complete"
                results.append({"agent": agent, "ok": True, "msg": msg})
            else:
                err = stderr.decode().strip()[:200]
                msg = f"✗ {title} failed — {err}"
                results.append({"agent": agent, "ok": False, "msg": msg})
        except FileNotFoundError:
            msg = f"✗ {title} failed — claude CLI not found"
            results.append({"agent": agent, "ok": False, "msg": msg})

        if on_status:
            await on_status(results[-1]["msg"])

    return results
