# Agentic Orchestrator

A portfolio of **agentic AI workflows** built with Claude Code, focused on **knowledge management**. It starts by turning raw Jira tickets into a living business ontology, then turns that knowledge into tools, forecasts, risk radars and an installable playbook.

**Live site:** https://machomono.github.io/agentic-orchestrator/

## What "agentic" means here
The agent is given a **goal**, not step-by-step instructions. It **plans → calls tools → observes → adjusts → verifies its own work**, and a human steps in only at checkpoints. Every project README shows the exact prompts used and a trace of what the agent did.

## Projects
| # | Project | Pattern | Status |
|---|---|---|---|
| 00 | [Portfolio Scaffold](projects/00-portfolio-scaffold) | Goal → multi-tool execution | ✅ |
| 01 | [Jira Harvester](projects/01-jira-harvester) | Gather | ✅ |
| 02 | Ontology Forge | Fan-out → Merge, Critique → Revise | ⏳ |
| 03 | Organizational Archaeology | Build → browser QA loop | ⏳ |
| 04 | Ontology MCP Server | Knowledge as a tool | ⏳ |
| 05 | Synthetic Stakeholder Council | Multi-agent debate | ⏳ |
| 06 | Time-Machine Forecaster | Backtested evals | ⏳ |
| 07 | Tribal Knowledge & Friction Radar | Multi-source analysis | ⏳ |
| 08 | Self-Improving Skill | Eval → self-edit loop | ⏳ |
| 09 | Ontology Radio | Monitor → Act (unattended) | ⏳ |
| 10 | Agentic Playbook marketplace | Package & distribute | ⏳ |

The full roadmap, with prompts and vocabulary, is in [PLAN.md](PLAN.md).

## 📘 The Field Guide
[**GUIDE.md**](GUIDE.md) is a living guide to agentic orchestration: principles, patterns and a glossary, each learned from a real project here. It grows with every project.

## Data
All data comes from the **public Apache Jira** (issues.apache.org). No private or company data is used.
