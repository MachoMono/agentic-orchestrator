# Plan: Agentic Orchestrator Portfolio (Jira → Business Ontology, and Beyond)

## Context
You're the new AI Orchestrator on your company's AI Power team, specializing in knowledge management. You're practicing at home, self-paced, with no schedule. You want **real agentic projects** that are **unconventional**, where **each one can be shown off on GitHub**. Every project includes **the prompts to type, why they work, and vocabulary with definitions**.

**Data:** Apache's public Jira (issues.apache.org, no login, openly licensed) stands in for your company's Jira. Everything is safe to publish, and every skill later points at your work Jira unchanged.

**Tools:** **Claude Code CLI** as the main workspace, **VS Code** alongside it for reading files, **GitHub** (`gh` CLI) as the showcase.

**Resuming:** each project saves state to disk. Start `claude` and say *"Read projects/*/NOTES.md and tell me where I left off."*

---

## The agentic bar (every project must clear it)
Chat is when you ask and Claude answers. **Agentic** is when you give a *goal* and Claude **plans → uses tools → observes → adjusts → verifies its own work**, and you step in only at *checkpoints*. Each project lists its **Agentic check**.

| Term | Meaning |
|---|---|
| **Agent** | An AI that pursues a goal by choosing and using tools in a loop. |
| **Agentic loop** | Think → act (tool call) → observe result → repeat until done. |
| **Tool call** | One action: run a command, read or write a file, fetch a URL, click in a browser. |
| **Context window** | Everything the model can "see" at once. It's limited, so what you feed it matters. |
| **Context engineering** | Deliberately choosing what goes into and stays out of the context. |
| **Orchestration** | Coordinating multiple agents, tools, and steps toward one outcome. |
| **Human-in-the-loop (HITL)** | Designed pause points where a person approves before the agent continues. |

---

## GitHub showcase standard (applies to every project)
- **One public monorepo:** `agentic-orchestrator/`, with each project in `projects/NN-name/`, plus a **GitHub Pages** site that hosts every live demo.
- **Every project README** uses the same template: *Problem → Agentic pattern (diagram) → Demo (GIF/live link) → Prompts I used → What the agent actually did (tool trace) → Results/eval score → Vocabulary → Lessons.*
- **Terminal recordings:** `brew install vhs` records a GIF of the agent working, which is proof that it's agentic.
- **Pinned profile README** linking the portfolio. The prompt log is part of the showcase: *how* you directed the agent is the skill you're demonstrating.

| Term | Meaning |
|---|---|
| **Monorepo** | One repository that holds many projects. |
| **GitHub Pages** | Free static website hosting straight from a repo. It's your live demo site. |
| **GitHub Actions** | Automation that runs on GitHub's servers on a trigger or schedule. |
| **Tool trace** | The record of which tools the agent called, and in what order. It shows it *acted*, not just talked. |

---

## Project 0: Agent builds the portfolio scaffold
**Goal:** the public repo, Pages site, README template, and CLAUDE.md, created and pushed by Claude.

**Prompts:**
1. `Build my portfolio scaffold here: git init, CLAUDE.md (I'm an AI Orchestrator; define new vocabulary; update projects/<name>/NOTES.md at the end of each session), a README template at templates/PROJECT_README.md with sections: Problem, Agentic Pattern (mermaid diagram), Demo, Prompts I Used, What the Agent Did, Results, Vocabulary, Lessons. Create a GitHub Pages landing page in docs/. Use gh to create a public repo "agentic-orchestrator", push, and enable Pages. Verify the site loads.`

**Why:** one outcome-level prompt drives about 15 actions. Standardizing the README makes every later project instantly presentable.

**Agentic check:** multi-tool (git, gh, files, web check) ✔ self-verification (site loads) ✔

| Term | Meaning |
|---|---|
| **CLAUDE.md** | A file Claude reads at the start of every session in the folder: your standing instructions. |
| **gh CLI** | GitHub's command-line tool. It lets the agent create repos, PRs, and Pages. |
| **Mermaid** | Text-based diagrams that GitHub renders automatically. Useful for drawing agent patterns. |

---

## Project 1: Jira Harvester (the "Gather" pattern)
**Showcase:** a GIF of the agent paginating, recovering from errors, and printing a validation report, plus a clean dataset in the repo.

**Prompts:**
1. Press **Shift+Tab** for plan mode, then: `Goal: harvest ~1,000 KAFKA issues from the public Apache Jira REST API spanning several years into data/raw/ (key, summary, description, type, status, priority, components, labels, assignee, created, resolved, comments, changelog of status/assignee changes). Plan it, including how you'll verify completeness.`
2. `Execute. Then validate (counts, missing fields, duplicate keys), write data/tickets.md as a readable digest, and fill in the project README.`

**Why:** plan mode separates *deciding* from *doing*. The changelog (status and assignee history) is the secret ingredient that later projects use.

**Agentic check:** goal ✔ HTTP + scripts ✔ loop (pagination, retries) ✔ validation ✔ checkpoint (plan) ✔

| Term | Meaning |
|---|---|
| **Plan mode** | Claude researches and proposes a plan but can't change anything until you approve. |
| **REST API / JSON** | A web service you query by URL, and the structured text format it returns. |
| **Pagination** | Data arrives in pages, so the agent must loop to collect everything. |
| **Changelog** | Jira's history of every field change on a ticket: who moved it, when, and from what to what. |

---

## Project 2: Ontology Forge (the "Fan-out → Merge" and "Critique → Revise" patterns)
**Showcase:** a README diagram showing parallel subagents and a critic agent, plus before/after stats (e.g. "412 raw entities → 187 canonical").

**Prompts:**
1. `Sample 40 tickets and propose an ontology schema (entity types like System, Component, Role, Process, Failure Mode, Business Impact; relationship types) with definitions and examples. Save to ontology/schema.md and stop for my review.`
2. **Checkpoint:** you edit the schema. This is where your business judgment is the value.
3. `Extract entities and relationships from all tickets: split into batches, one subagent per batch in parallel, every relationship citing ticket keys. Merge into ontology/ontology.json.`
4. `Launch a critic subagent that didn't build it: find synonyms ("KRaft" vs "Kraft mode"), weak evidence (open the cited tickets), schema violations → ontology/review.md.` Then you ✅ the fixes: `Apply ✅ fixes with canonical names + aliases, re-verify, log to CHANGELOG.md, commit.`

**Why:** schema-first gives consistency. Fresh-context subagents keep quality from sliding. A critic without the builder's blind spots catches what one pass misses.

**Agentic check:** multi-agent orchestration ✔ grounding ✔ independent verification ✔ HITL ✔

| Term | Meaning |
|---|---|
| **Ontology** | A formal model of a domain: types of things, how they relate, and rules. |
| **Entity / triple** | A specific thing (e.g. "Kafka Connect"), and a fact stated as *subject → relation → object*. |
| **Subagent** | A separate Claude instance with its own clean context, launched for a sub-task. |
| **Grounding** | Tying every claim to a source so it can be checked. This reduces **hallucination** (plausible but unsupported output). |
| **Entity resolution / canonicalization** | Deciding when names mean the same thing, then picking one official name. |

---

## Project 3: Organizational Archaeology (a time-lapse knowledge graph)
**Unconventional angle:** instead of a static diagram, **watch the business's mental model evolve over time**. Concepts are born, grow, merge, and die. Drag a slider through the years.

**Showcase:** a live interactive graph on GitHub Pages with a time slider, plus a README GIF of the time-lapse.

**Prompts:**
1. `Build an interactive knowledge-graph page in docs/archaeology/ from ontology.json, using ticket dates so each entity and relationship appears when first mentioned. Add a year slider and play button; node size = ticket volume at that time. Click a node → its evidence tickets.`
2. `Open it in the browser, play the time-lapse, screenshot 3 moments, and fix anything broken. Loop until it works. Then write a "3 eras of Kafka" narrative from what the graph shows, put it in the README, and push.`

**Why:** the build → test in a real browser → fix loop makes the agent its own QA. The narrative step turns data into a *story*, which is what executives remember.

**Agentic check:** browser automation ✔ self-QA loop ✔ insight synthesis ✔

| Term | Meaning |
|---|---|
| **Knowledge graph** | An ontology populated with real entities and drawn as a network of **nodes** (things) and **edges** (relationships). |
| **Temporal graph** | A graph where nodes and edges carry time, so you can see change. |
| **Browser automation** | The agent controls a real browser (clicks, screenshots) to test its own work. |

---

## Project 4: Ontology as an MCP Server (turn knowledge into a tool)
**Unconventional angle:** the ontology stops being a document and becomes **a capability any AI agent can plug into**. Other Claudes can ask "what depends on the Broker?" as a tool call.

**Showcase:** an installable MCP server in the repo, and a GIF of a *fresh* Claude session using it to answer questions it couldn't answer before.

**Prompts:**
1. `Build a small MCP server (Python) exposing the ontology as tools: find_entity, neighbors, path_between, evidence_for, and search_tickets. Write tests, then register it with Claude Code for this project.`
2. `Now in a fresh subagent that only has the MCP tools, answer: "If the Controller component fails, what business impacts are likely, and what's the evidence?" Show the tool calls it made.`

**Why:** this is how knowledge management scales in the agent era. You don't send people documents. You give *agents* structured access.

**Agentic check:** agent builds tools for other agents ✔ tested by an independent agent ✔

| Term | Meaning |
|---|---|
| **MCP (Model Context Protocol)** | An open standard for connecting AI to tools and data. An "MCP server" offers tools that any compatible AI can call. |
| **Multi-hop query** | Answering by chaining lookups (component → failures → impacts). |
| **Tool schema** | The definition of a tool's name, inputs, and purpose that the AI reads to know how to use it. |

---

## Project 5: Synthetic Stakeholder Council
**Unconventional angle:** the ontology's *Role* entities (SRE, connector developer, enterprise user, security reviewer) become **AI personas grounded in real ticket history**. Give them a proposed change and they debate it, citing what "their" tickets show they care about.

**Showcase:** a README with a sample council transcript and the decision memo it produced, plus a council-flow diagram.

**Prompts:**
1. `From ontology Role entities, build persona cards (goals, pain points, typical objections) grounded in their tickets, with citations. Save to council/personas/.`
2. `Run a council: proposal = "deprecate ZooKeeper mode in the next release." One subagent per persona writes a position with evidence; a moderator agent runs 2 rounds of rebuttal, then writes a decision memo with risks, dissent, and open questions.`

**Why:** it pressure-tests decisions against real historical concerns before the meeting. The difference from generic "role-play" is grounding: every objection cites a ticket.

**Agentic check:** multi-agent debate ✔ grounded personas ✔ moderator orchestration ✔

| Term | Meaning |
|---|---|
| **Persona agent** | An agent given a specific role and viewpoint to argue from. |
| **Moderator / orchestrator agent** | An agent that runs other agents and synthesizes their output. |
| **Adversarial collaboration** | Agents deliberately disagreeing to expose weak reasoning. |

---

## Project 6: Time-Machine Forecaster (backtesting an agent)
**Unconventional angle:** hide the future from the agent. It sees only tickets before a cutoff date, predicts next quarter's hot spots (which components and failure modes will surge), and is **then graded against what actually happened**. That's a real scorecard, not vibes.

**Showcase:** a README chart of predicted vs actual, the accuracy score across 4 historical cutoffs, and the method.

**Prompts:**
1. `Build a backtest harness: for cutoffs [4 dates], give a subagent ONLY tickets before the cutoff (enforce it — separate folder). It writes a forecast: top 5 rising components/failure modes with reasoning.`
2. `Score each forecast against the real next-90-days tickets, write evals/forecast-results.md with a chart, then have the agent analyze its misses and revise its forecasting instructions. Re-run and compare scores.`

**Why:** this teaches the most important orchestrator skill: **proving** an agent works. Enforcing the cutoff with separate folders is how you prevent the agent from peeking at the answers.

**Agentic check:** controlled information access ✔ self-scoring ✔ improve-and-re-run loop ✔

| Term | Meaning |
|---|---|
| **Backtesting** | Testing a prediction method on past data where you already know the outcome. |
| **Data leakage** | When the agent accidentally sees information it shouldn't (the "future"), which inflates its score. |
| **Eval** | A repeatable test that scores an AI workflow. |
| **Prompt iteration** | Improving instructions based on measured failures. |

---

## Project 7: Tribal Knowledge & Friction Radar
**Unconventional angle:** use the *changelog* to find what org charts hide. It finds **bus-factor risks** (components only one person understands), **ticket ping-pong** (reassigned 4+ times), **zombie tickets** (reopened repeatedly), and **heat** (tense comment threads).

**Showcase:** a "risk radar" dashboard on Pages, plus an auto-generated "Top 10 knowledge risks" report.

**Prompts:**
1. `From the changelog and comments, compute per-component: unique resolvers (bus factor), reassignment counts, reopen rates, and comment-thread friction (have a subagent classify tone on a sample). Link each to ontology entities.`
2. `Build a dashboard page in docs/radar/, verify it in the browser, and write a report with the 10 biggest knowledge risks, each with evidence tickets and a recommended mitigation (docs to write, pairing, ownership change).`

**Why:** this is knowledge management at its sharpest: finding knowledge that exists only in people's heads *before* they leave. Leadership will care about this one.

**Agentic check:** multi-source analysis ✔ classification subagent ✔ browser QA ✔ recommendations with evidence ✔

| Term | Meaning |
|---|---|
| **Bus factor** | How many people would have to leave before knowledge of something is lost. 1 is dangerous. |
| **Tribal knowledge** | Know-how that lives in people's heads, not in documentation. |
| **Classification** | An agent labeling items into categories (e.g. tense or neutral). |

---

## Project 8: The Self-Improving Skill
**Unconventional angle:** package the Forge (Project 2) as a `jira-to-ontology` skill, then let the agent **run evals, read its own failures, rewrite its own skill, and re-test**. The result is a version leaderboard.

**Showcase:** a README chart of eval score by skill version (v1 → v5) and a diff of what the agent changed in itself and why.

**Prompts:**
1. `Use skill-creator to package Project 2 as jira-to-ontology. Build an eval set: 3 Apache projects (KAFKA, SPARK, CASSANDRA) with hand-checked expected entities for 20 tickets each.`
2. `Run the loop up to 5 times: run evals → analyze failures → edit the skill → re-run. Save each version and score to skills/jira-to-ontology/versions/. Stop when the score plateaus. Show me the leaderboard.`

**Why:** skills are how you scale yourself across the company. A skill that tunes itself against evals is the most advanced pattern in this set.

**Agentic check:** agent modifies its own instructions ✔ measured improvement loop ✔ stopping criterion ✔

| Term | Meaning |
|---|---|
| **Skill** | A packaged folder of instructions and scripts that Claude loads when a task matches. |
| **Trigger description** | The summary Claude uses to decide *when* to use a skill. |
| **Progressive disclosure** | Claude reads only a skill's summary until it's needed. This saves context. |
| **Plateau / stopping criterion** | The rule for when to stop iterating (the score stops improving). |

---

## Project 9: Ontology Radio (an autonomous weekly audio briefing)
**Unconventional angle:** this plays to your audio-engineer side. Every week, with nobody at the keyboard, the agent pulls new tickets, updates the ontology, writes a 3-minute briefing script, **renders it to audio with local TTS, masters it** (high-pass 80 Hz, light compression, loudness normalized to −16 LUFS for podcasts), and publishes it as a podcast feed on Pages.

**Showcase:** a playable episode on the Pages site, a podcast RSS feed, and the scheduled workflow file.

**Prompts:**
1. `Make the pipeline incremental: last-run timestamp, fetch only new/changed tickets, extract + verify only those, merge, and write ontology/changes/YYYY-MM-DD.md.`
2. `Write a briefing script from the changes (3 min, radio style, "new this week / rising risks / one deep dive"). Render it with a local TTS engine (e.g. piper), then master with ffmpeg: highpass 80Hz, gentle compression, loudnorm to -16 LUFS / -1.5 dBTP. Verify loudness with ffmpeg's ebur128 measurement, then publish to docs/radio/ with an RSS feed.`
3. `Show me how to run all of this headless (claude -p), then schedule it weekly with /schedule or a GitHub Action. Add a hook that runs ontology verification whenever ontology.json changes.`

**Why:** this is fully unattended *Monitor → Act*, and the loudness check shows the agent verifying *technical quality*, not just text.

**Agentic check:** unattended ✔ multi-modal output ✔ technical self-verification (LUFS) ✔ guardrails (hooks) ✔

| Term | Meaning |
|---|---|
| **Headless mode** | Running Claude from a script (`claude -p "..."`) with no chat. |
| **Scheduled routine / cron** | A job that runs automatically on a timetable. |
| **Incremental / idempotent** | Process only what's new, and be safe to run twice without duplicating anything. |
| **Hook** | A rule in Claude Code settings that runs a command automatically on an event. |
| **Guardrail** | A mechanism that keeps an agent within safe, correct bounds. |
| **LUFS** | Loudness Units relative to Full Scale: perceived loudness. −16 LUFS is the usual podcast target. |

---

## Project 10 (capstone): The Agentic Playbook as an installable plugin marketplace
**Unconventional angle:** the playbook isn't just a document you read. It's a set of **skills you install**. Anyone runs `/plugin marketplace add <your-github>/agentic-orchestrator` and gets your patterns as working skills: `jira-to-ontology`, `stakeholder-council`, `friction-radar`, `intake-interview`, and so on.

**Showcase:** the marketplace install command at the top of your README, plus a playbook site on Pages where each pattern page links to its skill.

**Prompts:**
1. After each project: `Review this session, NOTES.md, and git log. Write playbook/<pattern>.md: pattern, when to use it, prompts that worked, failures, vocabulary. Commit.`
2. `Build an intake-interview skill: it interviews a requester (goal, inputs, output, frequency, reviewer), picks the matching playbook pattern, and drafts a project brief.`
3. `Package all skills as a Claude Code plugin marketplace in this repo. Test it by installing from GitHub in a fresh folder and running one skill. Publish the playbook site to Pages.`

**Why:** this is your job description made real. You're the person whose patterns everyone else installs.

**Agentic check:** agent documents its own history ✔ packages and distributes ✔ tests the install end-to-end ✔

| Term | Meaning |
|---|---|
| **Plugin** | A bundle of skills, commands, agents, hooks, and MCP servers, installable in one step. |
| **Plugin marketplace** | A repo that lists plugins so others can browse and install them. |
| **Intake / scoping** | Turning a vague request into a clear goal, inputs, outputs, and success criteria. |
| **Pattern** | A reusable shape of agentic work (Gather, Extract→Structure, Fan-out→Merge, Critique→Revise, Monitor→Act, Triage→Route). |

---

## Bonus ideas for later
- **Ticket time-traveler:** ask any past ticket "what happened to you next?" and it narrates its own lifecycle from the changelog.
- **Jargon decoder for new hires:** a browser tool where you highlight any internal term and the ontology MCP explains it with examples.
- **Counterfactual postmortems:** agents replay a major incident's tickets and propose where the right knowledge could have prevented it.
- **Cross-project DNA:** compare ontologies of 5 Apache projects to find universal failure modes versus culture-specific ones.

## What happens when you approve
I run **Project 0** with you (you'll need `gh auth login` first; run it with `! gh auth login`), then coach you through Project 1. You type each prompt, and I explain what the agent is doing and why.

## Verification per project
Each project is "done" when:
1. Its README is complete using the template.
2. A demo (GIF or live Pages link) works.
3. Its agentic-check items are visible in the tool trace.
4. A playbook entry is committed and pushed.
