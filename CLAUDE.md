# Agentic Orchestrator Portfolio

## Who I am
I'm an **AI Orchestrator** on my company's AI Power team, specializing in **knowledge management**. This repo is my public portfolio for learning agentic workflows with Claude Code. I care about practical application and building over deep technical internals.

## How to work with me
- **Define new vocabulary.** When you introduce a term I may not know (agentic, MCP, idempotent, etc.), define it in one plain-English line the first time it comes up.
- **Explain the why.** After finishing a step, say briefly *why* the approach works, so I can reuse the pattern.
- **Stay agentic.** Take a goal and run with it: plan, use tools, verify your own work, and pause only at real decision points.
- **Showcase-ready.** Everything here is public on GitHub. Each project needs a README built from `templates/PROJECT_README.md`.

## Session hygiene
At the end of every working session on a project, update `projects/<NN-name>/NOTES.md` with:
- what we did
- the current state
- the exact next step (so I can resume by saying "read NOTES.md and continue")

## Repo map
- `PLAN.md`: the full project roadmap (Projects 0–10)
- `projects/NN-name/`: one folder per project (README.md + NOTES.md + project files)
- `templates/PROJECT_README.md`: the README template for every project
- `docs/`: GitHub Pages site (live demos go in `docs/<project>/`)
- `data/`, `ontology/`, `skills/`, `playbook/`, `evals/`: shared working folders used across projects

## Data rules
- Use only **public** data (Apache Jira at issues.apache.org). Never commit work or company data.
- Never commit secrets or API keys.
