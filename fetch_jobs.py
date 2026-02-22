"""
Fetches entry-level IT jobs from The Muse API (no API key required).
Writes results to jobs.json for the static GitHub Pages site to consume.
"""

import json
import requests
from datetime import datetime, timezone

BASE_URL = "https://www.themuse.com/api/public/jobs"

# The Muse categories that map to IT / tech support roles
CATEGORIES = [
    "IT",
    "Data Science",
    "Software Engineering",
    "Data & Analytics",
]

LEVEL = "Entry Level"
PAGES_PER_CATEGORY = 3   # 20 results per page → up to 60 per category


def fetch_jobs():
    all_jobs = []
    seen_ids = set()

    for category in CATEGORIES:
        for page in range(1, PAGES_PER_CATEGORY + 1):
            try:
                resp = requests.get(
                    BASE_URL,
                    params={
                        "category": category,
                        "level": LEVEL,
                        "page": page,
                        "descending": "true",
                    },
                    timeout=15,
                )
                resp.raise_for_status()
                data = resp.json()
                results = data.get("results", [])

                if not results:
                    break   # no more pages for this category

                for job in results:
                    job_id = job.get("id")
                    if job_id in seen_ids:
                        continue
                    seen_ids.add(job_id)

                    # Flatten to a clean, minimal shape
                    all_jobs.append({
                        "id": job_id,
                        "title": job.get("name", ""),
                        "company": job.get("company", {}).get("name", ""),
                        "company_logo": (job.get("company", {}).get("refs", {}) or {}).get("logo_image", ""),
                        "locations": [
                            loc.get("name", "")
                            for loc in job.get("locations", [])
                        ],
                        "remote": any(
                            "remote" in loc.get("name", "").lower()
                            for loc in job.get("locations", [])
                        ),
                        "categories": [
                            cat.get("name", "")
                            for cat in job.get("categories", [])
                        ],
                        "levels": [
                            lvl.get("short_name", "")
                            for lvl in job.get("levels", [])
                        ],
                        "published": job.get("publication_date", ""),
                        "url": job.get("refs", {}).get("landing_page", ""),
                    })

                print(f"  [{category}] page {page}: {len(results)} jobs fetched")

            except Exception as e:
                print(f"  [{category}] page {page}: ERROR — {e}")
                break

    # Sort by published date descending
    all_jobs.sort(key=lambda j: j.get("published", ""), reverse=True)

    output = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(all_jobs),
        "jobs": all_jobs,
    }

    with open("jobs.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nDone — {len(all_jobs)} unique jobs written to jobs.json")


if __name__ == "__main__":
    fetch_jobs()
