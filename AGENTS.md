# AGENTS.md

Repository guidance for coding agents. `CLAUDE.md` is a symlink to this file.

## Core Principles (CRITICAL)

**Less is more. The simplest solution is the best solution.** The action hierarchy for every change: **Delete > Replace > Add**.

1. **Solve at the owner**: Put behavior in the code path that owns or observes it. For fixes, never guard a symptom with a staleness check, initialization flag, skip-first-call branch, or `try/except` around broken logic; relocate the trigger and delete the wrong path. For features, extend the existing owner rather than creating a parallel abstraction.
2. **Search and reuse first**: Search the whole repository before creating a feature, component, helper, workflow, or utility. Reuse or adapt what exists, consolidate in-scope duplication in the shared owner, and delete duplicate paths. Three similar lines beat a helper nobody else calls.
3. **Delete and modify existing code before creating new code**: Bugfixes are net-negative by default unless deletion and relocation are demonstrably impossible. A new file must first prove it cannot fit cleanly in an existing owner.
4. **Keep scope minimal**: Implement only the simplest complete solution. Avoid impossible-state handling, speculative flags, compatibility shims, policy scaffolding, and unrelated cleanup. Tests are out of scope by default — rely on existing coverage and focused validation; only an uncovered, high-risk regression path justifies minimal new test code.
5. **Ship zero-regression, production-ready changes**: Understand what you remove instead of retaining broken code as insurance. Remove unused imports, functions, types, files, and comments; run relevant cleanup checks; and thoroughly debug and validate the changed owner. Do not break existing features or workflows unless the PR intentionally removes them with evidence.

**Review gate:** for every addition, the reviewer decides whether deleting or changing existing code would have fixed the problem instead — if it would, that is a blocking finding. A missing or thin PR description is never itself a finding.

NEVER push to `main`. NEVER force push. Always start work in a new git worktree (`git worktree add`) on a feature branch and open a PR — never edit the primary checkout directly, it may hold in-flight work.

## PR Workflow

After opening a PR:

1. Wait for the automated PR review and auto-format commit from Ultralytics Actions (`format.yml`), then pull and address every finding.
2. Review the full diff in-session against the Core Principles, performance, and the review gate above, then batch the fixes into one commit and push. After each round of bot or human commits, pull and resume the same reviewer on `<last-reviewed-sha>..HEAD` plus anything that delta could have invalidated. Repeat until the local head matches the live head.
3. Hand off or merge only on a clean final pass: one cold full-diff review returning LGTM with no findings, on a head that is still live at merge time.
4. Never fight other commits: Ultralytics Actions pushes auto-format and header commits, and multiple users may work on the same PR. `git pull --rebase` before pushing; never reset or revert commits you did not author.
5. After the PR merges, clean up: remove local worktrees and branches for it, then `git checkout main && git pull`.

## Commands and validation

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
python -m compileall -q fetch_stats.py utils.py count_stars.py
```

There is no unit-test suite and PR workflows never execute the fetchers. Syntax checks do not validate API behavior. For collection changes, exercise the affected fetcher with an explicit temporary output path and inspect the result; `fetch_stats.py` is safe to import. Preserve existing data for fallback validation. Read `.github/workflows/analytics.yml` before running the daily pipeline; dispatch it only on `main`.

## Where to look

- Daily collection and summary → `fetch_stats.py`.
- HTTP, fallback merge, JSON output → `utils.py`.
- Historical star counting → `count_stars.py`.
- Scheduled data PRs → `.github/workflows/analytics.yml`.

## Conventions

- Every source file starts with the `# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license` header — Ultralytics Actions adds it automatically; don't add or revert it manually.
- Google-style docstrings and Prettier-formatted YAML/JSON/Markdown, enforced by the Ultralytics Actions bot on PRs — don't fight its auto-format commits.
- `data/*.json` files are bot-committed daily by `UltralyticsAssistant` ("Update Ultralytics analytics" PRs) — never hand-edit them, and expect them to have moved on `main` if a branch lives past 02:07 UTC.
- Dependencies are floor-pinned in `requirements.txt` and bumped monthly by Dependabot (`.github/dependabot.yml`); there is no version-bump or publish step to maintain.
- The bot's Ruff pass runs pyupgrade at `--target-version py38`; `fetch_stats.py` and `utils.py` use `from __future__ import annotations` so their `str | None` / `dict | None` annotations stay valid there — keep that import in any new module that uses PEP 604 unions.
- Every source follows one shape: `existing = read_json(output)` → fetch → `safe_merge(new, existing, keys, label, allow_zero=...)` → `write_json(output, new)` → return the dict. New sources copy this shape inside `fetch_stats.py`; do not add a second helper module.
- `write_json` emits `indent=2`, `ensure_ascii=False`, a trailing newline, and `allow_nan=False` (NaN/Inf are sanitized to 0), which already matches the bot's Prettier output — daily data PRs carry exactly one commit.
- Configuration is read with `os.getenv` only; nothing loads `.env` files. `ORG` changes just the GitHub organization, not the PyPI list, GA property, subreddit, Platform endpoint, or output filenames.

## Pitfalls

- Never `gh workflow run analytics.yml --ref <feature-branch>`. The job checks out that ref, branches `analytics-*` from it, opens a PR against `main`, and `gh pr merge --squash --admin` lands it after 300 s — carrying the branch's code changes into `main` without review. Dispatch only on `main`.
- Missing secrets locally do not zero the summary. Without `PORTAL_API_KEY`/`GA_CREDENTIALS_JSON`, `platform.json` and `google_analytics.json` are untouched and `summary.json` keeps the committed `platform_*`/`events_per_day`, printing `Warning: Keeping existing summary.<key>` — expected, not a bug. Without `PEPY_API_KEY`, each package's `total` likewise falls back to the committed value if pepy.tech rejects the request.
- Running with a different `ORG` against the committed `data/github.json` reuses same-named repos' old values as fallbacks, because old records are matched by `name` without an `org` check.
- `count_stars.py` ignores the `GITHUB_TOKEN` env var and reads `--token` (default: the empty `GITHUB_TOKEN = ""` constant) — never paste a token into that constant. Unauthenticated PyGithub calls hit GitHub's low anonymous rate limit, and `--save` writes personal data to an untracked `users.csv`.

Choose `safe_merge(..., allow_zero=...)` deliberately: failed fetches preserve valid prior totals; zero is valid for windows such as GA reports. Do not blanket-reject zero or decreasing metrics.
