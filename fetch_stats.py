# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

import os
import sys
import time
from pathlib import Path

import requests

from utils import get_timestamp, post_json, write_json


def fetch_github_repos(org: str, token: str) -> list[dict]:
    """Fetch all public non-archived repos for org via GraphQL."""
    query = """
    query($org: String!, $cursor: String) {
      organization(login: $org) {
        repositories(first: 100, after: $cursor, isFork: false, privacy: PUBLIC) {
          pageInfo { hasNextPage endCursor }
          nodes { name stargazerCount isArchived isDisabled isLocked isMirror }
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
        repo_block = data["data"]["organization"]["repositories"]
        nodes = [
            n
            for n in repo_block["nodes"] or []
            if not (n["isArchived"] or n["isDisabled"] or n["isLocked"] or n["isMirror"])
        ]
        repos.extend(nodes)
        if not repo_block["pageInfo"]["hasNextPage"]:
            break
        cursor = repo_block["pageInfo"]["endCursor"]
        time.sleep(0.3)
    return repos


def fetch_github_contributors(org: str, repo: str, token: str) -> int:
    """Fetch contributor count for a repo using Link header pagination."""
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    url = f"https://api.github.com/repos/{org}/{repo}/contributors"
    r = requests.get(url, headers=headers, params={"per_page": 1, "anon": "true"}, timeout=60)
    if r.status_code != 200:
        return 0
    link = r.headers.get("Link", "")
    return int(link.split("page=")[-1].split(">")[0]) if "last" in link else len(r.json())


def fetch_github_stats(org: str, token: str, output: Path) -> dict:
    """Fetch and write GitHub org stats to JSON."""
    repos = fetch_github_repos(org, token)
    repo_data = []
    for r in sorted(repos, key=lambda x: -x["stargazerCount"]):
        contributors = fetch_github_contributors(org, r["name"], token)
        repo_data.append({"name": r["name"], "stars": r["stargazerCount"], "contributors": contributors})
        time.sleep(0.1)
    data = {
        "org": org,
        "total_stars": sum(r["stars"] for r in repo_data),
        "total_contributors": sum(r["contributors"] for r in repo_data),
        "public_repos": len(repo_data),
        "timestamp": get_timestamp(),
        "repos": repo_data,
    }
    write_json(output, data)
    return data


def fetch_pypi_package_stats(package: str, pepy_api_key: str = None) -> dict:
    """Fetch PyPI download statistics from pypistats.org (recent) and pepy.tech (total)."""
    stats = {"package": package, "last_day": 0, "last_week": 0, "last_month": 0, "total": 0}
    try:
        # Recent stats from pypistats.org
        r = requests.get(f"https://pypistats.org/api/packages/{package}/recent", timeout=30)
        if r.status_code == 200:
            data = r.json()["data"]
            stats["last_day"] = data.get("last_day", 0)
            stats["last_week"] = data.get("last_week", 0)
            stats["last_month"] = data.get("last_month", 0)
    except Exception as e:
        print(f"Warning: Failed to fetch recent stats for {package}: {e}")

    try:
        # All-time total from pepy.tech
        headers = {"X-API-Key": pepy_api_key} if pepy_api_key else {}
        r = requests.get(f"https://api.pepy.tech/api/v2/projects/{package}", headers=headers, timeout=30)
        if r.status_code == 200:
            data = r.json()
            stats["total"] = data.get("total_downloads", 0)
    except Exception as e:
        print(f"Warning: Failed to fetch total stats for {package}: {e}")

    time.sleep(1.0)  # Rate limiting: 10 calls/min for free pepy.tech
    return stats


def fetch_google_analytics_stats(property_id: str, credentials_json: str, output: Path) -> dict:
    """Fetch Google Analytics stats for a property."""
    import json

    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import DateRange, Metric, RunReportRequest
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

    data = {"property_id": property_id, "timestamp": get_timestamp()}

    for days, suffix in [(1, "1d"), (30, "30d"), (90, "90d"), (365, "365d")]:
        request = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[DateRange(start_date=f"{days}daysAgo", end_date="today")],
            metrics=metrics,
        )
        response = client.run_report(request)
        row = response.rows[0] if response.rows else None

        data[f"active_users_{suffix}"] = int(row.metric_values[0].value) if row else 0
        data[f"sessions_{suffix}"] = int(row.metric_values[1].value) if row else 0
        data[f"events_{suffix}"] = int(row.metric_values[2].value) if row else 0
        data[f"avg_session_duration_{suffix}"] = float(row.metric_values[3].value) if row else 0.0

    write_json(output, data)
    return data


def fetch_pypi_stats(packages: list[str], output: Path, pepy_api_key: str = None) -> dict:
    """Fetch and write PyPI stats to JSON."""
    stats = [fetch_pypi_package_stats(pkg, pepy_api_key) for pkg in packages]
    total_downloads = sum(s["total"] for s in stats)
    total_last_month = sum(s["last_month"] for s in stats)

    # Validate data - don't write if we got all zeros (API errors)
    if total_downloads == 0 and total_last_month == 0:
        print("Warning: All PyPI stats are zero, skipping write (possible API errors)")
        return {"total_downloads": 0, "total_last_month": 0, "timestamp": get_timestamp(), "packages": stats}

    data = {
        "total_downloads": total_downloads,
        "total_last_month": total_last_month,
        "timestamp": get_timestamp(),
        "packages": stats,
    }
    write_json(output, data)
    return data


if __name__ == "__main__":
    # GitHub stats
    org = os.getenv("ORG", "ultralytics")
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        sys.exit("Set GITHUB_TOKEN in env")
    github_output = Path(os.getenv("GITHUB_STATS_OUTPUT", "data/org_stars.json"))
    github_data = fetch_github_stats(org, token, github_output)
    print(
        f"✅ GitHub: {len(github_data['repos'])} repos, {github_data['total_stars']:,} stars, {github_data['total_contributors']:,} contributors"
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
    pypi_output = Path(os.getenv("PYPI_STATS_OUTPUT", "data/pypi_downloads.json"))
    pepy_api_key = os.getenv("PEPY_API_KEY")
    pypi_data = fetch_pypi_stats(pypi_packages, pypi_output, pepy_api_key)
    print(
        f"✅ PyPI: {len(pypi_data['packages'])} packages, {pypi_data['total_downloads']:,} total downloads, {pypi_data['total_last_month']:,} downloads (30d)"
    )

    # Google Analytics stats
    ga_property_id = "371754141"
    ga_credentials_json = os.getenv("GA_CREDENTIALS_JSON")
    if ga_credentials_json:
        ga_output = Path(os.getenv("GA_STATS_OUTPUT", "data/google_analytics.json"))
        ga_data = fetch_google_analytics_stats(ga_property_id, ga_credentials_json, ga_output)
        print(
            f"✅ GA: {ga_data['active_users_1d']:,} users, {ga_data['sessions_1d']:,} sessions, {ga_data['events_1d']:,} events (1d/30d/90d/365d)"
        )
