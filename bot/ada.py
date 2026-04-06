import asyncio
import subprocess


def build_ada_prompt(message: str, project: str) -> str:
    return f"""You are Ada, Chief of Staff.

Read: agents/ada/SOUL.md, AGENTS.md, CEO.md, PROJECTS.md

The CEO sent you this message via Telegram:
"{message}"

Scope to the project "{project}" unless the CEO names a different project.
Based on the current state of the project files, respond to the CEO.

If the CEO is:
- Asking a question: read the relevant files and answer concisely.
- Giving a command (e.g., "move X to P0"): execute it by writing to the appropriate file, then confirm.
- Giving feedback on a specific item: write the feedback file to the correct agent's outbox.

Keep responses short — this is a chat, not a document. The CEO is reading on a phone."""


async def ask_ada(message: str, project: str, base_dir: str) -> str:
    prompt = build_ada_prompt(message, project)

    try:
        proc = await asyncio.create_subprocess_exec(
            "claude", "-p", prompt, "--output-format", "text",
            cwd=base_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

        if proc.returncode == 0:
            return stdout.decode().strip()
        else:
            return f"Ada encountered an error: {stderr.decode().strip()[:200]}"
    except FileNotFoundError:
        return "Error: claude CLI not found. Make sure it's installed and in PATH."
