# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, etc.) when working with code in this repository. CLAUDE.md is a symlink to this file.

## Core Principles (CRITICAL)

Respecting these principles is critical for every PR.

**Less is more. The simplest solution is the best solution.**

The action hierarchy for every change: **Delete > Replace > Add**. The best code change is a deletion. The second best is modifying what exists. Adding new code is the last resort.

1. **Minimal**: The simplest solution that works. Do not over-engineer, over-abstract, or add code just in case. Three similar lines beat a premature abstraction. Avoid error handling for impossible states, feature flags, compatibility shims, or policy scaffolding unless they are truly required.
2. **Solve at the source**: Do not hack fixes. Solve problems at their root. If something is broken, fix or remove the broken thing. Never patch over a broken abstraction, add workarounds, or add synchronization code for state that should not be duplicated.
3. **Delete ruthlessly**: When replacing code, delete what it replaced. Remove unused imports, functions, types, files, and commented-out code. Git preserves history. Run the repo's relevant dead-code or cleanup check when available.
4. **Replace > Add**: Modify existing code over adding new code. Edit existing files, extend existing components or functions with minimal parameters, and reuse existing utilities. If creating a new file, first prove it cannot fit cleanly in an existing file.
5. **Check existing**: Search the entire repo before creating anything new. If a feature, component, helper, responder, workflow, or utility already solves a similar problem, reuse or adapt it and delete the duplicate path.
6. **Deduplicate**: Do not duplicate existing code when updating the repo. Consolidate or refactor duplicates you find when it is in scope and low risk.
7. **Zero Regression**: Do not break existing features or workflows unless the PR intentionally removes them with evidence.
8. **Production ready**: All changes must be thoroughly debugged, validated, and production ready.

**When fixing bugs, ask: "What can I delete?" before "What can I replace?" before "What should I add?"**

## PR Workflow

After opening a PR:

1. Wait for the automated PR review and auto-format commit from Ultralytics Actions (`format.yml`), then pull and address every finding.
2. Launch an independent adversarial review agent with cold context (just the PR diff and this file) to hunt for bugs, regressions, and Core Principles violations — use the Codex CLI, one fresh `codex exec` run per round. Fix, push, and repeat until a fresh run reports LGTM.
3. Never fight other commits: Ultralytics Actions pushes auto-format and header commits, and multiple users may work on the same PR. `git pull --rebase` before pushing; never force-push, reset, or revert commits you did not author.
4. After the PR merges, clean up: remove local worktrees and branches for it, then `git checkout main && git pull`.

## Commands

```bash
uv pip install -r requirements.txt                # install (CI uses: uv pip install --system -r requirements.txt)
GITHUB_TOKEN= < token > python fetch_stats.py     # run the daily analytics fetcher (writes data/*.json)
python count_stars.py --token 30 < token > --days # historical star tracking (optional --save writes users.csv)
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
