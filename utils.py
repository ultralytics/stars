# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests


def retry_request(func, *args, retries: int = 3, backoff: float = 2.0, **kwargs):
    """Retry a request function with exponential backoff on exceptions and 5xx/429 errors."""
    last_error = None
    retries = max(1, retries)  # Ensure at least one attempt
    for attempt in range(retries):
        try:
            response = func(*args, **kwargs)
            # Retry on server errors (5xx) and rate limits (429)
            if response.status_code >= 500 or response.status_code == 429:
                last_error = requests.RequestException(f"HTTP {response.status_code}: {response.text[:200]}")
                if attempt < retries - 1:
                    wait = backoff * (2**attempt)
                    print(f"Retry {attempt + 1}/{retries} after {wait}s: HTTP {response.status_code}")
                    time.sleep(wait)
                continue
            return response
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


def post_json(url: str, headers: dict, payload: dict, timeout: int = 60, retries: int = 3) -> dict:
    """POST JSON to URL with retry and error handling."""
    last_error = None
    for attempt in range(retries):
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=timeout)
            if r.status_code == 200:
                return r.json()
            # Retry on server errors (5xx), fail immediately on client errors (4xx)
            if r.status_code >= 500:
                last_error = f"HTTP {r.status_code}: {r.text[:200]}"
                if attempt < retries - 1:
                    wait = 2.0 * (2**attempt)
                    print(f"Retry {attempt + 1}/{retries} after {wait}s: {last_error}")
                    time.sleep(wait)
                continue
            sys.exit(f"HTTP {r.status_code}: {r.text[:200]}")
        except (requests.RequestException, requests.Timeout) as e:
            last_error = str(e)
            if attempt < retries - 1:
                wait = 2.0 * (2**attempt)
                print(f"Retry {attempt + 1}/{retries} after {wait}s: {e}")
                time.sleep(wait)
    sys.exit(f"Failed after {retries} retries: {last_error}")


def write_json(path: Path, data: dict) -> None:
    """Write compact JSON with trailing newline."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")


def get_timestamp() -> str:
    """Return ISO 8601 timestamp with Z suffix."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
