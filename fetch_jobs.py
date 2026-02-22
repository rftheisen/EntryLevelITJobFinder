"""
Fetches entry-level IT jobs from The Muse API (no API key required).
Writes results to jobs.json for the static GitHub Pages site to consume.
"""

import json
import requests
from datetime import datetime, timezone

BASE_URL = "https://www.themuse.com/api/public/jobs"

# Muse categories most likely to contain IT roles
CATEGORIES = [
    "IT",
    "Software Engineering",
    "Data Science",
    "Data & Analytics",
]

LEVEL = "Entry Level"
PAGES_PER_CATEGORY = 5   # 20 results per page → up to 100 per category (before filtering)

# ── Title allowlist ───────────────────────────────────────────────────────────
# A job title must contain at least one of these to be included.
# Keeps only genuine IT / tech roles.
IT_TITLE_KEYWORDS = [
    # Help desk / support (very specific — safe standalone)
    "it support", "help desk", "helpdesk", "service desk",
    "technical support", "tech support", "desktop support",
    "it technician", "field technician", "computer technician",
    "it specialist", "it coordinator", "it analyst",
    # Infrastructure / networking
    "network engineer", "network admin", "network administrator",
    "sysadmin", "system admin", "systems admin", "system administrator",
    "systems administrator", "infrastructure engineer",
    "cloud engineer", "cloud architect", "cloud admin",
    "devops", "site reliability", "linux admin",
    "active directory", "virtualization",
    # Security
    "security engineer", "security analyst", "security architect",
    "cybersecurity", "cyber security", "soc analyst",
    "information security", "infosec", "penetration tester",
    "vulnerability analyst", "security operations",
    # Development (require "software", "web", "junior", or specific lang/stack)
    "software engineer", "software developer",
    "web developer", "web engineer",
    "full stack", "fullstack", "front end developer", "frontend developer",
    "back end developer", "backend developer",
    "mobile developer", "ios developer", "android developer",
    "junior developer", "junior software", "junior engineer",
    "junior java", "junior python", "junior cloud",
    "junior devops", "junior data", "junior android",
    "junior salesforce", "junior game", "junior service desk",
    "associate developer", "associate engineer", "associate software",
    "entry level developer", "entry level engineer", "entry level software",
    "programmer", "java developer", "python developer",
    "javascript developer", "react developer", ".net developer",
    "salesforce developer", "application developer",
    # Data
    "data analyst", "data engineer", "data scientist",
    "database administrator", "database analyst", "database engineer",
    "sql developer", "business intelligence", "bi analyst",
    "machine learning engineer", "ml engineer", "data warehouse",
    # QA / testing
    "qa engineer", "quality assurance engineer", "qa analyst",
    "test engineer", "automation engineer", "software tester",
    # IT project / product
    "it project manager", "technical project manager",
    "product manager", "product analyst",
    "scrum master", "agile coach",
    "ux designer", "ui designer", "ui/ux",
    # General IT (phrase-level — not single broad words)
    "solutions engineer", "solutions architect",
    "systems analyst", "systems engineer",
    "technical analyst", "technology analyst",
    "application support", "business application",
    "it graduate", "it trainee", "it intern",
]

# ── Title blocklist ───────────────────────────────────────────────────────────
# If a title contains any of these, drop it regardless of category.
NON_IT_TITLE_KEYWORDS = [
    # Food / hospitality
    "meal", "food", "chicken", "cook", "chef", "kitchen", "culinary",
    "rotisserie", "deli", "bakery", "meat", "restaurant", "barista",
    # Retail / trade
    "cashier", "retail", "store associate", "sales associate",
    "merchandiser", "stocking",
    # Transport / logistics
    "delivery driver", "driver", "forklift", "warehouse", "logistics",
    "supply chain coordinator", "fulfillment",
    # Healthcare (non-IT)
    "nurse", "nursing", "medical assistant", "dental", "pharmacy tech",
    "therapist", "physical therapy", "occupational therapy",
    "phlebotomist", "emt", "paramedic",
    # Finance / trading (non-IT)
    "trader", "lending", "portfolio analyst", "financial advisor",
    "insurance agent", "mortgage", "real estate agent", "broker",
    "underwriter", "actuary",
    # Facilities / labour
    "cleaning", "janitorial", "landscaping", "construction worker",
    "electrician", "plumber", "hvac",
    # Admin (non-IT)
    "customer service representative", "call center",
    "receptionist", "administrative assistant",
    "processos administrativos", "contas a pagar",  # Portuguese admin roles
    # Production / manufacturing (non-IT)
    "production engineer", "engineer - production",
    "manufacturing engineer", "process engineer",
    "industrial engineer", "quality control inspector", "assembly",
]


def is_it_job(title: str) -> bool:
    """Return True only if the title looks like a genuine IT/tech role."""
    lower = title.lower()

    # Blocklist check first — fast reject
    for bad in NON_IT_TITLE_KEYWORDS:
        if bad in lower:
            return False

    # Must match at least one IT keyword
    for kw in IT_TITLE_KEYWORDS:
        if kw in lower:
            return True

    return False


def fetch_jobs():
    all_jobs = []
    seen_ids = set()
    dropped = 0

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

                kept = 0
                for job in results:
                    job_id = job.get("id")
                    if job_id in seen_ids:
                        continue
                    seen_ids.add(job_id)

                    title = job.get("name", "")

                    # Skip non-IT roles
                    if not is_it_job(title):
                        dropped += 1
                        continue

                    kept += 1
                    all_jobs.append({
                        "id": job_id,
                        "title": title,
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

                print(f"  [{category}] page {page}: {kept} kept / {len(results) - kept} filtered")

            except Exception as e:
                print(f"  [{category}] page {page}: ERROR — {e}")
                break

    # Sort by published date descending
    all_jobs.sort(key=lambda j: j.get("published", ""), reverse=True)

    print(f"\nTotal dropped (non-IT): {dropped}")

    output = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(all_jobs),
        "jobs": all_jobs,
    }

    with open("jobs.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"Done — {len(all_jobs)} IT jobs written to jobs.json")


if __name__ == "__main__":
    fetch_jobs()
