# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import requests

from utils import (
    get_timestamp,
    post_json,
    read_json,
    retry_request,
    safe_merge,
    write_json,
)


def fetch_github_repos(org: str, token: str) -> list[dict]:
    """Fetch all public non-archived repos for org via GraphQL."""
    query = """
    query($org: String!, $cursor: String) {
      organization(login: $org) {
        repositories(first: 100, after: $cursor, isFork: false, privacy: PUBLIC) {
          pageInfo { hasNextPage endCursor }
          nodes { name stargazerCount forkCount issues { totalCount } pullRequests { totalCount } isArchived isDisabled isLocked isMirror }
        }
      }
    }
    """
    headers = {"Authorization": f"Bearer {token}"}
    cursor, repos = None, []
    while True:
        data = post_json(
            "https://api.github.com/graphql", headers, {"query": query, "variables": {"org": org, "cursor": cursor}}
        )
        if "errors" in data:
            sys.exit(f"GraphQL errors: {data['errors']}")

        # Safely navigate nested response structure
        org_data = data.get("data", {}).get("organization")
        if not org_data:
            sys.exit(f"Organization '{org}' not found or inaccessible")
        repo_block = org_data.get("repositories", {})
        nodes = repo_block.get("nodes") or []

        # Filter out archived/disabled/locked/mirror repos
        for n in nodes:
            if n and not (n.get("isArchived") or n.get("isDisabled") or n.get("isLocked") or n.get("isMirror")):
                repos.append(n)

        page_info = repo_block.get("pageInfo", {})
        if not page_info.get("hasNextPage"):
            break
        cursor = page_info.get("endCursor")
        time.sleep(0.3)
    return repos


def fetch_github_contributors(org: str, repo: str, token: str) -> int:
    """Fetch contributor count for a repo using Link header pagination with retry."""
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    url = f"https://api.github.com/repos/{org}/{repo}/contributors"
    try:
        r = retry_request(requests.get, url, headers=headers, params={"per_page": 1, "anon": "true"}, timeout=60)
        if r.status_code != 200:
            print(f"Warning: Failed to fetch contributors for {repo}: HTTP {r.status_code}")
            return 0
        link = r.headers.get("Link", "")
        if "last" in link:
            # Parse last page number from Link header
            return int(link.split("page=")[-1].split(">")[0])
        # No pagination - count items in response
        data = r.json()
        return len(data) if isinstance(data, list) else 0
    except Exception as e:
        print(f"Warning: Failed to fetch contributors for {repo}: {e}")
        return 0


def fetch_github_stats(org: str, token: str, output: Path) -> dict:
    """Fetch GitHub org stats, merge with existing data, and write to JSON."""
    existing = read_json(output)
    old_repos = {r["name"]: r for r in existing.get("repos", [])}

    repos = fetch_github_repos(org, token)
    repo_data = []
    for r in sorted(repos, key=lambda x: -x["stargazerCount"]):
        contributors = fetch_github_contributors(org, r["name"], token)
        new_repo = {
            "name": r["name"],
            "stars": r["stargazerCount"],
            "forks": r["forkCount"],
            "issues": r["issues"]["totalCount"],
            "pull_requests": r["pullRequests"]["totalCount"],
            "contributors": contributors,
        }
        safe_merge(
            new_repo,
            old_repos.get(r["name"], {}),
            ("stars", "forks", "issues", "pull_requests", "contributors"),
            r["name"],
        )
        repo_data.append(new_repo)
        time.sleep(0.1)

    # If API returned no repos, keep existing repos
    if not repo_data and existing.get("repos"):
        print("Warning: GitHub API returned no repos, keeping existing data")
        repo_data = existing["repos"]

    data = {
        "org": org,
        "total_stars": sum(r["stars"] for r in repo_data),
        "total_forks": sum(r["forks"] for r in repo_data),
        "total_issues": sum(r["issues"] for r in repo_data),
        "total_pull_requests": sum(r["pull_requests"] for r in repo_data),
        "total_contributors": sum(r["contributors"] for r in repo_data),
        "public_repos": len(repo_data),
        "timestamp": get_timestamp(),
        "repos": repo_data,
    }
    write_json(output, data)
    return data


def fetch_pypi_package_stats(package: str, pepy_api_key: str | None = None) -> dict:
    """Fetch PyPI download statistics from pypistats.org (recent) and pepy.tech (total)."""
    stats = {"package": package, "last_day": 0, "last_week": 0, "last_month": 0, "total": 0}

    # Recent stats from pypistats.org (with retry)
    try:
        r = retry_request(requests.get, f"https://pypistats.org/api/packages/{package}/recent", timeout=30)
        if r.status_code == 200:
            data = r.json().get("data", {})
            stats["last_day"] = data.get("last_day", 0) or 0
            stats["last_week"] = data.get("last_week", 0) or 0
            stats["last_month"] = data.get("last_month", 0) or 0
    except Exception as e:
        print(f"Warning: Failed to fetch recent stats for {package}: {e}")

    # All-time total from pepy.tech (with retry)
    try:
        headers = {"X-API-Key": pepy_api_key} if pepy_api_key else {}
        r = retry_request(requests.get, f"https://api.pepy.tech/api/v2/projects/{package}", headers=headers, timeout=30)
        if r.status_code == 200:
            data = r.json()
            stats["total"] = data.get("total_downloads", 0) or 0
    except Exception as e:
        print(f"Warning: Failed to fetch total stats for {package}: {e}")

    time.sleep(1.0)  # Rate limiting: 10 calls/min for free pepy.tech
    return stats


def fetch_google_analytics_stats(property_id: str, credentials_json: str, output: Path) -> dict | None:
    """Fetch Google Analytics stats, merge with existing data, and write to JSON."""
    import json

    existing = read_json(output)

    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.analytics.data_v1beta.types import (
            DateRange,
            Metric,
            RunReportRequest,
        )
        from google.oauth2 import service_account

        credentials_info = json.loads(credentials_json)
        credentials = service_account.Credentials.from_service_account_info(credentials_info)
        client = BetaAnalyticsDataClient(credentials=credentials)

        metrics = [
            Metric(name="activeUsers"),
            Metric(name="sessions"),
            Metric(name="eventCount"),
            Metric(name="averageSessionDuration"),
        ]

        data = {"property_id": property_id, "timestamp": get_timestamp(), "periods": {}}

        for days, suffix in [(1, "1d"), (7, "7d"), (30, "30d"), (90, "90d"), (365, "365d")]:
            request = RunReportRequest(
                property=f"properties/{property_id}",
                date_ranges=[DateRange(start_date=f"{days}daysAgo", end_date="today")],
                metrics=metrics,
            )
            response = client.run_report(request)
            row = response.rows[0] if response.rows else None

            data["periods"][suffix] = {
                "active_users": int(row.metric_values[0].value) if row else 0,
                "sessions": int(row.metric_values[1].value) if row else 0,
                "events": int(row.metric_values[2].value) if row else 0,
                "avg_session_duration": float(row.metric_values[3].value) if row else 0.0,
            }

        old_periods = existing.get("periods", {})
        for suffix, period in data["periods"].items():
            safe_merge(
                period,
                old_periods.get(suffix, {}),
                ("active_users", "sessions", "events", "avg_session_duration"),
                f"GA {suffix}",
            )

        write_json(output, data)
        return data

    except Exception as e:
        print(f"Warning: Failed to fetch Google Analytics stats: {e}")
        return existing if existing.get("periods") else None


def parse_abbreviated_number(value: str) -> int:
    """Parse abbreviated numbers like '1.4k' or '2.5M' to integers."""
    try:
        value = value.strip().lower()
        if not value:
            return 0
        multipliers = {"k": 1_000, "m": 1_000_000, "b": 1_000_000_000}
        for suffix, mult in multipliers.items():
            if value.endswith(suffix):
                return int(float(value[:-1]) * mult)
        return int(float(value.replace(",", "")))
    except (ValueError, AttributeError):
        return 0


def fetch_reddit_stats(subreddit: str, output: Path) -> dict:
    """Fetch Reddit subscriber count, merge with existing data, and write to JSON."""
    existing = read_json(output)
    subscribers = 0

    try:
        # Use shields.io JSON endpoint with retry - they have special Reddit API access
        r = retry_request(
            requests.get, f"https://img.shields.io/reddit/subreddit-subscribers/{subreddit}.json", timeout=30
        )
        if r.status_code == 200:
            data = r.json()
            subscribers = parse_abbreviated_number(data.get("value", "0"))
    except Exception as e:
        print(f"Warning: shields.io Reddit endpoint failed: {e}")

    result = {"subreddit": subreddit, "subscribers": subscribers, "timestamp": get_timestamp()}
    safe_merge(result, existing, ("subscribers",), "Reddit")
    write_json(output, result)
    return result


def fetch_pypi_stats(packages: list[str], output: Path, pepy_api_key: str | None = None) -> dict:
    """Fetch PyPI stats, merge with existing data per-package, and write to JSON."""
    existing = read_json(output)
    old_packages = {p["package"]: p for p in existing.get("packages", [])}

    stats = []
    for pkg in packages:
        new_pkg = fetch_pypi_package_stats(pkg, pepy_api_key)
        safe_merge(new_pkg, old_packages.get(pkg, {}), ("last_day", "last_week", "last_month", "total"), pkg)
        stats.append(new_pkg)

    data = {
        "total_downloads": sum(s["total"] for s in stats),
        "total_last_month": sum(s["last_month"] for s in stats),
        "timestamp": get_timestamp(),
        "packages": stats,
    }
    write_json(output, data)
    return data


if __name__ == "__main__":
    BASE_DIR = Path(__file__).parent

    # GitHub stats
    org = os.getenv("ORG", "ultralytics")
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        sys.exit("Set GITHUB_TOKEN in env")
    github_output = BASE_DIR / "data/github.json"
    github_data = fetch_github_stats(org, token, github_output)
    print(
        f"✅ GitHub: {len(github_data['repos'])} repos, {github_data['total_stars']:,} stars, {github_data['total_forks']:,} forks, {github_data['total_issues']:,} issues, {github_data['total_pull_requests']:,} PRs, {github_data['total_contributors']:,} contributors"
    )

    # PyPI stats
    pypi_packages = [
        "ultralytics",
        "ultralytics-actions",
        "ultralytics-thop",
        "hub-sdk",
        "mkdocs-ultralytics-plugin",
        "ultralytics-autoimport",
    ]
    pypi_output = BASE_DIR / "data/pypi.json"
    pepy_api_key = os.getenv("PEPY_API_KEY")
    pypi_data = fetch_pypi_stats(pypi_packages, pypi_output, pepy_api_key)
    print(
        f"✅ PyPI: {len(pypi_data['packages'])} packages, {pypi_data['total_downloads']:,} total downloads, {pypi_data['total_last_month']:,} downloads (30d)"
    )

    # Google Analytics stats
    ga_property_id = "371754141"
    ga_credentials_json = os.getenv("GA_CREDENTIALS_JSON")
    ga_data = None
    if ga_credentials_json:
        ga_output = BASE_DIR / "data/google_analytics.json"
        ga_data = fetch_google_analytics_stats(ga_property_id, ga_credentials_json, ga_output)
        if ga_data:
            day = ga_data["periods"]["1d"]
            print(
                f"✅ GA: {day['active_users']:,} users, {day['sessions']:,} sessions, {day['events']:,} events (1d/7d/30d/90d/365d)"
            )

    # Reddit stats
    reddit_output = BASE_DIR / "data/reddit.json"
    reddit_data = fetch_reddit_stats("ultralytics", reddit_output)
    print(f"✅ Reddit: {reddit_data['subscribers']:,} subscribers")

    # Create summary with field-level merge from existing
    existing_summary = read_json(BASE_DIR / "data/summary.json")
    summary = {
        "total_stars": github_data["total_stars"],
        "total_forks": github_data["total_forks"],
        "total_issues": github_data["total_issues"],
        "total_pull_requests": github_data["total_pull_requests"],
        "total_downloads": pypi_data["total_downloads"],
        "events_per_day": round(float(ga_data["periods"]["90d"]["events"]) / 90.0) if ga_data else 0,  # 90-day mean
        "total_contributors": github_data["total_contributors"],
        "reddit_subscribers": reddit_data["subscribers"],
        "timestamp": get_timestamp(),
    }
    safe_merge(summary, existing_summary, [k for k in summary if k != "timestamp"], "summary")
    summary_output = BASE_DIR / "data/summary.json"
    write_json(summary_output, summary)
    print(
        f"✅ Summary: {summary['total_stars']:,} stars, {summary['total_forks']:,} forks, {summary['total_issues']:,} issues, {summary['total_pull_requests']:,} PRs, {summary['total_downloads']:,} downloads, {summary['events_per_day']:,} events/day, {summary['total_contributors']:,} contributors, {summary['reddit_subscribers']:,} reddit"
    )
