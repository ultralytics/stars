# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests


def fetch_repos(org: str, token: str) -> list[dict]:
    """Paginate repos for org via GraphQL."""
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
        r = requests.post(
            "https://api.github.com/graphql",
            headers=headers,
            json={"query": query, "variables": {"org": org, "cursor": cursor}},
            timeout=60,
        )
        if r.status_code != 200:
            sys.exit(f"GitHub API error {r.status_code}: {r.text[:200]}")
        data = r.json()
        if "errors" in data:
            sys.exit(f"GitHub API errors: {data['errors']}")
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


def write_json(path: Path, org: str, repos: list[dict]) -> None:
    """Write compact JSON with totals and per-repo breakdown."""
    total = sum(r["stargazerCount"] for r in repos)
    payload = {
        "org": org,
        "total_stars": total,
        "public_repos": len(repos),
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "repos": [
            {"name": r["name"], "stars": r["stargazerCount"]} for r in sorted(repos, key=lambda x: -x["stargazerCount"])
        ],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")


if __name__ == "__main__":
    org = os.getenv("ORG", "ultralytics")
    token = os.getenv("GITHUB_TOKEN")
    out = Path(os.getenv("OUTPUT", "data/org_stars.json"))
    if not token:
        sys.exit("Set GITHUB_TOKEN in env.")
    out.parent.mkdir(parents=True, exist_ok=True)
    repos = fetch_repos(org, token)
    write_json(out, org, repos)
    print(f"✅ Wrote {out} with {len(repos)} repos, {sum(r['stargazerCount'] for r in repos):,} total stars")
