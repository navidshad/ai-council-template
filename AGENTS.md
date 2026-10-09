# AGENTS.md — AI Council Decision Workflows

> **Template repo — run setup first.** Before you use the council, initialize the repo for your product. Run **Workflow 0 — Setup**: an agent interviews you (or reads a pitch / PRD you paste) and fills in the whole template — personas, docs, and the placeholders. See `SETUP.md` for the routine. (Prefer to fill it in by hand? The placeholder list is in `README.md` → "Make it yours".)

This file is the **single source of truth** for how AI agents run the decision-making workflows in this repo. It is the cross-tool standard: **Claude Code**, **Gemini CLI**, **Antigravity**, and **Cursor** all read it. The thin per-tool files point back here:

- `CLAUDE.md` — Claude Code pointer + Claude Code spawning notes.
- `GEMINI.md` — Gemini CLI **and** Antigravity pointer + their spawning notes.
- `.gemini/agents/*.md` — the personas as native Gemini CLI subagents.

If a per-tool file and this file disagree on *workflow*, this file wins. The per-tool files only add *how to spawn agents in that tool* — never new rules.

---

## What this repo is

This repo is the **living product documentation** for `<PRODUCT_NAME>` — `<ONE_LINE_PITCH>`. The repo holds no product code. It is the source of truth for product strategy, technical architecture, marketing, metrics, and user-facing docs. The one exception is `studio/`, once it exists: the source of the marketing films, stills and slides. Agents build marketing pieces there (Workflow 4).

Every request flows through up to three stages — **triage** (is this trivial or a real decision?), then **depth** (how hard do we think?), then **output** (which record do we write?). The job of this file is to route the request through that flow and pick the cheapest path that does the job.

See `README.md` for the project pitch. See `docs/README.md` for the documentation map.

---

## Code repos are read-only for AI agents

AI agents may **read** the code repos for this product to audit, answer questions, ground a deliberation, or prepare tasks. They must **never edit code**: no file changes, no commits, no merges, no pushes in a code repo.

When an agent finds a code gap or bug, the output is:

1. a **task in your tracker** describing the change (preview with the owner first), and/or
2. a **doc update** in this repo if a living doc is stale.

Engineering changes are made by the team — not by agents. This applies to every tool (Claude Code, Gemini CLI, Antigravity, Cursor).

`studio/` in **this** repo is not a code repo in this sense. It is marketing source, and agents may edit it, render from it and commit to it, through a branch and a pull request (Workflow 4).

> Delete this section if your repo has no separate code repos, or loosen it to fit your setup.

---

## Writing style — the house style

> This is the **house style** for this repo. The default below is "plain, simple English" because it travels well and keeps docs readable for everyone, including non-native speakers. Replace this section if your project needs a different voice.

Write in plain everyday English. Both **chat replies** AND **product docs** (PR/FAQs, ADRs, council syntheses, living docs) should use it:

- Short sentences, one idea per sentence where possible.
- Common words. Avoid academic or business jargon (e.g. *ego-syntonic*, *load-bearing*, *decontextual*, *leverage* as a verb, *surface* as a verb, *thin sliver*, *addressable population*).
- Prefer short Anglo-Saxon words over long Latin ones: *use* not *utilise*, *help* not *facilitate*, *show* not *demonstrate*, *stop* not *discontinue*.
- Idioms and metaphors only if they are very common.
- Light bullets and numbered lists are fine when listing options.

Professional structure stays — formal headings, clear sections, neutral tone. "Professional" means clear and accurate, not dense or academic.

**Carry this into every subagent prompt.** When spawning a critic pass, a council lens, or a single-lens consult, include this writing-style instruction in the agent prompt. Without it, agents drift into academic English by default. (The native Gemini CLI subagents in `.gemini/agents/` already carry this in their system prompt.)

---

## How a request flows — think first, then choose the output

Every request goes through up to three stages. Cheap requests stop early; only real decisions reach the later stages. The key idea: **how hard you think (depth) and what record you write (output) are two separate choices.**

> **Precondition — is the repo initialized?** If template placeholders like `<PRODUCT_NAME>` still appear in the repo, it has not been set up yet. Run **Workflow 0 — Setup** (see `SETUP.md`) before any council / PR/FAQ / ADR work — the council needs real product facts to reason well.

### Stage 1 — Triage (always; cheap)

Read the request and sort it:

- **Trivial** — typo, formatting, file move, factual lookup, a clear single-answer question. Just do it or answer it. No agents, no doc. Stop here.
- **A real decision** — something a future reader will want the reasoning for. Go to Stage 2.

If you cannot tell which path fits, ask the user one short question. A wrong-tool deliberation is worse than a one-line clarifying question.

### Stage 2 — Depth (how hard do we think?)

Pick the lightest depth that does the job:

- **One lens** — one expert is clearly enough (e.g. a technical-only choice → the Technical Architect persona).
- **Council (many lenses)** — the decision is strategic or cross-functional (pricing, kill, pivot, sequence, go-to-market), or it would change a living doc (`docs/product/prd.md`, `docs/product/roadmap.md`, `docs/tech/architecture.md`, `docs/marketing/brand.md`). Default to the **2 most relevant** lenses and escalate only if a gap shows up. The council is for the few truly strategic calls per quarter, not the weekly question.

### Stage 3 — Output (which record do we write?)

Pick the record shape that fits the question. The shape is independent of the depth — a one-lens think can still produce a PR/FAQ, and a council can feed a PR/FAQ or an ADR.

| Question shape | Output | Lives in | Procedure |
|---|---|---|---|
| Should we **build** this feature? | **PR/FAQ** | `decisions/pr-faq/` | Workflow 2 |
| Which **technical option** do we pick? | **ADR** | `decisions/adr/` | Workflow 3 |
| What is the **strategic, cross-functional call**? | **Council synthesis** | `decisions/council/` | Workflow 1 |
| Make a **marketing video**, still, cover or slide deck | **Studio piece**: source in `studio/`, a row in `studio/videos.md` | `studio/` | Workflow 4 (`STUDIO.md`) |
| Trivial (typo, lookup, file move) | direct edit / answer | wherever it belongs | — |

Each procedure below (Workflows 1–3) is the common pairing of a depth with an output: the council procedure pairs many lenses with a synthesis; the PR/FAQ procedure pairs one critic lens with a feature doc; the ADR procedure pairs one architect lens with a technical doc.

**Rules**

1. Default to the cheapest path that does the job. Don't reach for the council when one lens is enough.
2. Outputs can chain. A PR/FAQ that surfaces real cross-functional tension escalates to a council. An ADR with product-strategy stakes escalates to a council. A council decision often spawns PR/FAQ or ADR follow-ups. The cheap-to-expensive direction is the common one.
3. Every output ends by appending a one-line entry to the **Decision Log** at the bottom of `docs/README.md`. The log is a thin table of contents — it points to the permanent file (PR/FAQ, ADR, or council synthesis) where the full rationale lives. See "Records and history" below.

---

## How to spawn personas (per tool)

The workflows below say "spawn a lens" or "spawn a critic." How you spawn depends on the tool. The persona content is the same everywhere; only the mechanism differs.

- **Claude Code** — spawn each persona with the **Task** tool (`subagent_type: "general-purpose"`), reading `agents/<role>.md` verbatim into the prompt. Spawn in parallel: one message, several Task calls. See `CLAUDE.md`.
- **Gemini CLI** — the personas are **native subagents** in `.gemini/agents/*.md` (names: `product-manager`, `ux-designer`, `technical-architect`, `business-strategist`). The main agent calls each as a tool, or you force one with `@product-manager`. Each runs in its **own isolated context** — independence is guaranteed. They may run one after another, not truly at the same time; that is fine, isolation gives the same independent reasoning. **A Gemini subagent cannot call another subagent.** So the **main agent** always does the synthesis — never ask a subagent to synthesize or to read another subagent. See `GEMINI.md`.
- **Antigravity** — no native subagent files needed. Spawn each persona in the **Agent Manager** as a separate agent, pasting the persona file (`agents/<role>.md`) plus the grounding pack into the prompt. Run them as parallel agents. The main agent synthesizes. See `GEMINI.md`.

`agents/*.md` is the canonical, human-readable persona source (used verbatim by Claude Code and Antigravity). `.gemini/agents/*.md` is the same content compiled into Gemini CLI's native subagent format. **If you change a persona, update both `agents/<role>.md` and `.gemini/agents/<role>.md`.**

Track multi-step workflows with your tool's todo / task list (TodoWrite in Claude Code, the todo/plan view in Gemini CLI, the task list in Antigravity).

---

## Records and history

The repo's memory is layered. Each layer has a different job — keeping them separate avoids duplication and drift.

- **Permanent files** (`decisions/pr-faq/`, `decisions/adr/`, `decisions/council/`) — the full reasoning behind each decision lives here. PR/FAQs, ADRs, and council syntheses are committed and never rewritten after acceptance. To change a decision, write a new file that supersedes the old one.
- **Living docs** (`docs/product/prd.md`, `docs/product/roadmap.md`, `docs/tech/architecture.md`, `docs/marketing/*`, etc.) — the current state of the product. These get edited as decisions land.
- **Git history** — the source of truth for *what changed and why*. Use rich commit messages with prefixes (`Council:`, `PR/FAQ:`, `ADR-NNN:`) and put the headline rationale in the message body. `git log --grep="^Council:"` is the chronological view of council decisions.
- **Decision Log** in `docs/README.md` — a thin one-line-per-entry table of contents that points to the permanent file. The log makes decisions discoverable; it does NOT duplicate rationale. If the log and a permanent file disagree, the file wins.
- **Ephemeral scratch** (`.council-temp/session_<id>/`) — gitignored. Per-agent perspective files are deleted after the synthesis is written. Only the synthesis is promoted to a permanent file.

**What NOT to keep:** session transcripts, agent reasoning logs, intermediate drafts. They age badly and the synthesis already captured the verdict.

---

## Workflow 0 — Setup (run once)

Use this the first time you open a fresh clone of the template, or whenever the product changes a lot. The goal: replace every placeholder with real product facts so the lenses reason from truth, not from `<...>` tokens.

Setup is a **main-thread routine** — an interview plus a bulk edit, not a council deliberation. In short:

1. **Detect.** If `<PRODUCT_NAME>` still appears anywhere in the repo, it is not set up. Offer to run setup before any other workflow.
2. **Interview.** Use the initializer prompt in `SETUP.md`. Ask in small batches. If the user pastes a pitch / PRD / link, read it first and ask only for what is missing.
3. **Fill in.** Apply the fill-in map in `SETUP.md`: product name and pitch everywhere, the four persona Context blocks (and their Gemini mirrors), and the `docs/` skeleton. Add a 5th domain lens if the user wants one.
4. **Finalize.** Remove the template banners, confirm no `<...>` tokens remain, and commit with `Setup: initialize council for <PRODUCT_NAME>`.

The full question set, the fill-in map, and the finalize steps live in **`SETUP.md`**. Follow that file — this section is the pointer.

---

## Workflow 1 — Council (cross-functional strategic decisions)

Use when the question is **strategic, cross-functional, or would change a living document**. Typical triggers:

- "ask the council …", "what does the council think …", "council, deliberate on …"
- "should we kill / pivot / re-sequence …"
- "how should we price / position …"
- any proposed change to `docs/product/prd.md`, `docs/product/roadmap.md`, `docs/tech/architecture.md`, or `docs/marketing/brand.md`

Do **not** activate the council for: typo fixes, single-feature pitches (use PR/FAQ), tech-only choices (use ADR), or anything where one expert lens is clearly enough.

### The lenses

The personas live in `agents/` (canonical) and `.gemini/agents/` (Gemini-native mirror):

- `agents/product-manager.md` — strategic prioritization, roadmap, user impact
- `agents/ux-designer.md` — UX, interaction patterns, accessibility, design system
- `agents/technical-architect.md` — feasibility, scalability, performance, tech debt
- `agents/business-strategist.md` — monetization, go-to-market, unit economics, competitive position

Each file is the **complete persona prompt** for that agent — never paraphrase, always read and forward verbatim into the subagent (Claude Code / Antigravity). In Gemini CLI the persona is already the subagent's system prompt.

> **Adding a domain lens.** Many products need a fifth, domain-specific lens (e.g. a Security Expert, a Clinician, a Data Scientist, a Learning Scientist). To add one, copy an existing persona file as a starting point, rewrite the Role / Expertise / Persona / Decision Framework for the new domain, and add a Gemini mirror in `.gemini/agents/`. Spawn it **selectively** — only when the topic touches its domain — using the same two-tier discipline as the others.

### Steps

Track these steps with your tool's todo / task list.

**1. Build the grounding pack.** Before spawning any agent, the main thread reads the relevant context once and writes a short grounding block — key metrics from `docs/metrics/framework.md`, recent user feedback the user mentioned, known competitive moves, and any user-supplied context. This block is passed *inline* to every agent so they don't re-read the same source docs. Aim for ≤ 400 words total. Without this, the council reasons in a vacuum and pays the same context cost several times over.

**2. Pick the lenses (two-tier default).** Default to spawning the **2 most relevant** lenses for the topic, not all of them. For each lens, ask: does this lens have material input on this specific decision? If a lens has nothing distinctive to add (e.g. a pure pricing question rarely needs UX; a pure infra-cost question rarely needs the PM), skip it for tier 1 and note why. The skipped lenses are held in reserve and only spawned in step 5 if synthesis surfaces a real gap.

**3. Create a session directory.** Path: `.council-temp/session_<UTC-timestamp>/` (format `YYYY-MM-DD_HH-MM-SS`). The `.council-temp/` directory is gitignored — sessions are ephemeral. Get the timestamp via shell: `date -u +"%Y-%m-%d_%H-%M-%S"`.

**4. Spawn the chosen lenses (independent + concurrent where possible).** Spawn one subagent per chosen lens. They must reason **independently** — never let them read each other's files. Where the tool supports it, run them at the same time (Claude Code: one message with several Task calls; Antigravity: parallel agents in the Agent Manager). In Gemini CLI they may run one after another as separate isolated subagent calls — that still gives independent reasoning. See "How to spawn personas (per tool)" above.

Each agent prompt must:

1. Tell the agent which persona it is. (Claude Code / Antigravity: tell it to read `agents/{role-file}.md` first. Gemini CLI: the persona is already the subagent's system prompt — just give it the task.)
2. Include the grounding pack from step 1 *inline* in the prompt.
3. State the deliberation topic clearly with all relevant context.
4. Point the agent at **1–2 specific files** to consult before writing — not whole folders. If the grounding pack already covers it, skip the file read.
5. Tell them to write their response to `.council-temp/session_<id>/<role>.md` using the format below, **and** to report back a one-paragraph summary + confidence number.
6. Tell them to stay in character, end with a confidence rating (1–10), and NOT to read the other agents' files.

#### Subagent prompt template

```
You are the {ROLE} on the <PRODUCT_NAME> AI Product Council.

Step 1 — Persona. (Claude Code / Antigravity: read your persona file agents/{role-file}.md and adopt that voice and decision framework. Gemini CLI: you already are this persona.)
Step 2 — Read for context (only these files, not whole folders): {1–2 specific paths}. If the grounding pack below already covers what you need, skip this step.
Step 3 — Use the grounding pack below as current state. Do not re-read what is summarised here.

GROUNDING PACK:
{paste the inline grounding block from step 1}

Step 4 — Deliberate on: {full topic + user-provided context}.
Step 5 — Write your perspective to: .council-temp/session_{id}/{role}.md

Use this exact structure:

# {Role} Perspective

**Request**: {topic}
**Time**: {UTC timestamp}

## Analysis
{your reasoning from your discipline's lens}

## Recommendation
{concrete recommendation — be opinionated}

## Pre-mortem
{imagine this decision fails 6 months from now — what is the most likely cause?}

## Questions/Concerns
{open questions, risks, things you'd want to validate}

## Confidence
{1–10 — how confident are you in your recommendation, and why? One sentence.}

Stay strictly in your discipline's lens. Do NOT read the other agents' session files — independent perspectives are the point. Report back with a one-paragraph summary of your recommendation and your confidence number.

**Writing style.** Write your perspective AND your reply to the main thread in plain everyday English — short sentences, common words, no academic jargon (this is the repo house style; see AGENTS.md → "Writing style"). Professional structure stays (headings, sections, neutral tone) but the language must be easy to read. Prefer short Anglo-Saxon words over long Latin ones.
```

**5. Synthesize. Escalate only if gaps appear.** The **main agent** reads the perspective files written in step 4 (in Gemini CLI, also use the summaries each subagent returned). Write `.council-temp/session_<id>/synthesis.md` using the verdict-doc structure from `.council-temp/README.md` (Decision, Sequence, Why, Open Issues, Action Items — omit any section with no substance). Target ≤300 words for the body (canonical tables / copy that downstream living docs will reuse are exempt from the word target — they are the source of truth, not deliberation residue).

The synthesis is a **verdict doc, not a transcript**. Write it as if the per-agent files don't exist — because for the future reader, they don't. Do not include a Perspectives Summary, an Areas of Agreement list, or any section that just restates what the Decision already says. Disagreements that actually shaped the verdict go into a one-sentence note inside `## Why` or into `## Open Issues`; "no hard disagreements" is not a section, it is a sign to omit the section.

If during synthesis you identify a gap that one of the *unspawned* lenses would fill (e.g. "we have no read on technical feasibility"), spawn that lens now using the same template and the same grounding pack, then re-synthesize. Record skipped lenses in the commit body, not in the permanent file.

**If two or more agents rated their confidence below 6, flag that as a "go get more data" signal rather than ship.**

**6. Persist the synthesis and update the living docs.** Two parts:

a. **Promote the synthesis to a permanent file.** Move `.council-temp/session_<id>/synthesis.md` to `decisions/council/<NNN>-<slug>.md` (next sequential number, kebab-case slug). The `**Lenses**` field at the top is a single comma-separated line — no justification for skipped lenses inside the permanent file (that belongs in the commit body). The per-agent perspective files stay in `.council-temp/` and are deleted with the session — only the synthesis survives.

b. **Edit the living docs.** For each Action Item in the synthesis, edit the relevant `docs/**/*.md` file directly.

Then append a one-line entry to the **Decision Log** at the bottom of `docs/README.md`:

```
- {YYYY-MM-DD} — Council — {short topic title} — `decisions/council/<NNN>-<slug>.md`
```

Commit with the prefix `Council:` and put the headline decision in the commit message body. The synthesis file + the docs diff + the commit body together are the permanent record. The log entry is just a discoverability pointer; do not duplicate the rationale there.

**7. Report back to the user.** Summarize: what was decided, which lenses ran (and which were skipped, with reasoning), where the agents disagreed and how it resolved, what files changed, and what remains open. Keep it concise — the diffs and decision log entry are the artifacts.

---

## Workflow 2 — PR/FAQ (should we build this feature?)

Use when the question is **"should we build feature X?"** or **"is this idea good enough to put on the roadmap?"**. The PR/FAQ forces you to state user-facing value before any work starts. If you can't write a compelling press release, you don't have a feature — you have an idea.

### Steps

**1. Draft the PR/FAQ.** Copy `templates/pr-faq-template.md` to `decisions/pr-faq/<NNN>-<slug>.md` (next sequential number, kebab-case slug). Fill in every section. Be specific about the user, the problem, the moment of use, and the headline customer benefit. **Release scope is named `Phase 1` / `Phase 2` / `Phase 3` — not `V1` / `V2` / `V3`.** The Phase wording is clearer and avoids confusion with product-version numbers.

**2. Critic pass.** After drafting, spawn ONE subagent whose job is to find the strongest objections. Prompt: "Read `decisions/pr-faq/<file>.md`. You are a skeptical investor reviewing this for fundability. List the three strongest reasons this should NOT be built, the weakest claim in the PR section, and any FAQ answer that is hand-wavy. Be specific and harsh. **Write in plain everyday English — short sentences, common words, no academic jargon** (the repo house style)." Append the critique to the bottom of the PR/FAQ under `## Critic Pass`.

**3. Decide.** Read the critique. Either revise and proceed, set the doc's `Status` to `Rejected` with reasoning, or — if the critique surfaces real cross-functional trade-offs (pricing, positioning, infra cost, go-to-market) — escalate to the council. Set `Status` to `Pending Council` and run Workflow 1 with the PR/FAQ as input context.

**4. Log it.** Append a one-line entry to the **Decision Log** at the bottom of `docs/README.md`:

```
- {YYYY-MM-DD} — PR/FAQ ({Approved/Rejected/Escalated}) — {feature name} — `decisions/pr-faq/<NNN>-<slug>.md`
```

The PR/FAQ file itself is the permanent record — committed to git and part of the product memory, not ephemeral. Commit with the prefix `PR/FAQ:` and put the headline decision in the message body.

---

## Workflow 3 — ADR (architectural decision records)

Use when the question is **a technical/architectural choice with multiple valid options** and you want a permanent record of *why* you picked one. Examples: choosing a database, picking a caching strategy, deciding on a state-management approach, choosing a payment integration.

Do **not** use ADRs for routine implementation choices — ADRs are for decisions a future engineer would want to understand the reasoning behind.

### Steps

**1. Draft the ADR.** Copy `templates/adr-template.md` to `decisions/adr/<NNN>-<slug>.md` (next sequential number). Fill in: Status, Context (what forces are at play), Decision (what we're doing), Alternatives Considered (with reasons rejected), Consequences (good and bad).

**2. Single-lens review.** The Technical Architect persona is the natural reviewer. Spawn ONE subagent: "Adopt the Technical Architect persona (read `agents/technical-architect.md`, or use the `technical-architect` subagent in Gemini CLI). Then read `decisions/adr/<file>.md`. Critique the decision and the alternatives. Are the trade-offs honest? Is anything missing? Append your critique to the doc under `## Architect Review`. **Write in plain everyday English — short sentences, common words, no academic jargon** (the repo house style)."

**3. Decide.** Revise based on the review. Set Status to `Accepted`, `Rejected`, or `Superseded by ADR-NNN`.

**4. Log it.** Append a one-line entry to the **Decision Log** at the bottom of `docs/README.md`:

```
- {YYYY-MM-DD} — ADR-{NNN} ({Accepted/Rejected}) — {decision title} — `decisions/adr/<NNN>-<slug>.md`
```

ADRs are committed to git. They're never edited after acceptance — to change a decision, write a new ADR that supersedes the old one. Commit with the prefix `ADR-{NNN}:` and put the rationale in the message body.

---

## Workflow 4 — Studio (marketing films, stills and slides)

Use this when someone asks for a marketing piece: a launch or product film, a short clip for social, a video cover, store or launch-gallery images, a slide deck. The full routine lives in **`STUDIO.md`** — this section is the pointer.

**Depth.**
- Most pieces need no lens: `docs/marketing/brand.md` and the studio's design system already hold the rules.
- Ask the **Business Strategist** lens when the piece makes a new public claim, aims at a new audience, or touches price.
- Ask the **UX Designer** lens when a new visual style is proposed.
- A change to the brand itself (the mark, the palette, the voice, the claims in `brand.md`) is a council call.

**In short.**

1. **Set up on first use.** The template ships no studio. The first time a piece is asked for, create `studio/` from `STUDIO.md` §2 — only the parts the piece needs. Later pieces start from the last one.
2. **Brief → story → key frames → silent cut → sound → master**, with the founder approving the brief, the story, the key frames and the review cut (`STUDIO.md` §3.3).
3. **Publish private.** Only the founder makes an upload public. Every upload gets a row in `studio/videos.md`.
4. **Commit the source** on a branch with a pull request, prefix `Studio:`. Never commit a video.

Studio pieces need no Decision Log entry unless they carry out a decision. Their log is `studio/videos.md`.

---

## Editing rules for living docs

- **Roadmap, PRD, architecture, brand** — never edit these without a council deliberation. They are the strategic spine.
- **Metrics framework, feature specs, marketing tactics** — single-lens edits are fine if the user is clear, but flag if a strategic shift is implied.
- **User-facing docs (`docs/user-docs/`), getting-started, terms** — treat as legal/customer-facing; edit only with explicit user instruction.
- **The studio design system (`studio/design-system/`)** — refining a style or adding one is a single-lens edit with the founder's OK. A change that alters the brand (the mark, the palette, the voice, the honesty rules) follows `brand.md` and goes through the council.

Always preserve the existing voice and structure of the doc you're editing. The living docs are versioned in git — make commits self-contained and message them like decisions, not edits (e.g., `Council: prioritize onboarding redesign ahead of referrals`, `PR/FAQ: approve saved-search alerts`, `ADR-007: adopt Postgres over DynamoDB`).

---

## Turning decisions into work

When a PR/FAQ, ADR, or council decision turns into engineering work, the work goes into your task tracker. A few light rules keep tasks clean:

- **Lead each task title with a verb and the outcome.** A developer who has never seen this project should be able to read the title and know what to do. No internal acronyms in the title.
- **One task = one ownable piece of work.** A PR/FAQ becomes several tasks, not one. Don't bundle work that spans two code repos into one task — split it into two linked tasks.
- **Always preview the task list with the owner before creating any task.** Nothing lands in the tracker without explicit approval of the name, the description, and the scope.
- **Link each task back to its decision doc** (PR/FAQ, ADR, or council file) so the reasoning is one click away.

> This is deliberately light. If your team wants a strict task convention (fixed scope field, a description template, UX hand-off rules), add it here.

---

## Anti-patterns

- **Defaulting to the council.** It's the most expensive workflow. Use PR/FAQ or ADR when they fit.
- **Spawning every lens by default.** Two-tier is the default — pick the 2 most relevant lenses, escalate to more only when synthesis reveals a real gap.
- **Running chosen lenses sequentially when the tool can run them together.** In Claude Code and Antigravity, spawn the tier in parallel. (In Gemini CLI, isolated subagent calls may run one after another — that is acceptable because isolation already gives independent reasoning.)
- **Skipping the grounding pack.** Without it each agent re-reads the same source docs and you pay the same context cost N times over.
- **Paraphrasing personas.** Read the full persona file each session (or rely on the native subagent system prompt in Gemini CLI).
- **Letting council agents read each other.** Synthesis is the main agent's job, not theirs. (In Gemini CLI this is enforced — subagents cannot call or read other subagents — so never structure the council so a subagent must synthesize.)
- **Skipping the Decision Log entry.** Decisions become hard to find without it. (The permanent record is the doc + commit; the log is the discovery layer.)
- **Duplicating rationale into the log.** The log is a thin table of contents — one line per entry. The full reasoning lives in the permanent file and the commit body.
- **Persisting agent perspectives.** Only the synthesis is promoted to `decisions/council/`. Per-agent perspective files stay ephemeral in `.council-temp/` and are deleted with the session.
- **PR/FAQ without a critic pass.** A beautifully written PR/FAQ for a bad idea is still a bad idea.
- **ADRs that hide alternatives.** The "Alternatives Considered" section is the entire point — without it an ADR is just a memo.
- **Convening any workflow for trivial requests.** Direct edit is fine for typos, formatting, factual lookups, and obvious clarifications.
- **In-chat revision markers on decision docs.** When iterating on a PR/FAQ, ADR, or council synthesis within a single chat, do NOT annotate with "Rev 2", "(after critic pass)", "what was addressed", or any other changelog-style markers inside the doc. Edit the body in place until it reads as a single stable version. Revisions live in git — the commit message body carries "what changed", that is git's job, not the doc's. The Status field stays a single value, no parenthetical version note.
- **Synthesis as transcript.** The council synthesis is a verdict doc, not a record of the deliberation. Do NOT include a Perspectives Summary, an Areas of Agreement list, a Points of Contention section when there is no contention, or any section that just restates the Decision in different words. The per-agent files are deleted with the session — the permanent file must stand alone for a reader who has never seen them.
- **Process-citations inside decision docs.** Inline parentheticals like `(deduplicated)` or `(no revision markers)` are notes-to-self, not part of the decision. The rules they cite already live in this file; re-citing them inside the synthesis is noise for the future reader.
- **Committing a video or render output.** The studio keeps source only; a video is a re-render or a link in `studio/videos.md`.
- **Building a published asset in a scratch folder.** A cover, thumbnail or store image whose source sits in a temp folder is lost when the folder is cleared. Its source goes in `studio/`.
- **Publishing a marketing piece without the founder.** Uploads stay private until the founder makes them public.
- **A film or slide that claims more than the product does.** Check `brand.md` and the honesty rules in `STUDIO.md` §4 before anything is rendered.
- **Justifying skipped lenses inside the permanent file.** The `**Lenses**` field is a single line listing which lenses ran. Why a lens was skipped is a commit-body concern, not a section of the synthesis.
