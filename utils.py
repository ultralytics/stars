# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests


def fetch_json(url: str, headers: dict | None = None, timeout: int = 60) -> dict:
    """Fetch JSON from URL with error handling."""
    r = requests.get(url, headers=headers, timeout=timeout)
    if r.status_code != 200:
        sys.exit(f"HTTP {r.status_code}: {r.text[:200]}")
    return r.json()


def post_json(url: str, headers: dict, payload: dict, timeout: int = 60) -> dict:
    """POST JSON to URL with error handling."""
    r = requests.post(url, headers=headers, json=payload, timeout=timeout)
    if r.status_code != 200:
        sys.exit(f"HTTP {r.status_code}: {r.text[:200]}")
    return r.json()


def write_json(path: Path, data: dict) -> None:
    """Write compact JSON with trailing newline."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")


def get_timestamp() -> str:
    """Return ISO 8601 timestamp with Z suffix."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
