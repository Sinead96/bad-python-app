import json
import os
import requests

TOKEN = os.environ["SEMGREP_API_TOKEN"]  # set this first
SINCE = "2026-01-01T00:00:00Z"
API = "https://semgrep.dev/api/v1"

session = requests.Session()
session.headers["Authorization"] = f"Bearer {TOKEN}"

slug = session.get(f"{API}/deployments").json()["deployments"][0]["slug"]
print(f"Pulling findings for '{slug}' since {SINCE}...")

# Page through 100 at a time until a page comes back short.
findings, page = [], 0
while True:
    batch = session.get(
        f"{API}/deployments/{slug}/findings",
        params={"since": SINCE, "page": page, "page_size": 100, "dedup": "true"},
    ).json()["findings"]
    findings += batch
    if len(batch) < 100:
        break
    page += 1

with open("semgrep_findings.json", "w") as f:
    json.dump(findings, f, indent=2)

print(f"Done — {len(findings)} findings saved to semgrep_findings.json")
