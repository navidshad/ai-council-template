# GEMINI.md — Gemini CLI & Antigravity pointer

**Read `AGENTS.md` in full before doing anything in this repo.** It is the single source of truth for the decision-making workflows (triage → depth → output; the council, PR/FAQ, ADR and studio procedures; records and history; the writing style; and the anti-patterns). Both Gemini CLI and Antigravity read this file. `AGENTS.md` holds the shared rules; this file adds **only** how to spawn agents in the two Gemini-family tools. It adds no new rules.

> Precedence note (Antigravity): when a rule here conflicts with `AGENTS.md`, this file wins. Nothing here is meant to conflict — these are spawning notes, not rule changes.

---

## First run — set up the repo

If the repo still has `<...>` placeholders (e.g. `<PRODUCT_NAME>`), it is a fresh template. Run the setup routine in `SETUP.md` (**Workflow 0**) before any council work. Setup is a main-thread interview + bulk edit run by the main agent — not a subagent job.

## The shared rule for both tools

The council's whole value is **independent** lenses, then **one** synthesis by the main agent.

- Each persona reasons on its own and must **not** read another persona's work.
- The **main agent** reads the per-agent perspective files in `.council-temp/session_<id>/` and writes the synthesis. A persona never synthesizes.
- This is not just style — in Gemini CLI it is enforced: **a subagent cannot call or read another subagent.** So always keep synthesis in the main agent.

Track multi-step workflows with the tool's todo / plan / task list.

**Studio work (Workflow 4)** is a main-agent job: building scenes and sound is ordinary file work, not a council. The full routine is in `STUDIO.md`.

---

## Gemini CLI

The personas are **native subagents** in `.gemini/agents/`. Gemini CLI auto-loads them. Names:

- `product-manager`
- `ux-designer`
- `technical-architect`
- `business-strategist`

How to run the council:

1. The **main agent** builds the grounding pack (see `AGENTS.md` Workflow 1, step 1) and the session directory `.council-temp/session_<timestamp>/`.
2. For each chosen lens, call its subagent — either let auto-delegation pick it, or force it with `@<name>` (e.g. `@product-manager`). Give it the grounding pack inline, the topic, the 1–2 context files, and tell it to write its perspective to `.council-temp/session_<id>/<role>.md` and report back a one-paragraph summary + confidence.
3. Each subagent runs in its **own isolated context**. They may run one after another rather than at the same time — that is fine; isolation already gives independent reasoning.
4. The **main agent** reads the perspective files (plus the returned summaries) and writes the synthesis. Then promotes it to `decisions/council/` and updates the living docs, per `AGENTS.md`.

For the PR/FAQ critic pass and the ADR architect review, use a one-off subagent with the prompt in `AGENTS.md` (the ADR review can use `@technical-architect`).

Subagent files use YAML frontmatter (`name`, `description`, `tools`) + the persona as the system prompt, and already carry the writing-style rule. **If you change a persona, update both `agents/<role>.md` (canonical) and `.gemini/agents/<role>.md`.**

---

## Antigravity

Antigravity reads both `AGENTS.md` and this `GEMINI.md`. It does **not** use the `.gemini/agents/` subagent files — those are Gemini-CLI-only. Spawn personas through the **Agent Manager** instead:

1. The main agent builds the grounding pack and the session directory.
2. For each chosen lens, start a **separate agent** in the Agent Manager. Paste the persona file `agents/<role>.md` (verbatim) + the grounding pack + the topic + the 1–2 context files into its prompt, and tell it to write its perspective to `.council-temp/session_<id>/<role>.md`. Always include the writing-style block from `AGENTS.md`.
3. Run the chosen lenses as **parallel agents**. Keep them independent — do not let one read another's file.
4. The main agent reads the perspective files and writes the synthesis, then promotes and updates docs per `AGENTS.md`.

> Global-config gotcha: if you also use Gemini CLI on the same machine, both tools share `~/.gemini/GEMINI.md` for *global* rules, so global rules can leak between them. This repo keeps everything **project-level** (files in the repo root), which avoids that conflict. Don't move these workflow rules into `~/.gemini/GEMINI.md`.

---

## Writing style

Plain everyday English — in chat replies, in docs, and in every agent prompt. Full rules are in `AGENTS.md` → "Writing style — the house style".
