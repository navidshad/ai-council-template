# SETUP.md — initialize the council (Workflow 0)

This is the **setup routine**. Run it **once**, right after you clone the template, to make the council fit your product. Instead of editing files by hand, an agent interviews you (or reads a doc you paste) and fills the whole template in.

This routine is run by the **main agent** — it is an interview plus a bulk edit, not a council deliberation. No subagents are needed (one optional self-check at the end can use them).

---

## When to run it

Run setup when **any** of these is true:

- You just cloned the template and the files still contain placeholders like `<PRODUCT_NAME>` or `<ONE_LINE_PITCH>`.
- The user says "set up the council", "initialize", "make it fit my product", or similar.
- An agent is asked to run a council / PR/FAQ / ADR workflow but the repo is **not yet initialized**.

**Detection rule (how an agent knows it is not set up):** search the repo for the token `<PRODUCT_NAME>`. If it still appears in any tracked file, the repo is **uninitialized** — stop and offer to run this setup before doing any other workflow.

```bash
grep -rl '<PRODUCT_NAME>' . --exclude-dir=.git
```

If that returns any file, run setup first.

---

## How to run it

1. **Offer first.** Tell the user the repo is a fresh template and you can set it up for their product. Ask if they want to start.
2. **Take a shortcut if they have docs.** If the user can paste a pitch, a PRD, a website link, or a README, read it first and pull every answer you can. Then ask only for what is missing. This is faster and more accurate than asking everything.
3. **Interview in small batches.** Use the **initializer prompt** below. Ask 3–5 questions at a time, in plain English. Do not dump all questions at once.
4. **Don't block on the unknown.** If the user doesn't have an answer yet, write a short `TODO:` line in the right doc and move on. Setup should never stall.
5. **Confirm, then fill.** Show a short summary of what you captured. When the user approves, apply the **fill-in map**, run the **finalize** steps, and commit.

---

## The initializer prompt

> This is the script the agent follows (and the user can paste it to kick things off). Keep it conversational — it is an interview, not a form.

```
You are setting up this AI Product Council repo for a new product. Your job:
interview me, then fill in the template so the council reasons from real facts.

Rules:
- Ask in small batches (3–5 questions), not all at once.
- If I give you a pitch, PRD, website link, or README, read it first and pull what
  you can. Only ask for what is missing.
- Keep questions short and in plain English.
- If I don't know something yet, write a short TODO line in the doc and move on.

Ask me about, in this order:

Round 1 — Product (required)
- Product name
- One-line pitch (what it is + who it's for)
- Target users (who they are, what they want)
- 3–5 core features or surfaces today
- Anything clearly out of scope for now

Round 2 — Tech
- Stack (frontend, backend, database)
- Main systems or services
- Key integrations (AI, payments, analytics, auth)
- Key constraints (latency, scale, privacy, cost)

Round 3 — Business
- How it makes money (free / paid model)
- Free limits vs. paid benefits
- The few metrics you watch
- Main competitors and what makes you different

Round 4 — Experience
- Design system or component library (if any)
- Visual style in one line
- Known UX gaps

Round 5 — Setup choices
- Keep the plain-English house style, or change it?
- Are there separate code repos the agents should treat as read-only?
  (keep or drop that rule in AGENTS.md)
- Do you want a 5th domain lens beyond the four core ones?
  If yes: name the domain and one line on what it cares about.
- Do you want the docs mirrored into ClickUp? If no, delete `scripts/` and
  `.github/workflows/sync-clickup-docs.yml`. If yes, point them at
  `scripts/README-clickup-sync.md` (they add the token and ids themselves).

After I answer, show me a short summary of what you captured. When I approve,
fill in the files (see the fill-in map in SETUP.md), run the finalize steps,
commit with "Setup: initialize council for <PRODUCT_NAME>", and tell me what changed.
```

---

## Fill-in map (answer → where it goes)

| What you captured | Where to write it |
|---|---|
| **Product name** (replaces `<PRODUCT_NAME>`) | Every file — do a global replace of `<PRODUCT_NAME>`. |
| **One-line pitch** (replaces `<ONE_LINE_PITCH>`) | `AGENTS.md` → "What this repo is"; `docs/marketing/brand.md`; `README.md` intro. |
| **Users · core features · out of scope** | `agents/product-manager.md` Context block **and** its mirror `.gemini/agents/product-manager.md`; seed `docs/product/prd.md`. |
| **Stack · systems · integrations · constraints** | `agents/technical-architect.md` Context block **and** mirror; seed `docs/tech/architecture.md`. |
| **Monetization · limits · metrics · competition** | `agents/business-strategist.md` Context block **and** mirror; seed pricing in `docs/marketing/brand.md` and metrics in `docs/metrics/framework.md`. |
| **Design system · visual style · UX gaps** | `agents/ux-designer.md` Context block **and** mirror. |
| **House-style choice** | `AGENTS.md` → "Writing style". Keep the plain-English default, or replace it with the user's chosen voice. |
| **Separate code repos?** | `AGENTS.md` → "Code repos are read-only". Keep it if yes; delete the section if no. |
| **ClickUp sync?** | If no, delete `scripts/` and `.github/workflows/sync-clickup-docs.yml`. If yes, leave them; the user follows `scripts/README-clickup-sync.md`. Never ask the user to paste a token into chat. |
| **5th domain lens?** | If yes, see "Add a domain lens" below. If no, leave the four core lenses. |

> When you fill a persona Context block, **delete the `> Fill this in...` note** above it and replace the `<...>` lines with real content. Keep these blocks short — the deep detail lives in `docs/`.

---

## Add a domain lens (optional)

If the user wants a 5th lens (e.g. Security Expert, Clinician, Data Scientist, Learning Scientist):

1. Copy `agents/product-manager.md` to `agents/<role>.md` as a starting point. Rewrite Role, Expertise, Persona, Decision Framework, Responsibilities, and the Context block for the new domain.
2. Create the Gemini mirror `.gemini/agents/<role>.md` with matching YAML frontmatter (`name`, `description`, `tools`) and the council-lens + writing-style footer.
3. Add the new lens to the list in `AGENTS.md` → Workflow 1 → "The lenses", to the names list in `GEMINI.md`, and to the council list in `README.md`.
4. Spawn it **selectively** — only when the topic touches its domain (same two-tier rule as the others).

---

## Optional — lens self-check

After the Context blocks are filled, you can ask each lens to sanity-check its own block. Spawn each persona once: "Read your filled Context block in `agents/<role>.md`. Does it read right for this product? Flag anything wrong or missing in one short paragraph." Fix anything they flag. This is optional polish, not required.

---

## Finalize

Once the files are filled:

1. **Remove the template banners.** Delete the "Template repo — run setup first" blockquote at the top of `AGENTS.md`. In `README.md`, replace the "Make it yours" section with a short line: "This repo is set up for `<PRODUCT_NAME>`. Re-run `SETUP.md` if the product changes." Update the README title if you want.
2. **Check nothing is left.** Run the detection grep again — no `<PRODUCT_NAME>` (or other `<UPPER_SNAKE>` tokens) should remain:
   ```bash
   grep -rnE '<[A-Z_]+>' . --exclude-dir=.git
   ```
3. **Commit.** Use `Setup: initialize council for <PRODUCT_NAME>` and put a one-line summary in the body.
4. **Report.** Tell the user what was filled in, what you left as `TODO`, and that the council is ready. Point them at `AGENTS.md` to run their first real request.

---

## Re-run to update

Setup is not one-way. If the product changes (new pricing, new stack, a pivot), run this routine again. It updates the same fields. For a single change (e.g. one new metric), a normal edit is enough — full re-setup is only for big shifts.
