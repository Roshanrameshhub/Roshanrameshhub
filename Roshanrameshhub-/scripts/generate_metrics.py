#!/usr/bin/env python3
"""
ROSHAN // ENGINEERING SYSTEM — GitHub Metrics Generator
=======================================================
Aggregates public repository metadata, stars, language statistics,
and generates GitHub telemetry data snapshots.
"""

import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "github.json")
USERNAME = "Roshanrameshhub"


def main():
    print("=========================================================")
    print("  ROSHAN // GITHUB METRICS & TELEMETRY GENERATOR         ")
    print("=========================================================")

    # In production/Actions, can query GitHub API with GITHUB_TOKEN if present
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"User-Agent": "Roshan-Profile-Generator"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=updated", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                repos = json.loads(resp.read().decode("utf-8"))
                print(f"  [+] Fetched {len(repos)} repositories from GitHub API")

                # Compute language usage
                lang_counts = {}
                for r in repos:
                    l = r.get("language")
                    if l:
                        lang_counts[l] = lang_counts.get(l, 0) + 1

                total = sum(lang_counts.values()) or 1
                lang_dist = {k: round((v / total) * 100, 1) for k, v in lang_counts.items()}

                data = {
                    "username": USERNAME,
                    "fetched_at": datetime.now(timezone.utc).isoformat(),
                    "total_repos": len(repos),
                    "languages": lang_dist
                }

                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                print(f"  [+] Updated {DATA_FILE}")
                return
    except Exception as e:
        print(f"  [!] Notice: {e}. Preserving offline GitHub snapshot.")


if __name__ == "__main__":
    main()
