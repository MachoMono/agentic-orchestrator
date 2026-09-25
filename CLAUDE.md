# Agentic Orchestrator Portfolio

## Who I am
I'm an **AI Orchestrator** on my company's AI Power team, specializing in **knowledge management**. This repo is my public portfolio for learning agentic workflows with Claude Code. I care about practical application and building over deep technical internals.

## How to work with me
- **Define new vocabulary.** When you introduce a term I may not know (agentic, MCP, idempotent, etc.), define it in one plain-English line the first time it comes up.
- **Explain the why.** After finishing a step, say briefly *why* the approach works, so I can reuse the pattern.
- **Stay agentic.** Take a goal and run with it: plan, use tools, verify your own work, and pause only at real decision points.
- **Showcase-ready.** Everything here is public on GitHub. Each project needs a README built from `templates/PROJECT_README.md`.

## Model routing (for subagents)
Subagents inherit this session's model unless told otherwise, so always choose deliberately:
- **Haiku:** classification, simple lookups, formatting, routing
- **Sonnet:** bulk, rule-following work: extraction, summarizing, most coding
- **Opus:** planning, schema design, critique/review, messy judgment calls

Match the model to how much *judgment* the task needs, not how important it feels. Mention which model you chose and why when you launch agents.

## The Field Guide (`GUIDE.md`)
`GUIDE.md` is my living guide to being an agentic orchestrator. **Whenever you teach me a new principle, pattern, technique or term** (in an explanation, or as a lesson from something that went wrong or right), add it to `GUIDE.md` in the right part:
- a **bold one-line rule**, a short explanation, a concrete example from our work, and the project tag, e.g. *(P3)*
- new terms go in the Glossary (Part 8), kept alphabetical
- patterns go in the Pattern library (Part 7)
Organize by topic, not by date. Tighten or merge existing entries rather than duplicating them. Tell me briefly what you added.

## Session hygiene
At the end of every working session on a project, update `projects/<NN-name>/NOTES.md` with:
- what we did
- the current state
- the exact next step (so I can resume by saying "read NOTES.md and continue")

## Repo map
- `PLAN.md`: the full project roadmap (Projects 0–10)
- `GUIDE.md`: the living Agentic Orchestrator Field Guide (principles, patterns, glossary)
- `projects/NN-name/`: one folder per project (README.md + NOTES.md + project files)
- `templates/PROJECT_README.md`: the README template for every project
- `docs/`: GitHub Pages site (live demos go in `docs/<project>/`)
- `data/`, `ontology/`, `skills/`, `playbook/`, `evals/`: shared working folders used across projects

## Data rules
- Use only **public** data (Apache Jira at issues.apache.org). Never commit work or company data.
- Never commit secrets or API keys.
