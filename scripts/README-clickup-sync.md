# Sync docs to ClickUp

> **Optional.** This is off until you add the `CLICKUP_WORKSPACE_ID` variable (step 4). Repos that never set it are not affected: the workflow is skipped. If you do not use ClickUp, you can delete `scripts/` and `.github/workflows/sync-clickup-docs.yml`.

On every push to `main`, the workflow `.github/workflows/sync-clickup-docs.yml`
mirrors this repo's `docs/` and `decisions/` folders into one ClickUp Doc.

## What it builds

```
Main page  (intro — docs/README.md)
  |- Marketing            (docs/marketing/)
  |    `- Brand
  |- Metrics
  |    `- Framework
  |- Product
  |    |- PRD
  |    `- Roadmap
  |- Tech
  |    `- Architecture
  `- Decision             (decisions/)
       |- ADR
       |- Council
       `- PR-FAQ
```

Each folder becomes a page; a folder's `README.md` becomes that page's content,
and the other markdown files become child pages. Page names come from each file's
first `# heading`.

## One-time setup

### 1. Get a ClickUp personal API token
ClickUp → your avatar → **Settings** → **Apps** → **API Token** → **Generate**.
It starts with `pk_`. (Tokens never expire.)

### 2. Get your Workspace id
Open ClickUp in the browser. The number right after `app.clickup.com/` in the URL
is your Workspace (team) id — e.g. `https://app.clickup.com/9008123456/...` → `9008123456`.

### 3. (Recommended) Get a Doc id
Create an empty Doc in ClickUp where you want the docs to live, open it, and copy
the id from the URL (the part after `/dc/`). Giving the workflow a fixed Doc id is
the safest option — it always updates the same Doc.

If you skip this, the workflow finds a Doc by name (`CLICKUP_DOC_NAME`, default
"Product Documentation") or creates one, and prints the new id in the run log so
you can save it.

### 4. Add the values to GitHub
In the repo: **Settings → Secrets and variables → Actions**.

Add one **secret**:

| Secret | Value |
| --- | --- |
| `CLICKUP_TOKEN` | your `pk_...` token |

Add these **variables** (Variables tab):

| Variable | Value | Required |
| --- | --- | --- |
| `CLICKUP_WORKSPACE_ID` | your workspace id | yes |
| `CLICKUP_DOC_ID` | the Doc id from step 3 | recommended |
| `CLICKUP_DOC_NAME` | Doc name for find-or-create | optional |

### 5. (Optional) One token per maintainer
ClickUp shows who edited a page, so each maintainer can use their own token.
Each person adds a secret named `CLICKUP_TOKEN_<GITHUB_LOGIN>`: uppercase the
login and turn every character that is not a letter or digit into `_`.

| GitHub login | Secret name |
| --- | --- |
| `octocat` | `CLICKUP_TOKEN_OCTOCAT` |
| `jane-doe` | `CLICKUP_TOKEN_JANE_DOE` |

The workflow picks the owner in this order, and stops at the first match:

1. the author of the merged PR (bots are skipped)
2. the person with the most commits in that PR
3. the person with the most commits in the push (direct pushes)
4. whoever started the run

If that person has no secret, the shared `CLICKUP_TOKEN` is used. Each token's
owner must be able to edit the target Doc. The run log shows who was picked
(never the token).

## Run it

- **Automatic:** push a change under `docs/` or `decisions/` to `main`.
- **By hand:** repo → **Actions** → **Sync docs to ClickUp** → **Run workflow**.

## Test locally

```bash
# See the planned page tree — makes no API calls:
python3 scripts/sync_clickup_docs.py --dry-run

# Do a real sync from your machine:
export CLICKUP_TOKEN=pk_xxx
export CLICKUP_WORKSPACE_ID=9008123456
export CLICKUP_DOC_ID=abcd-1234        # optional but recommended
python3 scripts/sync_clickup_docs.py
```

The script uses only Python's standard library — no `pip install` needed.

## Good to know

- **Markdown** is sent to ClickUp in the `content` field with `content_format:
  "text/md"`, so headings, lists, tables, and code blocks come across.
- **Who changed it.** Each page starts with one short line naming the last two
  people who changed its source file, newest first, by GitHub login and date, e.g.
  _Last changed by @jane-doe on 2026-10-01, before that by @octocat on 2026-09-28_. In CI this comes from the GitHub
  API (merge commits and bots are skipped). Local runs read `git log` instead, so
  they may show a commit name where the login is not known.
- **Links.** Relative markdown links between repo files (like `[PRD](product/prd.md)`) become links to the matching ClickUp page. Links written as plain `code` text stay as text, so use real links in `docs/` if you want them clickable in ClickUp.
- **Re-runs update, not duplicate.** Pages are matched by name inside their parent.
- **Renaming a file's `# heading`** changes the page name, so the sync will create a
  new page and leave the old one. Rename the old page in ClickUp (or delete it) if needed.
- **No auto-delete.** ClickUp's public API has no "delete page" endpoint, so removing
  a markdown file does **not** remove its ClickUp page. Delete it by hand in ClickUp.
- The Docs API needs a ClickUp plan that includes API access to Docs.
