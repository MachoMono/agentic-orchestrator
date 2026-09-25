# The Agentic Orchestrator's Field Guide

A living guide to directing AI agents well. It grows with every project: each principle is something learned by doing, with the project where it came from.

**How to read it:** Part 1 is the mindset. Parts 2–6 are the craft. Part 7 is the pattern library. Part 8 is the glossary. Skim the **bold rules**. Read the details when you need them.

---

## Part 1: The mindset

### What "agentic" actually means
Chat is when you ask, the AI answers, and *you* do the work. **Agentic** is when you give a **goal** and the agent **plans → uses tools → observes results → adjusts → verifies its own work**, and you step in only at checkpoints.

**The five-trait test.** Is a task really agentic?
1. **Goal, not instructions:** you state the outcome, and the agent works out the steps.
2. **Tool use:** it acts on the world (runs commands, calls APIs, reads and writes files, opens a browser).
3. **Loop:** act → observe → adjust, over many steps without you.
4. **Self-verification:** it checks its own output against a concrete standard.
5. **Human checkpoint:** you approve at the high-judgment moments, and only those.

### Your job as orchestrator
You are not the one doing the work, and you are not a passive requester either. You **design the work**: set the goal, define "done", choose the pattern, pick the models, place the checkpoints, and make the judgment calls only a human should make. *(P0–P2)*

---

## Part 2: Directing an agent

### The agentic brief
**Rule: a good prompt is a brief, not a request.** It has six parts: *(P1)*

| Part | What it does | Example |
|---|---|---|
| **Goal** | The outcome, not the steps | "A validated dataset of ~1,000 KAFKA issues in data/raw/" |
| **Definition of done** | Checks the agent can test itself against | "VALIDATION.md shows 0 duplicates, even spread, 3 spot-checks match" |
| **Authority** | What it may decide without asking | "When a check fails, diagnose, fix and re-run without asking me" |
| **Constraints** | Lines it must never cross | "Max 1 request/second. Public data only." |
| **When to stop and ask** | Exactly when to come back to you | "Only if the API blocks us or you'd need to change the goal" |
| **Report** | What to tell you at the end | "Summarize every problem you hit and how you fixed it" |

### Plan mode
**Rule: separate deciding from doing on anything non-trivial.** Press Shift+Tab to enter plan mode. The agent researches and proposes, and it can't change anything until you approve. Cheap mistakes get caught at the plan stage. *(P1)*

### `/goal`: an enforced finish line
`/goal <condition>` makes a **separate check** after every turn decide whether the condition is met. If it isn't, the agent is sent back to work. *(P1)*
- **The brief says *how*; `/goal` makes sure it gets *done*.** Use both.
- **Always include an escape clause:** "…OR you have reported a blocker that needs my decision." Otherwise it pushes the agent past points where it *should* stop, and burns tokens.
- **Write conditions that can be checked from what the agent prints** ("every check PASS"), not vibes ("the data is good").

### "Verify it" is the most valuable phrase you can add
**Rule: never let "done" be the agent's opinion.** "Verify the site loads", "re-fetch 3 at random and compare", "validate counts and duplicates". Without that phrase, the agent stops at "I enabled it". *(P0, P1)*

### Preflight checks
**Rule: before a long run, check the blockers first.** Auth, identity, name conflicts, API access. We found a missing git identity before it broke a push. *(P0, P1)*

---

## Part 3: Cost, context and models

### Tokens and cost
- A **token** is about ¾ of a word. You pay (or use up your limit) for everything the model **reads** and **writes**.
- **Rule: scripts move bulk data; the agent makes decisions.** In P1, 2.3M characters of tickets went straight to disk through a script, and the agent only read the summaries. The same job done "through the chat" would cost more than 100×. *(P1)*
- **Rule: trim before an agent reads.** Stripping code blocks and stack traces and capping comment length cut reading cost by **66%** (586K → 199K tokens) without losing meaning. *(P1)*
- Check your usage with `/cost` or `/usage`.

### Context engineering
The **context window** is everything the model can "see" at once. It's limited, and quality drops as it fills with noise. **Rule: give each agent exactly what it needs and nothing more.** That's why each extraction agent read *only* the schema, the vocab and its own batch. *(P2)*

### Model routing
**Rule: match the model to how much judgment the task needs, not how important it feels.** *(P2)*

| Model | Strength | Use for |
|---|---|---|
| **Haiku** | Fast, cheap | Classifying, simple lookups, formatting, routing |
| **Sonnet** | The workhorse | Extraction, summarizing, most coding, rule-following bulk work |
| **Opus** | Strongest reasoning | Planning, schema design, critique, messy judgment calls |

- **Subagents inherit the parent session's model unless told otherwise.** Don't leave it to chance.
- Three ways to control it: say it in the prompt (one-off) · a rule in CLAUDE.md (every session) · a **custom subagent** in `.claude/agents/<name>.md` with `model:` in its header (a fixed model per role).
- In P2: 9 extraction agents on **Sonnet** (about 1.1M tokens of rule-following work), 1 critic on **Opus** (skeptical judgment).

---

## Part 4: Multi-agent orchestration

### Fan-out → merge
**Rule: when work is big and splittable, split it across parallel agents, then merge.** Each **subagent** gets a fresh, focused context, so ticket #127 gets the same attention as ticket #1. *(P2)*

**What makes the merge work:**
- **Shared instructions in a file** (`EXTRACTION_PROMPT.md`), not repeated in each prompt. Every agent gets identical rules.
- **Canonical IDs** (`system:broker`, `failure:hang-stuck-state`) so 8 agents working separately still name the same thing the same way.
- **A merge script that enforces the rules**: it checks evidence, domain/range and vocabulary automatically.

### Pilot first, then scale
**Rule: test the process on a small sample before the full run.** The 40-ticket pilot (≈80K tokens) found 2 instruction gaps and 1 checker bug. Finding them after the full run would have meant re-running 8 agents. *(P2)*

### Same instructions, different agents, different results
Eight agents with identical rules skipped between **2 and 35** tickets each. Some were too strict, and one "folded" tickets into evidence loosely. **Rule: expect drift across parallel agents, and measure it** (coverage per batch) rather than trusting the reports. *(P2)*

### Gap-fill passes
**Rule: measure what the first pass missed, then target only the gaps.** Don't re-run everything. 131 uncited tickets went to 1 agent with a stricter rule, and coverage went 87% → 100%. *(P2)*

### Critic agents (Draft → Critique → Revise)
**Rule: the builder shouldn't grade its own work.** A separate reviewer with a fresh context doesn't share the builder's blind spots. The critic **proposes**, a human **approves**, and only then does anything get applied. *(P2)*
- **Make fixes machine-applicable.** The critic writes `review.md` (checkboxes for the human) *and* `review_fixes.json` (the same fixes as data), so approval → application is mechanical, not a re-interpretation.
- **Order matters when applying fixes:** drops and remaps first (they use the original IDs), merges last (they rename IDs).
- In P2 the critic proposed 85 fixes: 31 duplicate merges, 31 remaps, 17 drops. My prediction that it would recommend a schema change was wrong: every violation fit the existing schema once remapped. Good critics correct the orchestrator too.

---

## Part 5: Quality and verification

### Fix the cause, never weaken the test
**Rule: when a check fails, find out *why* before changing anything.** In P1 a spot-check failed on dates. The easy fix was to delete the check. The real cause was that one API endpoint drops milliseconds. We fixed the *comparison* and kept the check strict. *(P1)*

### Investigate every alarm before acting on it
**Rule: an alarm is a question, not a verdict.** In P2, "369 hallucinated citations" turned out to be one agent writing `13270` instead of `KAFKA-13270`, and 20 "schema violations" were bugs in *my own checker*. Blindly deleting the flagged data would have thrown away **155 real facts**. *(P2)*

### Your checker can be wrong too
**Rule: when a validation fails, suspect the validator as well as the thing it validates.** Two of P2's biggest alarms were checker bugs. The agent that did the work was fine. *(P2)*

### Grounding and evidence
**Rule: every claim cites its source.** Evidence makes facts checkable and reduces **hallucination**. Watch for **evidence padding**: citing sources that don't really support a claim, just to raise coverage. *(P2)*

### Spot-checks
Re-verify a **random sample** against the source of truth. Cheap, and it catches what summary stats miss. *(P1, P2)*

### Confidence labels are a triage signal
**Rule: ask agents to label their confidence, then spend your review time where confidence is low.** In P2 the critic found **80%** of high/medium facts fully supported (and 0 unsupported), but only **25%** of low-confidence facts. The labels were honest, so review effort goes where the risk is. *(P2)*

### Verify the critic too
**Rule: nobody's output is trusted unchecked, reviewers included.** Before presenting the critic's findings, spot-check 2–3 of its claims against the source. In P2 both checked claims held up (duplicate IDs exist; 6 of 8 "evidence" tickets never mention the controller). *(P2)*

### Harvest structured facts; don't make agents guess them
**Rule: if a fact exists as a field in the source system, collect the field.** Don't ask an agent to infer it from prose. P1 didn't harvest Jira's `fixVersion`, so P2 agents had to guess releases from text, and 4 of 23 release links had no support. Structured data is cheaper and more accurate than extraction. *(P2)*

### Passing checks ≠ true facts
Mechanical checks (format, schema, counts) passing doesn't mean the content is right. **Rule: after the numbers pass, read a handful of real outputs yourself.** *(P2)*

---

## Part 6: Knowledge management craft

### Ontology basics
- **Ontology:** a formal model of a domain: the *types* of things, how they *relate*, and the rules.
- **Tickets are evidence, not entities.** Sources support facts. They aren't facts themselves. *(P2)*
- **Few types, rich attributes:** one `Interface` type with `kind: api|config|metric` beats five separate types. *(P2)*
- **Controlled vocabularies** for anything you want to count (Failure Mode, Business Impact). Otherwise you get 200 phrasings of "it hangs". *(P2)*
- **Roles, not people.** Model functions, and keep individuals in the raw data. *(P2)*
- **Every fact has a time,** which lets you see how knowledge evolves. *(P2)*

### Schema-first
**Rule: design the schema on a sample, get a human to approve it, then extract.** Business judgment lives in the schema. That's the human's highest-value contribution. *(P2)*

### RAG vs GraphRAG
- **RAG (retrieval-augmented generation):** find the relevant documents, then answer from them.
- Basic RAG finds text by *similarity* (**embeddings** in a **vector database**). It's good for "find text about X".
- **GraphRAG** walks the *relationships* in a knowledge graph. It's good for multi-hop questions like *"what business impact follows if the Controller fails?"*. It's your specialty path. *(P1 discussion, P4)*

### Sampling
- **Stratified sampling:** split the data into groups (quarters) and sample each evenly, so no period dominates. *(P1)*
- **Seeds** make "random" reproducible. Same seed, same sample. *(P1)*

---

## Part 7: Pattern library

| Pattern | Shape | When to use | Seen in |
|---|---|---|---|
| **Gather** | Fetch → validate → store | Getting raw material out of a system | P1 |
| **Extract → Structure** | Unstructured text → schema-shaped facts | Turning documents into data | P2 |
| **Fan-out → Merge** | Split → parallel agents → combine | Big, splittable work | P2 |
| **Draft → Critique → Revise** | Build → independent critic → human-approved fixes | Anything where quality matters | P2 |
| **Pilot → Scale** | Small trial → fix → full run | Before any expensive run | P2 |
| **Measure → Gap-fill** | Measure coverage → target only the misses | After any bulk pass | P2 |
| **Monitor → Act** | Scheduled check → action → report | Ongoing upkeep | *P9 (coming)* |
| **Triage → Route** | Classify → send to the right workflow | Incoming requests | *bonus idea* |

---

## Part 8: Glossary

| Term | Meaning |
|---|---|
| **Agent** | An AI that pursues a goal by choosing and using tools in a loop |
| **Agentic loop** | Think → act → observe → repeat until done |
| **Background agent** | A subagent working in parallel while the main conversation continues |
| **Canonical ID** | The single official identifier for a thing, so separate agents name it the same way |
| **Checkpoint (data)** | Saved progress so an interrupted run resumes instead of restarting |
| **CLAUDE.md** | A file Claude reads at the start of every session in that folder: standing instructions |
| **Context window** | Everything the model can see at once |
| **Controlled vocabulary** | An approved list of terms so everyone labels things the same way |
| **Custom subagent** | A reusable agent definition (`.claude/agents/*.md`) with its own instructions, tools and model |
| **Domain / range** | Which entity types a relationship may start from and point to |
| **Entity resolution** | Deciding when two names mean the same real thing |
| **Escape clause** | A condition that lets an agent stop properly instead of looping forever |
| **ETL** | Extract, transform, load: pull data, clean it, store it |
| **Eval** | A repeatable test that scores an AI workflow |
| **Evidence padding** | Citing sources that don't really support a claim, to inflate coverage |
| **Exponential backoff** | On errors, wait 2s, 4s, 8s… before retrying |
| **Fan-out** | Splitting one job across many agents running at once |
| **False positive** | An alarm when nothing is actually wrong |
| **Grounding** | Tying every claim to a checkable source |
| **Hallucination** | Plausible-sounding output that isn't supported by any source |
| **Human-in-the-loop (HITL)** | Designed pause points where a person approves before the agent continues |
| **Evidence audit** | Checking a sample of facts against their cited sources: supported / weak / unsupported |
| **Idempotent** | Safe to run twice: no duplicates, no damage |
| **Independent evaluator** | A check separate from the worker, so the agent isn't grading its own homework |
| **Model inheritance** | Subagents default to the parent session's model |
| **Model routing** | Sending each task to the model best suited to it |
| **Ontology** | A formal model of a domain: types, relationships, rules |
| **Pagination** | Getting API data page by page |
| **Pilot run** | A small trial that tests the process before scaling |
| **Plan mode** | The agent proposes a plan and can't act until you approve |
| **Polling** | Checking repeatedly until something is ready |
| **Preflight check** | Confirming prerequisites before starting |
| **Prompt iteration** | Improving instructions based on what actually went wrong |
| **RAG / GraphRAG** | Retrieve then answer; GraphRAG retrieves by walking relationships |
| **Rate limiting** | Pacing requests so you don't overload a server |
| **Root-cause fix** | Fixing why a check failed, not deleting the check |
| **Schema** | The defined shape of data |
| **Seed** | A fixed starting number that makes "random" reproducible |
| **Self-verification** | The agent checks its own result against a concrete test |
| **Stop condition** | The test that decides when an agent's loop may end |
| **Stratified sampling** | Sampling each group evenly so none dominates |
| **Subagent** | A separate agent with its own clean context, launched for a sub-task |
| **Token** | ~¾ of a word. The unit of LLM reading, writing and cost |
| **Tool call** | One action an agent takes (a command, a file write, a fetch) |
| **Triple** | A fact as subject → predicate → object |
| **Truncation** | When a service silently returns only part of the data |
