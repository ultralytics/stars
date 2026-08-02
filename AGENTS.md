# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, etc.) when working with code in this repository. CLAUDE.md is a symlink to this file.

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
uv pip install -r requirements.txt                        # install (CI uses: uv pip install --system -r requirements.txt)
GITHUB_TOKEN=YOUR_GITHUB_TOKEN python fetch_stats.py      # run the daily analytics fetcher (writes data/*.json)
python count_stars.py --token YOUR_GITHUB_TOKEN --days 30 # historical star tracking (optional --save writes users.csv)
```

- There is no test suite, coverage setup, or local lint config in this repo; formatting (Ruff, docformatter, Prettier, codespell) is applied to PRs automatically by `ultralytics/actions@main` via `.github/workflows/format.yml`.
- CI has no test matrix: `analytics.yml` runs a single `ubuntu-latest` job on Python `"3.x"`; both scripts require the live network and a GitHub token.
- Optional env vars for `fetch_stats.py`: `PEPY_API_KEY` (pepy.tech totals), `GA_CREDENTIALS_JSON` (Google Analytics), `PORTAL_API_KEY` (Platform stats), `ORG` (defaults to `ultralytics`).

## Architecture

This repo publishes Ultralytics org analytics as static JSON consumed via `raw.githubusercontent.com/ultralytics/stars/main/data/*.json`. `fetch_stats.py` is the entry point: it fetches GitHub org stats (GraphQL for repos, REST `Link` header for contributor counts), PyPI downloads (pypistats.org for recent, pepy.tech for all-time), Google Analytics, Reddit subscribers (via shields.io), and Ultralytics Platform metrics, writing six files under `data/`. `utils.py` holds shared helpers; its `safe_merge()` is the key invariant — on API failure new invalid/zero values fall back to the previous JSON so published totals never regress. `count_stars.py` is a standalone manual script with an inline `REPOS` list.

Publishing is gated by `analytics.yml`: a daily cron (`7 2 * * *`, 02:07 UTC) plus `workflow_dispatch` runs the fetcher, then commits `data/` to a timestamped `analytics-*` branch, opens a PR, sleeps 300s for checks, and squash-merges it with `--admin` (branch auto-deleted via trap). There is no package, release, or version-tag process — merging to `main` is the release.

## Conventions

- Every source file starts with the `# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license` header — Ultralytics Actions adds it automatically; don't add or revert it manually.
- Google-style docstrings and Prettier-formatted YAML/JSON/Markdown, enforced by the Ultralytics Actions bot on PRs — don't fight its auto-format commits.
- `data/*.json` files are bot-committed daily by `UltralyticsAssistant` ("Update Ultralytics analytics" PRs) — never hand-edit them, and expect them to have moved on `main` if a branch lives past 02:07 UTC.
- Dependencies are floor-pinned in `requirements.txt` and bumped monthly by Dependabot (`.github/dependabot.yml`); there is no version-bump or publish step to maintain.
