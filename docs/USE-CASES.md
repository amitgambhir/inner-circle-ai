# Use Cases — Inner Circle AI

The framework ships with **Open Source Repo Management** as the starter use case (the agents manage this repo itself). Below are additional patterns you can adapt by creating a new project directory and adjusting the agent focus areas.

---

## 1. Content Engine for a SaaS Blog

**Scenario:** You're a solo founder or small team that needs consistent content output but spends too many hours researching, writing, and editing.

**How the team adapts:**

| Agent | Focus |
|-------|-------|
| Curie | Research trending topics in your niche, monitor competitor blogs, identify content gaps |
| Ogilvy | Draft blog posts, social media content, email newsletters from Curie's research |
| Nightingale | Track content performance (views, engagement, SEO rankings), maintain editorial calendar |
| Tesla | Light — review code examples in technical posts, ensure accuracy |
| Ada | Coordinate the editorial pipeline, deliver weekly content briefing to CEO |

**Key adaptation:** Ogilvy becomes the primary producer. Curie runs daily instead of weekly. The outbox is heavy on content drafts. Consider adding a standing permission for Nightingale to update the editorial calendar without approval.

**Execution order:** Curie (research) → Ogilvy (draft) → Nightingale (track performance) → Ada (brief CEO)

**Start here:** Create `projects/content-engine/`, assign Curie to research 3 topics per week, have Ogilvy draft one blog post and 3 social posts per week.

---

## 2. Launch Week Playbook

**Scenario:** You're launching a new feature or product and need coordinated output across technical docs, marketing content, and support materials — all on a hard deadline.

**How the team adapts:**

| Agent | Focus |
|-------|-------|
| Curie | Research competitor positioning, gather market context for the launch narrative |
| Tesla | Write the technical changelog, migration guide, breaking changes documentation |
| Ogilvy | Announcement blog post, social threads, email blast, landing page copy |
| Nightingale | Support docs, FAQ, known issues page, contributor migration guide |
| Ada | Run the launch checklist with hard deadlines, ensure nothing ships without CEO approval |

**Key adaptation:** Create a dedicated project (`projects/launch-v2/`), set it to P0 with a hard deadline. All five agents run at full throttle for a bounded period. Ada's briefings include a countdown and checklist.

**Execution order:** All agents work in parallel with Ada coordinating dependencies. Tesla and Curie should run first (technical content and research), then Ogilvy and Nightingale (marketing and support content).

**Start here:** Define the launch date, create the project, have Ada build a checklist with milestones working backward from launch day.

---

## 3. Weekly Competitor Intelligence Briefing

**Scenario:** You want to stay ahead of the market without spending hours manually tracking competitor activity.

**How the team adapts:**

| Agent | Focus |
|-------|-------|
| Curie | Primary — monitor competitor pricing, features, funding, hiring, community activity on a strict weekly cadence |
| Ogilvy | Suggest "response content" — blog posts or social posts that position you against competitor moves |
| Tesla | Flag technical implications of competitor features — what should we build, what can we ignore? |
| Nightingale | Light — track how competitor moves correlate with your support ticket themes |
| Ada | Deliver a consolidated Monday morning competitive briefing |

**Key adaptation:** Curie's output format shifts to a structured comparison table, not a narrative brief. Ogilvy focuses on content angles rather than full drafts. The weekly cadence is strict — this runs every Monday.

**Start here:** Create `projects/competitor-intel/`, define 3-5 competitors for Curie to track, have Ada deliver the first briefing after one week of data collection.

---

## 4. Customer Feedback → Product Pipeline

**Scenario:** You have customer feedback scattered across support channels, and you need a systematic way to turn it into a prioritized product roadmap.

**How the team adapts:**

| Agent | Focus |
|-------|-------|
| Nightingale | Primary — aggregate feedback from support tickets, NPS surveys, app store reviews, community forums |
| Curie | Analyze patterns in Nightingale's aggregated data, identify top themes, validate against market trends |
| Tesla | Write technical specs for the top-priority feature requests identified by Curie |
| Ogilvy | Light — draft "we heard you" updates to close the feedback loop with customers |
| Ada | Present a prioritized roadmap proposal to the CEO |

**Key adaptation:** The intel flow reverses. Instead of Curie feeding everyone, Nightingale collects raw data, Curie analyzes it, and Tesla specs the highest-priority items. Ada's briefing focuses on product decisions rather than operational status.

**Start here:** Create `projects/feedback-pipeline/`, have Nightingale aggregate one week of feedback, then have Curie identify the top 5 themes.

---

## Creating Your Own Use Case

1. Copy `projects/_template/` to `projects/{your-slug}/`
2. Fill in `PROJECT.md` — define the goal, scope, agent assignments, and success criteria
3. Add a row to `PROJECTS.md` with the appropriate priority
4. Adjust agent focus areas in the project's `PROJECT.md` — you don't need to change SOUL.md files
5. Run agents in the recommended execution order for your use case
6. Iterate: refine agent focus, add standing permissions as trust builds

The five agents are general-purpose. The specialization comes from the project definition, not the agent identity.
