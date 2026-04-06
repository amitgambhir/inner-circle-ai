# Customization — Making Inner Circle AI Yours

## Step 1: Fork the Repo

```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/{you}/inner-circle-ai.git
cd inner-circle-ai
```

## Step 2: Rename Agents (Optional)

The agents are named after historical figures. You can keep them or rename them to figures that resonate with your domain.

**To rename an agent:**
1. Rename the directory: `agents/curie/` → `agents/{new-name}/`
2. Update the SOUL.md inside with the new identity
3. Update references in `AGENTS.md`, `HEARTBEAT.md`, and any `PROJECT.md` files
4. Update outbox directory names in project templates

**Naming tips:**
- Pick figures whose personality matches the role. The LLM already knows these characters from training data, which gives you free personality grounding.
- Keep names short and distinct — agents reference each other by name.
- Historical figures work better than fictional characters for professional contexts.

## Step 3: Build Your Voice Profile

Your agents need to know how you communicate. Feed your AI tool 5-10 of your best writing samples and ask:

> "Analyze these writing samples. Identify my tone, sentence structure patterns, words I use often, words I never use, formatting preferences, and any other stylistic patterns. Output a voice profile I can give to AI agents."

Paste the result into the **Voice Profile** section of `CEO.md`.

**Good samples to use:**
- Sent emails (your natural voice, not formal corporate)
- LinkedIn posts or blog articles
- Slack messages to your team
- Tweets or social posts

## Step 4: Swap the Starter Use Case

Replace `projects/inner-circle-mgmt/` with your own first project:

1. Copy `projects/_template/` to `projects/{your-project}/`
2. Fill in `PROJECT.md` with your goals, scope, and agent assignments
3. Update `PROJECTS.md` to list your project as P0
4. Delete or deprioritize `inner-circle-mgmt/`

See `docs/USE-CASES.md` for templates across different scenarios.

## Step 5: Adjust Standing Permissions

Review the default standing permissions in `CEO.md`. Add or remove based on your comfort level:

- **More trust:** Add permissions for routine actions (e.g., "Ogilvy may schedule approved social posts")
- **More control:** Remove permissions and route everything through the approval queue
- **Start tight, loosen over time** — this is the recommended approach

## Step 6: Customize Communication Standards

Edit `AGENTS.md` to adjust how agents report to you:

- Change the reporting format if the default doesn't match your preferences
- Adjust quality standards for your domain
- Add domain-specific terminology or context that all agents should know

## Step 7: Add Domain Context to SOUL.md Files

Each SOUL.md can be enriched with domain-specific knowledge:

- **Curie:** Add your specific research sources, competitors, and signals to track
- **Tesla:** Add your tech stack, coding standards, and architectural principles
- **Ogilvy:** Add your brand guidelines, content pillars, and platform-specific constraints
- **Nightingale:** Add your key metrics, SLA targets, and documentation standards

Keep each SOUL.md under 60 lines. Put detailed reference material in the project's `intel/` directory instead.

## Step 8: Set Up Scheduling (Optional)

For always-on operation, configure cron scheduling using your preferred tool:

**OpenClaw:** Built-in cron scheduling and Telegram integration. See OpenClaw docs.

**System cron:** Set up cron jobs that trigger your AI tool with the appropriate SOUL.md context.

**Manual:** Run agents manually through your IDE. Start with this — add automation later.

---

## What NOT to Customize (Without Careful Thought)

- **The approval queue pattern.** This is the governance backbone. Changing it affects trust and safety.
- **The one-writer-per-file rule.** This prevents conflicts. If you change it, you need another conflict resolution strategy.
- **Ada's routing role.** The hub-and-spoke model simplifies everything. Removing Ada creates N communication channels instead of one.
- **The memory system.** Agents depend on explicit file-based memory. Removing it breaks continuity across sessions.
