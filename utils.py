# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests


def retry_request(func, *args, retries: int = 3, backoff: float = 2.0, **kwargs):
    """Retry a request function with exponential backoff."""
    last_error = None
    for attempt in range(retries):
        try:
            return func(*args, **kwargs)
        except (requests.RequestException, requests.Timeout) as e:
            last_error = e
            if attempt < retries - 1:
                wait = backoff * (2**attempt)
                print(f"Retry {attempt + 1}/{retries} after {wait}s: {e}")
                time.sleep(wait)
    raise last_error


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
