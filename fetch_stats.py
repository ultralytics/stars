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


def fetch_pypi_package_stats(package: str) -> dict:
    """Fetch PyPI download statistics for a package."""
    stats = {"package": package, "last_day": 0, "last_week": 0, "last_month": 0, "total": 0}
    try:
        # Recent stats
        r = requests.get(f"https://pypistats.org/api/packages/{package}/recent", timeout=30)
        if r.status_code == 200:
            data = r.json()["data"]
            stats.update(
                {
                    "last_day": data.get("last_day", 0),
                    "last_week": data.get("last_week", 0),
                    "last_month": data.get("last_month", 0),
                }
            )
        # Overall stats
        r = requests.get(f"https://pypistats.org/api/packages/{package}/overall", timeout=30)
        if r.status_code == 200:
            data = r.json()["data"]
            stats["total"] = sum(item.get("downloads", 0) for item in data)
    except Exception:
        pass
    return stats


def fetch_pypi_stats(packages: list[str], output: Path) -> dict:
    """Fetch and write PyPI stats to JSON."""
    stats = [fetch_pypi_package_stats(pkg) for pkg in packages]
    data = {
        "total_downloads": sum(s["total"] for s in stats),
        "total_last_month": sum(s["last_month"] for s in stats),
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
    pypi_data = fetch_pypi_stats(pypi_packages, pypi_output)
    print(
        f"✅ PyPI: {len(pypi_data['packages'])} packages, {pypi_data['total_downloads']:,} total downloads, {pypi_data['total_last_month']:,} downloads (30d)"
    )
