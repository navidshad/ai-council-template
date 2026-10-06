# Living Product Documentation

This folder holds the **living docs** — the current state of the product. The **decision records** (PR/FAQ, ADR, council) that explain *why* choices were made live one level up, in the top-level `../decisions/` folder.

- **product/** — product vision, requirements, and roadmap
- **tech/** — technical architecture and specifications
- **marketing/** — brand, positioning, and pricing
- **metrics/** — the metrics framework and what we measure

> These are skeleton files. Fill them in for your product. Add or remove folders to fit how your team thinks.

Decision records (outside this folder):

- **`../decisions/pr-faq/`** — press-release feature pitches ("should we build this?")
- **`../decisions/adr/`** — Architecture Decision Records — *why* technical choices were made
- **`../decisions/council/`** — council syntheses for strategic, cross-functional calls

## Quick links

- **Product Requirements**: [prd.md](product/prd.md)
- **Roadmap**: [roadmap.md](product/roadmap.md)
- **PR/FAQs**: [pr-faq](../decisions/pr-faq/README.md)
- **Technical Architecture**: [architecture.md](tech/architecture.md)
- **ADRs**: [adr](../decisions/adr/README.md)
- **Council decisions**: [council](../decisions/council/README.md)
- **Metrics Framework**: [framework.md](metrics/framework.md)
- **Brand**: [brand.md](marketing/brand.md)

## How decisions get made here

Every request goes through up to three stages: **triage → depth → output**. See the root `AGENTS.md` for the full rules. In short:

- **Triage** decides if the request is trivial (just do it) or a real decision worth a record.
- **Depth** decides how hard to think: one expert lens, or the full council (many lenses) for strategic, cross-functional calls.
- **Output** decides which record to write:
  - **PR/FAQ** — "should we build this feature?" → a numbered file in `../decisions/pr-faq/`.
  - **ADR** — which technical option to pick? → a numbered file in `../decisions/adr/`.
  - **Council synthesis** — what is the strategic call? → a numbered file in `../decisions/council/`.

Every output also appends one line to the Decision Log below. Trivial edits, typos, and factual lookups skip all of this.

## Decision Log

The **single source of truth** for "what did we decide and why" — across all three workflows. Every council session, every approved or rejected PR/FAQ, and every accepted ADR appends one entry here. One line per entry, pointing to the permanent file. Do not duplicate the rationale here — the full reasoning lives in the file and the commit body.

Format:

```
- {YYYY-MM-DD} — {Council | PR/FAQ (Status) | ADR-NNN (Status)} — {short title} — `decisions/.../<file>.md`
```

---

_No decisions logged yet._

---
