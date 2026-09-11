# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, etc.) when working with code in this repository. CLAUDE.md is a symlink to this file.

`ultralytics/stars` publishes Ultralytics organization analytics as static JSON. A scheduled GitHub Actions job runs `fetch_stats.py`, which pulls GitHub, PyPI, Google Analytics, Reddit, and Ultralytics Platform numbers and rewrites `data/*.json`; the job then lands the result on `main` through an auto-merged PR, and consumers read the files from `https://raw.githubusercontent.com/ultralytics/stars/main/data/<name>.json`. The whole codebase is three Python files (`fetch_stats.py`, `utils.py`, `count_stars.py`) plus `requirements.txt`, six committed JSON files under `data/`, and three workflows. There is no package, no version, no test suite, and no local lint config.

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

## Commands

```bash
# Local setup. uv pip install needs an active virtualenv (CI passes --system instead); .venv* is gitignored.
# fetch_stats.py itself imports only requests (plus google-analytics-data, imported lazily, when GA_CREDENTIALS_JSON is
# set); pandas, PyGithub, and tqdm are for count_stars.py. Ruff and Node are not in requirements.txt.
uv venv .venv && source .venv/bin/activate
uv pip install -r requirements.txt

# Syntax check without importing dependencies or calling APIs (PR workflows lint and format but never execute the scripts)
python -m py_compile fetch_stats.py utils.py count_stars.py

# The daily fetcher, exactly as analytics.yml runs it. GITHUB_TOKEN is the only required variable (without it the script
# exits "Set GITHUB_TOKEN in env"). Rewrites data/github.json, data/pypi.json, data/reddit.json, and data/summary.json;
# writes data/google_analytics.json only when GA_CREDENTIALS_JSON is set and data/platform.json only when PORTAL_API_KEY
# is set. PEPY_API_KEY unlocks pepy.tech all-time totals; ORG overrides the GitHub organization (default "ultralytics").
GITHUB_TOKEN=ghp_... python fetch_stats.py
GITHUB_TOKEN=ghp_... PEPY_API_KEY=... GA_CREDENTIALS_JSON="$(cat service-account.json)" PORTAL_API_KEY=... python fetch_stats.py
git diff -- data/ # inspect what changed and read every "Warning:" line in the run output
git checkout -- data/ # then discard local data churn (the bot owns data/)

# Exercise one source in isolation: importing fetch_stats does not run the pipeline (guarded by __main__), and every
# fetcher takes an explicit output Path. Copy the committed JSON there first if you want to see fallback behavior.
python -c "from pathlib import Path; from fetch_stats import fetch_reddit_stats; print(fetch_reddit_stats('ultralytics', Path('/tmp/reddit.json')))"

# Manual historical star counting. Reads --token only (never the GITHUB_TOKEN env var). Add --save to also write
# users.csv (names, companies, emails of stargazers with a public email) into the cwd — not gitignored, never commit it.
python count_stars.py --token ghp_... --days 30

# Approximate the Ultralytics Actions bot locally. There is no pyproject.toml or ruff config in this repo, so a bare
# `ruff format` wraps at 88 columns and fights the bot's 120. Flags are copied from the "Run Python" and "Run Prettier"
# steps of action.yml in ultralytics/actions (not in this checkout); the bot additionally runs its own docstring
# formatter, treats Ruff failures as non-fatal, and uses broader Prettier globs, so expect it to still push a commit.
ruff format --line-length 120 .
ruff check --fix --unsafe-fixes --extend-select F,I,D,UP,RUF,FA --target-version py38 --ignore BLE001,D100,D104,D203,D205,D212,D213,D401,D406,D407,D413,RUF001,RUF002,RUF012,S110 .
npx prettier@3.8.5 --print-width 120 --write "**/*.{md,yml,yaml,json}"

# Trigger a production run on main (read the Gotchas before ever passing --ref)
gh workflow run analytics.yml && gh run list --workflow analytics.yml --limit 3
```

## Workflows

Files in `.github/workflows/`:

- `analytics.yml` (Update Analytics) — `schedule: "7 2 * * *"` (02:07 UTC daily) plus `workflow_dispatch`; `permissions: contents: write, pull-requests: write`. One `ubuntu-latest` job: `actions/checkout@v7`, `actions/setup-python@v7` with `python-version: "3.x"`, `ultralytics/actions/setup-uv@main` (uv cache keyed on `requirements.txt`), `uv pip install --system -r requirements.txt`, then `python fetch_stats.py` with `GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}` (the default Actions token) and the `PEPY_API_KEY`, `GA_CREDENTIALS_JSON`, `PORTAL_API_KEY` secrets. The "Create PR and merge" step does nothing unless `git status --porcelain` is non-empty; otherwise it sets the committer to `UltralyticsAssistant <web@ultralytics.com>`, branches `analytics-$(date +%s)`, runs `git add data/` (only `data/`), commits "Update analytics data", pushes, opens a PR titled "Update Ultralytics analytics" with `GH_TOKEN: ${{ secrets._GITHUB_TOKEN }}` (a PAT), waits `sleep 300`, then `gh pr merge --squash --delete-branch --admin`. An `EXIT` trap attempts to delete the remote branch on every exit path and ignores failures (`|| true`). Squash-merging puts one "Update Ultralytics analytics (#N)" commit on `main` per day. Runs observed 2026-09-07 through 2026-09-11 took 6–6.5 min, five of which are the sleep.
- `format.yml` (Ultralytics Actions) — on `issues: opened` and `pull_request` to `main` (`opened, closed, synchronize, review_requested`), runs `ultralytics/actions@main` with `labels`, `python`, `prettier`, `spelling` (codespell), `links` (Lychee), and `summary` enabled, authenticated with `secrets._GITHUB_TOKEN || secrets.GITHUB_TOKEN` and using `OPENAI_API_KEY` and `BRAVE_API_KEY`. It pushes auto-format commits to the PR branch (`contents: write`) and posts the AI PR summary and labels. It never runs the Python.
- `cla.yml` (CLA) — `pull_request_target` (opened, reopened, synchronize) plus `issue_comment: created`; the job runs only for PR comments whose body is exactly `recheck` or contains "I have read the CLA Document and I sign the CLA". Uses `ultralytics/actions/cla@main` with `secrets._GITHUB_TOKEN`.
- `.github/dependabot.yml` opens `pip` update PRs monthly (limit 10) and `github-actions` update PRs weekly (limit 5), both labeled `dependencies`.
- GitHub's CodeQL default setup (configured in repository settings, not a workflow file) also posts `Analyze (python)` and `Analyze (actions)` checks on PRs.

## Conventions

- Every source file starts with the `# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license` header — Ultralytics Actions adds it automatically; don't add or revert it manually.
- Google-style docstrings and Prettier-formatted YAML/JSON/Markdown, enforced by the Ultralytics Actions bot on PRs — don't fight its auto-format commits.
- `data/*.json` files are bot-committed daily by `UltralyticsAssistant` ("Update Ultralytics analytics" PRs) — never hand-edit them, and expect them to have moved on `main` if a branch lives past 02:07 UTC.
- Dependencies are floor-pinned in `requirements.txt` and bumped monthly by Dependabot (`.github/dependabot.yml`); there is no version-bump or publish step to maintain.
- The bot's Ruff pass runs pyupgrade at `--target-version py38`; `fetch_stats.py` and `utils.py` use `from __future__ import annotations` so their `str | None` / `dict | None` annotations stay valid there — keep that import in any new module that uses PEP 604 unions.
- Every source follows one shape: `existing = read_json(output)` → fetch → `safe_merge(new, existing, keys, label, allow_zero=...)` → `write_json(output, new)` → return the dict. New sources copy this shape inside `fetch_stats.py`; do not add a second helper module.
- `write_json` emits `indent=2`, `ensure_ascii=False`, a trailing newline, and `allow_nan=False` (NaN/Inf are sanitized to 0), which already matches the bot's Prettier output — daily data PRs carry exactly one commit.
- Configuration is read with `os.getenv` only; nothing loads `.env` files. `ORG` changes just the GitHub organization, not the PyPI list, GA property, subreddit, Platform endpoint, or output filenames.

## Architecture

Paths are relative to the repository root.

**Run flow.** `fetch_stats.py`'s `__main__` block runs the sources in a fixed order, each reading its committed JSON, fetching, merging with `safe_merge`, and writing its file immediately: `fetch_github_stats` → `fetch_pypi_stats` → `fetch_google_analytics_stats` (only if `GA_CREDENTIALS_JSON`) → `fetch_reddit_stats` → `fetch_platform_stats` (only if `PORTAL_API_KEY`) → an inline summary block that builds `data/summary.json` from the in-memory results. Output paths are `Path(__file__).parent / "data/<name>.json"`, so the script is cwd-independent. The GitHub stage is the only one that aborts deliberately: `fetch_github_repos` calls `sys.exit` on GraphQL `errors` or a missing organization, and `post_json` exits on any 4xx (including 429) or after three failed attempts, so a GitHub failure ends the run before anything is written and the workflow step fails (no PR). The other sources catch their request failures, print `Warning: ...`, and fall back to committed values; only an aggregation or filesystem error outside those handlers could still abort after earlier files were written.

- `fetch_stats.py`
  - `fetch_github_repos(org, token)`: GraphQL `organization.repositories(first: 100, isFork: false, privacy: PUBLIC)` paged by cursor with a 0.3 s sleep between pages; drops `isArchived`/`isDisabled`/`isLocked`/`isMirror` nodes client-side. Fields: `name`, `stargazerCount`, `forkCount`, `issues.totalCount`, `pullRequests.totalCount`.
  - `fetch_github_contributors(org, repo, token)`: REST `GET /repos/{org}/{repo}/contributors?per_page=1&anon=true`; the count is the last `page=` number in the `Link` header (so anonymous contributors are included), or the list length when there is no pagination. Returns 0 on non-200 or any exception, which the caller's `allow_zero=False` merge then replaces with the committed value.
  - `fetch_github_stats(org, token, output)`: orders repos by the fetched `stargazerCount` (before fallback) with a 0.1 s sleep per repo; merges `stars`/`forks`/`contributors` with `allow_zero=False` and `issues`/`pull_requests` with zeros allowed, matching old records by repo `name` only (no `org` check). A non-empty fetch replaces the repo list — repos that vanish or become archived/disabled/locked/mirror are dropped, and only an entirely empty result keeps the old list wholesale. Totals are sums over the merged list, `public_repos = len(repo_data)`, and `total_contributors` double-counts people who contribute to several repos.
  - `fetch_pypi_package_stats(package, pepy_api_key)`: pypistats.org `GET /api/packages/{package}/recent` → `last_day`/`last_week`/`last_month`; pepy.tech `GET /api/v2/projects/{package}` with `X-API-Key` → `total_downloads`; 1.0 s sleep per package (the code comment cites pepy's free tier as 10 calls/min). A non-200 from either API silently leaves those fields at 0 — only exceptions print a warning.
  - `fetch_pypi_stats(packages, output, pepy_api_key)`: merges `total` with `allow_zero=False`; if all three recent counts are 0 (treated as an API failure) it silently copies all three from the old record, otherwise merges them individually. The tracked packages are the inline `pypi_packages` list in `__main__` (seven, `ultralytics` … `ultralytics-platform`).
  - `fetch_google_analytics_stats(property_id, credentials_json, output)`: lazy-imports `google.analytics.data_v1beta` and `google.oauth2.service_account`, builds credentials from the JSON string, and issues one `RunReportRequest` per window `1d, 7d, 30d, 90d, 365d` (`{days}daysAgo`..`today`) for metrics `activeUsers`, `sessions`, `eventCount`, `averageSessionDuration`; an empty `response.rows` yields zeros for that window. GA4 property `371754141` is hardcoded in `__main__`. All five reports are built before the single write, so an exception in any of them discards the new periods and returns the existing file (if it has `periods`) or `None`. Periods merge with zeros allowed.
  - `parse_abbreviated_number(value)` + `fetch_reddit_stats(subreddit, output)`: shields.io `GET https://img.shields.io/reddit/subreddit-subscribers/{subreddit}.json`, parses `value` like `"4.7k"` (`k`/`m`/`b` suffixes) to an int, merges `subscribers` with `allow_zero=False`; a non-200 silently leaves 0 for the merge to replace.
  - `fetch_platform_stats(api_url, api_key, output)`: `GET https://portal.ultralytics.com/api/analytics/platform-metrics/mongodb?start=2026-01-13&end=<today>&summary=true` with `Authorization: Bearer <PORTAL_API_KEY>`; maps `projects`/`datasets`/`images`/`models`/`exports`/`totalAnnotations` to `total_*` and merges all with `allow_zero=False`. Non-200 or exception returns the existing dict without writing. The server lives in the separate `ultralytics/portal` repo at `apps/portal/app/api/analytics/platform-metrics/mongodb/route.ts`, which returns summary-only aggregates to Bearer requests.
  - Summary block: `events_per_day = round(GA 90d events / 90)` (0 when GA was skipped), `platform_*` from the platform dict (0 when skipped), everything else from the GitHub/PyPI/Reddit results; all keys merge against the old `summary.json` with `allow_zero=False`, so a skipped source keeps yesterday's published number instead of zeroing it — and an accepted 0 in a source file can coexist with an older non-zero value in the summary.
- `utils.py`
  - `retry_request(func, *args, retries=3, backoff=2.0, **kwargs)`: retries on `requests` exceptions, 5xx, and 429 with waits of `backoff * 2**attempt` (2 s, 4 s); returns the response for every other status so callers must check `status_code`; re-raises the last error when exhausted.
  - `post_json(url, headers, payload, timeout=60, retries=3)`: the GraphQL POST; retries only 5xx and exceptions with the same backoff and `sys.exit`s on any 4xx (429 included) or exhaustion — process-fatal on purpose.
  - `fetch_json(url, headers, timeout)`: has no callers. Delete it rather than build on it.
  - `read_json(path)` returns `{}` for a missing or unparsable file (it does not validate the shape); `write_json(path, data)` creates parent dirs and writes readable JSON (see Conventions), falling back to `_sanitize_floats` when `json.dumps(..., allow_nan=False)` raises.
  - `is_valid(value, allow_zero=True)`: `int`/`float` only (`bool` rejected), finite, `>= 0` (or `> 0` when `allow_zero=False`). `safe_merge(new_data, old_data, keys, label="", allow_zero=True)` mutates `new_data` per key: keep the new value if valid, else the old value if valid (printing `Warning: Keeping existing <label>.<key>: <old> (new: <new>)`), else 0. This is the repo's core invariant — a published value never becomes 0/NaN/None because an upstream API hiccuped; it says nothing about smaller-but-valid values, which are accepted. Choose `allow_zero` deliberately for a new metric: `False` where a 0 is far more likely an API failure than a reading (stars, forks, contributors, download totals, subscribers, platform totals — a repo with genuinely 0 forks simply stays 0), `True` where 0 is a normal reading (issues, PR counts, GA windows).
  - `get_timestamp()`: UTC ISO 8601 with a `Z` suffix.
- `count_stars.py` — standalone PyGithub script, not used by any workflow. `REPOS` is the inline list of 43 `owner/name` strings (several are historical names). `run(token, days, save)` walks `repo.get_stargazers_with_dates().reversed` newest-first with a tqdm bar and breaks at the first star older than `days`; `--save` sleeps 1.39 s per stargazer, fetches each profile, and writes only users with a public email to `users.csv` (pandas index plus Repo, Name, Company, Email, Location, GitHub, Followers, Date). `g.get_repo(repo)` and the stargazer call sit outside the `try`, so one repo that no longer resolves aborts the whole run. `parse_opt` defaults `--token` to the module-level `GITHUB_TOKEN = ""` constant. The `run` docstring's `repos.yaml` reference is stale; no such file exists.
- `data/` — the published API. Known consumers: the separate `ultralytics/portal` repo (`apps/portal/lib/community/stats.ts` reads `github.json` `total_*`, `pypi.json` `total_downloads`/`total_last_month`, `google_analytics.json`, and `summary.json` `platform_annotations`/`platform_images`/`platform_models`/`reddit_subscribers`) and the README's public field docs for `github.json` and `pypi.json`. Renaming or dropping a key is a breaking change: keep the old key or update every consumer in the same PR.

  | File                         | Written                         | Top-level fields                                                                                                                                                                                                                                                                              |
  | ---------------------------- | ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | `data/github.json`           | every completed run             | `org`, `total_stars`, `total_forks`, `total_issues`, `total_pull_requests`, `total_contributors`, `public_repos`, `timestamp`, `repos[]` of `{name, stars, forks, issues, pull_requests, contributors}` in fetched-stars order (`org` is not listed in the README)                            |
  | `data/pypi.json`             | every completed run             | `total_downloads`, `total_last_month`, `timestamp`, `packages[]` of `{package, last_day, last_week, last_month, total}`                                                                                                                                                                       |
  | `data/google_analytics.json` | only with `GA_CREDENTIALS_JSON` | `property_id`, `timestamp`, `periods` keyed `1d`/`7d`/`30d`/`90d`/`365d`, each `{active_users, sessions, events, avg_session_duration}`                                                                                                                                                       |
  | `data/reddit.json`           | every completed run             | `subreddit`, `subscribers`, `timestamp`                                                                                                                                                                                                                                                       |
  | `data/platform.json`         | only with `PORTAL_API_KEY`      | `total_projects`, `total_datasets`, `total_images`, `total_models`, `total_exports`, `total_annotations`, `timestamp`                                                                                                                                                                         |
  | `data/summary.json`          | every completed run             | `total_stars`, `total_forks`, `total_issues`, `total_pull_requests`, `total_downloads`, `events_per_day`, `total_contributors`, `reddit_subscribers`, `platform_datasets`, `platform_annotations`, `platform_images`, `platform_projects`, `platform_models`, `platform_exports`, `timestamp` |

- `.github/` — the three workflows above, `dependabot.yml`, and `ISSUE_TEMPLATE/` (`bug-report.yml`, `feature-request.yml`, `question.yml`, `config.yml` contact links). `.gitignore` is the generic Ultralytics YOLO ignore list (`*.pt`, `runs/*`, `results*.csv`, `*.data`, `.venv*`, `__pycache__/`, …) — it tracks `data/*.json` and does not ignore `users.csv`.

## Where to look

- A published number is stale or wrong → the `fetch_<source>_stats` function in `fetch_stats.py`, then the latest run log (`gh run list --workflow analytics.yml`, `gh run view <id> --log`) for `Warning: Keeping existing ...` and `Warning: Failed to fetch ...` lines. A fresh `timestamp` or a `✅` line does not prove every upstream fetch succeeded: `safe_merge` fallbacks and the PyPI all-zero fallback keep old values under a new timestamp, and PyPI/Reddit non-200 responses fall back without printing the status.
- A number dropped to 0 or went backwards → `safe_merge`/`is_valid` in `utils.py` and the `allow_zero` argument at the call site (GA windows and issue/PR counts accept zeros by design); for GitHub totals also check repo membership, since a repo that was archived, disabled, or removed drops out of `repos[]` and its totals on the next run.
- Adding a metric to an existing source → extend that source's request, result mapping, and `safe_merge` keys in its `fetch_<source>_stats`; add a `summary.json` key only if a consumer needs it.
- Adding a PyPI package → append to `pypi_packages` in `fetch_stats.py` `__main__`, then update the README "Packages tracked" list and the header comment of `analytics.yml` (both are hand-maintained mirrors).
- Adding a new source → a new `fetch_<source>_stats(..., output)` in `fetch_stats.py` following the read → fetch → `safe_merge` → `write_json` shape, called from `__main__` behind an env-var guard if it needs a secret; add the secret to the `env:` of the "Fetch analytics" step in `analytics.yml` and to the repo's Actions secrets; document the file and fields in `README.md`.
- Schedule, tokens, commit author, or merge behavior → `analytics.yml` only; no other automation writes `data/`.
- Formatting or spelling findings on a PR → they come from `ultralytics/actions@main` via `format.yml`; pull the bot's commit instead of reformatting locally.
- Repos tracked by the manual star counter → `REPOS` in `count_stars.py`.

## Gotchas

- No PR runs the scripts. `format.yml` and `cla.yml` are the only PR workflows; a broken `fetch_stats.py` merges green and fails at 02:07 UTC. Validate locally with a real `GITHUB_TOKEN` first (see Tests).
- Never `gh workflow run analytics.yml --ref <feature-branch>`. The job checks out that ref, branches `analytics-*` from it, opens a PR against `main`, and `gh pr merge --squash --admin` lands it after 300 s — carrying the branch's code changes into `main` without review. Dispatch only on `main`.
- Local runs dirty `data/`. Every completed run rewrites `timestamp` (and any changed numbers) in the four unconditional files; `git checkout -- data/` before committing. If a branch outlives the 02:07 UTC run, rebase conflicts in `data/` resolve to `main`'s version.
- Missing secrets locally do not zero the summary. Without `PORTAL_API_KEY`/`GA_CREDENTIALS_JSON`, `platform.json` and `google_analytics.json` are untouched and `summary.json` keeps the committed `platform_*`/`events_per_day`, printing `Warning: Keeping existing summary.<key>` — expected, not a bug. Without `PEPY_API_KEY`, each package's `total` likewise falls back to the committed value if pepy.tech rejects the request.
- Running with a different `ORG` against the committed `data/github.json` reuses same-named repos' old values as fallbacks, because old records are matched by `name` without an `org` check.
- Token roles: inside the workflows `GITHUB_TOKEN` is the default `secrets.GITHUB_TOKEN` (enough for the public GraphQL/REST reads); the `_GITHUB_TOKEN` PAT drives `gh pr create`/`gh pr merge` and the cleanup trap in `analytics.yml`, the CLA action, and Ultralytics Actions in `format.yml`. Locally, pass a personal token.
- Contributor counts come from the `Link` header with `anon=true`, so they include anonymous contributors and differ from the GitHub UI; Reddit subscribers come from shields.io's abbreviated badge text, so they are rounded to that precision (`4.7k` → `4700`).
- GA periods accept zeros (`allow_zero=True`), and an empty GA report also yields zeros; the committed `google_analytics.json` at the time of writing has an all-zero `1d` period next to populated `7d`+ windows, so a zero there is what GA returned, not a merge failure. `analytics.yml`'s header comment describes GA as "page views (30-day window)" — the code fetches `activeUsers`/`sessions`/`eventCount`/`averageSessionDuration` over five windows; trust the code.
- Rate limiting is fixed sleeps, not header parsing: 0.3 s between GraphQL pages, 0.1 s per repo, 1.0 s per PyPI package. `retry_request` retries 429s; `post_json` does not.
- `count_stars.py` ignores the `GITHUB_TOKEN` env var and reads `--token` (default: the empty `GITHUB_TOKEN = ""` constant) — never paste a token into that constant. Unauthenticated PyGithub calls hit GitHub's low anonymous rate limit, and `--save` writes personal data to an untracked `users.csv`.
- `requirements.txt` lists `packaging` explicitly because, per its comment, Python 3.13.7's setuptools no longer bundles it; `google-analytics-data` is unpinned and only imported inside `fetch_google_analytics_stats`.

## Tests

There are none: no `tests/`, no pytest or coverage configuration, no `pyproject.toml`. CI on PRs is limited to `format.yml` (Ruff, docstring formatting, Prettier, codespell, Lychee link check) and `cla.yml`; the daily `analytics.yml` run is the only execution of the code. Validate a change by running `python fetch_stats.py` locally with a real `GITHUB_TOKEN` (and the other secrets if your change touches them), or a single fetcher against a scratch `Path` as shown in Commands, reading every `Warning:` line, inspecting `git diff -- data/`, then discarding `data/` before committing. Focused regression tests are out of scope by default (Core Principle 4).
