#!/usr/bin/env python3
"""
Sync the repo's docs/ and decisions/ folders into a single ClickUp Doc.

Structure created in ClickUp (mirror folders):

    Main page  (intro = docs/README.md)
      |- Marketing            (docs/marketing/ -> folder page)
      |    `- Brand           (docs/marketing/brand.md)
      |- Metrics
      |    `- Framework
      |- Product
      |    |- PRD
      |    `- Roadmap
      |- Tech
      |    `- Architecture
      `- Decision             (decisions/ -> container page)
           |- ADR             (decisions/adr/README.md + its records)
           |- Council
           `- PR-FAQ

Markdown is sent to ClickUp in the `content` field with `content_format: "text/md"`
(that is the ClickUp parameter that accepts Markdown). Pages are matched by name
inside their parent, so re-running only updates pages instead of duplicating them.

Only Python's standard library is used (no pip install needed).

Environment variables
  CLICKUP_TOKEN         (required)  Personal API token, starts with "pk_".
  CLICKUP_WORKSPACE_ID  (required)  Numeric Workspace (team) id.
  CLICKUP_DOC_ID        (optional, recommended)  Existing Doc id to sync into.
  CLICKUP_DOC_NAME      (optional)  Doc name used for find-or-create. Default "Product Documentation".
  CLICKUP_PARENT_ID     (optional)  Parent id used only when creating a new Doc. Defaults to the workspace id.
  CLICKUP_PARENT_TYPE   (optional)  Parent type for a new Doc: 4 Space, 5 Folder, 6 List, 7 Everything, 12 Workspace. Default 7.
  REPO_ROOT             (optional)  Repo root path. Default: parent of this script's folder.

Usage
  python3 scripts/sync_clickup_docs.py            # do the sync
  python3 scripts/sync_clickup_docs.py --dry-run  # print the planned tree, call nothing
"""

import json
import os
import posixpath
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.clickup.com"
MD = "text/md"

# Folders in the repo we mirror. The first one is the "main page" (intro).
DOCS_DIR = "docs"
DECISIONS_DIR = "decisions"
DECISIONS_PAGE_NAME = "Decision"  # name of the sub-page that holds decisions/


# --------------------------------------------------------------------------- #
# Tiny ClickUp API client (stdlib only)
# --------------------------------------------------------------------------- #
class ClickUp:
    def __init__(self, token, workspace_id):
        self.token = token
        self.workspace_id = str(workspace_id)

    def _request(self, method, path, query=None, body=None):
        url = BASE + path
        if query:
            url += "?" + urllib.parse.urlencode(query)
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", self.token)
        req.add_header("Accept", "application/json")
        if data is not None:
            req.add_header("Content-Type", "application/json")

        for attempt in range(6):
            try:
                with urllib.request.urlopen(req) as resp:
                    raw = resp.read().decode("utf-8")
                    return json.loads(raw) if raw else {}
            except urllib.error.HTTPError as e:
                detail = e.read().decode("utf-8", "replace")
                # Back off and retry on rate limit / transient server errors.
                if e.code == 429 or 500 <= e.code < 600:
                    wait = int(e.headers.get("Retry-After", "0") or 0) or (2 ** attempt)
                    sys.stderr.write(f"  ! {e.code} on {method} {path}; retry in {wait}s\n")
                    time.sleep(wait)
                    continue
                raise SystemExit(f"ClickUp API error {e.code} on {method} {path}: {detail}")
            except urllib.error.URLError as e:
                wait = 2 ** attempt
                sys.stderr.write(f"  ! network error ({e.reason}); retry in {wait}s\n")
                time.sleep(wait)
        raise SystemExit(f"ClickUp API kept failing on {method} {path}")

    # Docs -----------------------------------------------------------------
    def search_docs(self):
        docs, cursor = [], None
        while True:
            q = {"limit": 100, "deleted": "false", "archived": "false"}
            if cursor:
                q["cursor"] = cursor
            res = self._request("GET", f"/api/v3/workspaces/{self.workspace_id}/docs", query=q)
            docs.extend(res.get("docs", []))
            cursor = res.get("next_cursor")
            if not cursor:
                return docs

    def create_doc(self, name, parent_id, parent_type):
        body = {
            "name": name,
            "visibility": "PRIVATE",
            "create_page": False,  # we create the intro page ourselves
            "parent": {"id": str(parent_id), "type": int(parent_type)},
        }
        return self._request("POST", f"/api/v3/workspaces/{self.workspace_id}/docs", body=body)

    def get_pages(self, doc_id):
        return self._request(
            "GET",
            f"/api/v3/workspaces/{self.workspace_id}/docs/{doc_id}/pages",
            query={"max_page_depth": -1, "content_format": MD},
        )

    def create_page(self, doc_id, name, content, parent_page_id=None):
        body = {"name": name, "content": content, "content_format": MD}
        if parent_page_id:
            body["parent_page_id"] = parent_page_id
        return self._request(
            "POST", f"/api/v3/workspaces/{self.workspace_id}/docs/{doc_id}/pages", body=body
        )

    def edit_page(self, doc_id, page_id, name, content):
        body = {
            "name": name,
            "content": content,
            "content_format": MD,
            "content_edit_mode": "replace",
        }
        return self._request(
            "PUT",
            f"/api/v3/workspaces/{self.workspace_id}/docs/{doc_id}/pages/{page_id}",
            body=body,
        )


# --------------------------------------------------------------------------- #
# Build the desired page tree from the repo
# --------------------------------------------------------------------------- #
def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def split_h1(md_text):
    """Return (title, body). If the file starts with an H1, use it as the title
    and drop that line from the body so ClickUp does not show the title twice."""
    lines = md_text.splitlines()
    i = 0
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    if i < len(lines) and lines[i].lstrip().startswith("# "):
        title = lines[i].lstrip()[2:].strip()
        body = "\n".join(lines[:i] + lines[i + 1:]).strip("\n")
        return title, body
    return None, md_text


# --------------------------------------------------------------------------- #
# Footprint: the last two people who changed a page's source file
# --------------------------------------------------------------------------- #
FOOTPRINT_COUNT = 2
NOREPLY_RE = re.compile(r"^(?:\d+\+)?([^@]+)@users\.noreply\.github\.com$", re.I)


def _github_authors(path):
    """Newest-first list of (name, is_login, date) for commits that touched `path`,
    from the GitHub API. Returns None when the API is not available."""
    repo = os.environ.get("GITHUB_REPOSITORY", "").strip()
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not repo or not token:
        return None
    url = f"https://api.github.com/repos/{repo}/commits?" + urllib.parse.urlencode(
        {"path": path, "per_page": 30}
    )
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    try:
        with urllib.request.urlopen(req) as resp:
            commits = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, ValueError) as e:
        sys.stderr.write(f"  ! could not read history for {path}: {e}\n")
        return None
    out = []
    for c in commits:
        if len(c.get("parents") or []) > 1:
            continue  # skip merge commits; the real authors are in the PR commits
        user = c.get("author") or {}
        git_author = (c.get("commit") or {}).get("author") or {}
        date = (git_author.get("date") or "")[:10]
        if user.get("login"):
            out.append((user["login"], True, date))
        else:  # email not linked to a GitHub account
            out.append((git_author.get("name"), False, date))
    return out


def _git_authors(repo_root, path):
    """Fallback for local runs: read authors from `git log`. The GitHub login is
    only known for noreply emails; otherwise the commit name is used."""
    import subprocess
    try:
        log = subprocess.run(
            ["git", "log", "--no-merges", "-n", "30", "--format=%an%x09%ae%x09%as", "--", path],
            cwd=repo_root, capture_output=True, text=True, check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return []
    out = []
    for line in log.splitlines():
        name, email, date = (line.split("\t") + ["", ""])[:3]
        m = NOREPLY_RE.match(email)
        out.append((m.group(1), True, date) if m else (name, False, date))
    return out


def footprint(repo_root, path):
    """One short line naming the last people who changed `path`, or ""."""
    authors = _github_authors(path)
    if authors is None:
        authors = _git_authors(repo_root, path)
    people, seen = [], set()
    for name, is_login, date in authors:
        if not name or name.endswith("[bot]") or name.lower() in seen:
            continue
        seen.add(name.lower())
        who = f"@{name}" if is_login else name
        people.append(f"{who} on {date}" if date else who)
        if len(people) == FOOTPRINT_COUNT:
            break
    if not people:
        return ""
    # Newest first, in words, so the order is clear.
    return "_Last changed by " + ", before that by ".join(people) + "_"


def nice_name(folder):
    return folder.replace("-", " ").replace("_", " ").strip().title()


def node(key, name, content, children, src=None):
    return {"key": key, "name": name, "content": content or "", "children": children, "src": src}


def build_folder_node(abs_dir, rel_dir, name_override=None):
    """Turn a directory into a page. A README.md becomes the page's content;
    other markdown files and sub-folders become child pages."""
    entries = sorted(os.listdir(abs_dir))
    readme = None
    src = None
    for e in entries:
        if e.lower() == "readme.md":
            readme = e
            break

    if readme:
        title, body = split_h1(read_text(os.path.join(abs_dir, readme)))
        name = name_override or title or nice_name(os.path.basename(rel_dir))
        content = body
        src = f"{rel_dir}/{readme}"
    else:
        name = name_override or nice_name(os.path.basename(rel_dir))
        content = ""  # filled in below with a small section note

    children = []
    subdirs = [e for e in entries if os.path.isdir(os.path.join(abs_dir, e))]
    files = [
        e for e in entries
        if e.lower().endswith(".md") and e.lower() != "readme.md"
        and os.path.isfile(os.path.join(abs_dir, e))
    ]

    for d in sorted(subdirs):
        children.append(build_folder_node(os.path.join(abs_dir, d), f"{rel_dir}/{d}"))
    for fn in sorted(files):
        title, body = split_h1(read_text(os.path.join(abs_dir, fn)))
        leaf_name = title or nice_name(os.path.splitext(fn)[0])
        children.append(node(f"{rel_dir}/{fn}", leaf_name, body, [], src=f"{rel_dir}/{fn}"))

    # If a folder page has no README content, add a small note so it is not blank.
    if not content:
        if children:
            listed = ", ".join(c["name"] for c in children)
            content = f"_This section groups the following pages: {listed}._"
        else:
            content = "_This section is empty._"

    return node(rel_dir, name, content, children, src=src)


def add_footprints(repo_root, node_):
    """Put a short "last changed by" line at the top of every page that comes
    from a file, so readers in ClickUp see who touched it most recently."""
    if node_.get("src"):
        line = footprint(repo_root, node_["src"])
        node_["footprint"] = line
        if line:
            node_["content"] = f"{line}\n\n{node_['content']}"
    for child in node_["children"]:
        add_footprints(repo_root, child)


def build_tree(repo_root):
    docs_abs = os.path.join(repo_root, DOCS_DIR)
    if not os.path.isdir(docs_abs):
        raise SystemExit(f"Could not find '{DOCS_DIR}/' in {repo_root}")

    # Main page = the docs/ folder (content from docs/README.md).
    root = build_folder_node(docs_abs, DOCS_DIR)

    # Attach decisions/ as the "Decision" sub-page, last.
    decisions_abs = os.path.join(repo_root, DECISIONS_DIR)
    if os.path.isdir(decisions_abs):
        decision = build_folder_node(decisions_abs, DECISIONS_DIR, name_override=DECISIONS_PAGE_NAME)
        root["children"].append(decision)

    add_footprints(repo_root, root)
    return root


# --------------------------------------------------------------------------- #
# Sync the desired tree into ClickUp
# --------------------------------------------------------------------------- #
def flatten_existing(pages, parent_id=None, out=None):
    """Index existing ClickUp pages as {parent_page_id or '': {name: page}}."""
    if out is None:
        out = {}
    for p in pages:
        pid = p.get("parent_page_id") or ""
        out.setdefault(pid, {})[p.get("name", "")] = p
        if p.get("pages"):
            flatten_existing(p["pages"], p["id"], out)
    return out


def resolve_doc(cu):
    """Return a doc id, creating the doc if needed."""
    doc_id = os.environ.get("CLICKUP_DOC_ID", "").strip()
    if doc_id:
        print(f"Using existing Doc id: {doc_id}")
        return doc_id

    name = os.environ.get("CLICKUP_DOC_NAME", "Product Documentation").strip()
    for d in cu.search_docs():
        if d.get("name") == name and not d.get("deleted") and not d.get("archived"):
            print(f"Found existing Doc '{name}': {d['id']}")
            return d["id"]

    parent_id = os.environ.get("CLICKUP_PARENT_ID", "").strip() or cu.workspace_id
    parent_type = os.environ.get("CLICKUP_PARENT_TYPE", "7").strip() or "7"
    created = cu.create_doc(name, parent_id, parent_type)
    print(f"Created new Doc '{name}': {created['id']}")
    print(f">>> Save this as the CLICKUP_DOC_ID variable to reuse it next time: {created['id']}")
    return created["id"]


def ensure_pages(cu, doc_id, node_, parent_page_id, existing_index, ids):
    """Pass 1: find or create every page so we know all the page ids."""
    bucket = existing_index.get(parent_page_id or "", {})
    match = bucket.get(node_["name"])

    # Special case: an existing root page that ClickUp auto-made can be adopted
    # as the main page even if its name differs, so we don't create a duplicate.
    if match is None and parent_page_id is None:
        roots = existing_index.get("", {})
        if len(roots) == 1:
            match = next(iter(roots.values()))

    if match:
        node_["match"] = match
        page_id = match["id"]
    else:
        created = cu.create_page(doc_id, node_["name"], "_Syncing..._", parent_page_id)
        page_id = created["id"]
        node_["match"] = None
    ids[node_["key"]] = page_id
    node_["page_id"] = page_id

    for child in node_["children"]:
        ensure_pages(cu, doc_id, child, page_id, existing_index, ids)


LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)\)")


def rewrite_links(content, src, ids, page_url):
    """Turn relative links between repo files into links to the ClickUp pages.
    Links to files that are not pages fall back to GitHub, or plain text."""
    if not src:
        return content
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    branch = os.environ.get("GITHUB_REF_NAME", "master")

    def fix(m):
        label, target = m.group(1), m.group(2)
        if re.match(r"^([a-zA-Z][a-zA-Z0-9+.-]*:|#|/)", target):
            return m.group(0)
        path, _, frag = target.partition("#")
        full = posixpath.normpath(posixpath.join(posixpath.dirname(src), path))
        keys = [full, full.rstrip("/")]
        if full.lower().endswith("/readme.md"):
            keys.append(full[: -len("/README.md")])
        for k in keys:
            if k in ids:
                return f"[{label}]({page_url(ids[k])})"
        if repo and not full.startswith(".."):
            return f"[{label}](https://github.com/{repo}/blob/{branch}/{full})"
        return label

    return LINK_RE.sub(fix, content)


def update_pages(cu, doc_id, node_, ids, page_url, indent=0):
    """Pass 2: write each page's final content, with links pointing at ClickUp."""
    pad = "  " * indent
    match = node_["match"]
    new = rewrite_links(node_["content"], node_.get("src"), ids, page_url).strip()
    if match:
        old = (match.get("content") or "").strip()
        if old == new and match.get("name") == node_["name"]:
            print(f"{pad}= {node_['name']} (unchanged)")
        else:
            cu.edit_page(doc_id, node_["page_id"], node_["name"], new)
            print(f"{pad}~ {node_['name']} (updated)")
    else:
        cu.edit_page(doc_id, node_["page_id"], node_["name"], new)
        print(f"{pad}+ {node_['name']} (created)")

    for child in node_["children"]:
        update_pages(cu, doc_id, child, ids, page_url, indent + 1)


def print_tree(node_, indent=0):
    line = node_.get("footprint")
    print("  " * indent + "- " + node_["name"] + (f"   [{line}]" if line else ""))
    for c in node_["children"]:
        print_tree(c, indent + 1)


def main():
    dry_run = "--dry-run" in sys.argv
    repo_root = os.environ.get("REPO_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    tree = build_tree(repo_root)

    if dry_run:
        print("DRY RUN — planned ClickUp page tree:\n")
        print_tree(tree)
        print("\n(no API calls made)")
        return

    token = os.environ.get("CLICKUP_TOKEN", "").strip()
    workspace_id = os.environ.get("CLICKUP_WORKSPACE_ID", "").strip()
    if not token or not workspace_id:
        raise SystemExit("CLICKUP_TOKEN and CLICKUP_WORKSPACE_ID must be set.")

    cu = ClickUp(token, workspace_id)
    doc_id = resolve_doc(cu)

    existing_index = flatten_existing(cu.get_pages(doc_id))
    print("\nSyncing pages:")
    ids = {}
    ensure_pages(cu, doc_id, tree, None, existing_index, ids)
    page_url = lambda pid: f"https://app.clickup.com/{workspace_id}/v/dc/{doc_id}/{pid}"
    update_pages(cu, doc_id, tree, ids, page_url)
    print("\nDone.")


if __name__ == "__main__":
    main()
