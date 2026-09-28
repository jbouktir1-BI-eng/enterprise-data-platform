import os
import requests
from pathlib import Path
from requests.auth import HTTPBasicAuth

ROOT = Path("/home/adm_jalilb/projects/enterprise-data-platform")

# Load .env without external dependency
for line in (ROOT / ".env").read_text().splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())

JIRA_URL = os.environ["JIRA_URL"].rstrip("/")
AUTH = HTTPBasicAuth(
    os.environ["JIRA_EMAIL"],
    os.environ["JIRA_API_TOKEN"],
)

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

EPIC = "SCRUM-5"

FEATURES = {
    "SCRUM-6": "Validate DEV environment",
    "SCRUM-7": "Configure repository standards",
    "SCRUM-8": "Validate Docker baseline",
    "SCRUM-9": "Document DEV architecture",
}

COMMIT = "f1c3771"

DOCS = [
    "docs/tp0/README.md",
    "docs/tp0/environment.md",
    "docs/tp0/jira-setup.md",
    "docs/tp0/validation.md",
    "docs/troubleshooting/tp0-issues.md",
    "docs/architecture/dev-environment.md",
]

def api(method, endpoint, **kwargs):
    response = requests.request(
        method,
        f"{JIRA_URL}{endpoint}",
        auth=AUTH,
        headers=HEADERS,
        timeout=30,
        **kwargs,
    )

    if response.status_code >= 400:
        raise RuntimeError(
            f"{method} {endpoint} -> "
            f"HTTP {response.status_code}: {response.text}"
        )

    return response

EPIC_DESCRIPTION = """TP0 establishes and validates the complete DEV engineering foundation for the Enterprise Data & Decision Intelligence Platform.

Scope:
- WSL2 / Ubuntu development environment
- Python, Git, Java and Docker baseline
- GitHub repository and SSH integration
- Jira Scrum project and REST API automation
- Automated 12-week backlog: 12 Epics / 48 Features / 328h
- TP0 technical documentation
- Security and source-control validation

Engineering workflow:
BUILD → TEST → DEBUG → VALIDATE → COMMIT → NEXT

Technical documentation:
""" + "\n".join(f"- {doc}" for doc in DOCS) + f"""

Git commit:
{COMMIT}

TP0 recorded execution time: 3h32
15-minute break excluded.
"""

FEATURE_DESCRIPTIONS = {
    "SCRUM-6": """Validated the DEV workstation and core runtime dependencies.

Validation covered WSL2 Ubuntu, Python, Git, Java, Docker, Docker Compose and development tooling.

Evidence is documented under docs/tp0/ and docs/architecture/.""",

    "SCRUM-7": f"""Established repository standards and source-control baseline.

Validated:
- canonical WSL repository location
- main branch
- GitHub SSH remote
- .gitignore
- .env exclusion
- automation and documentation structure

TP0 implementation commit: {COMMIT}""",

    "SCRUM-8": """Validated the Docker development baseline and WSL2 integration.

Previous Docker data was cleaned before the platform implementation baseline was established.

Docker and Docker Compose availability were successfully validated.""",

    "SCRUM-9": f"""Created the DEV architecture and TP0 technical documentation.

Documentation includes environment configuration, Jira setup, validation evidence, architecture and troubleshooting history.

Documentation commit: {COMMIT}"""
}

INCIDENTS_COMMENT = """TP0 troubleshooting record

1. Jira URL typo
Root cause: incorrect atlassain.net hostname.
Resolution: corrected to atlassian.net.

2. Jira scoped API token returned HTTP 401
Root cause: token scope did not match the Jira REST operation requirements.
Resolution: Classic API token used successfully; authentication returned HTTP 200.

3. Jira hierarchy assumption
Root cause: Feature and Task were assumed to be different parent/child levels.
Discovery confirmed both are hierarchy level 0.
Resolution: automation now respects the discovered Jira hierarchy.

4. Missing tree command
Root cause: tree package was not installed in Ubuntu.
Resolution: standard find command used; no unnecessary package added.

5. Backlog duplication risk
Root cause: create_backlog.py is not idempotent.
Control: script must not be rerun blindly. Future automation should implement duplicate protection.

6. Documentation generation terminal issue
Root cause: large Bash here-document paste left the shell waiting for its termination delimiter.
Resolution: cancelled and replaced with controlled Python documentation generation.

7. Documentation line-ending issue
Root cause: CRLF characters produced trailing-whitespace validation errors.
Resolution: converted the generator to Unix LF line endings and reran git diff --cached --check successfully.
"""
def adf(text):
    return {
        "type": "doc",
        "version": 1,
        "content": [{
            "type": "paragraph",
            "content": [{"type": "text", "text": text}]
        }]
    }


def update_description(issue_key, description):
    api(
        "PUT",
        f"/rest/api/3/issue/{issue_key}",
        json={"fields": {"description": adf(description)}},
    )
    print(f"DESCRIPTION: {issue_key} OK")


def add_comment(issue_key, comment):
    api(
        "POST",
        f"/rest/api/3/issue/{issue_key}/comment",
        json={"body": adf(comment)},
    )
    print(f"COMMENT: {issue_key} OK")


# Epic
update_description(EPIC, EPIC_DESCRIPTION)

# Features
for key, description in FEATURE_DESCRIPTIONS.items():
    update_description(key, description)

# Detailed troubleshooting history on the Epic
add_comment(EPIC, INCIDENTS_COMMENT)

FINAL_GATE_COMMENT = f"""TP0 GATE — CLOSED / VALIDATED

Technical implementation: COMPLETE
Jira execution tracking: COMPLETE
Documentation: COMPLETE
Validation: PASSED
Git commit: {COMMIT}
GitHub main branch: PUSHED

Documentation:
""" + "\n".join(f"- {doc}" for doc in DOCS) + """

Final result:
TP0 development foundation is validated and ready for TP1 — Multi-Source Ingestion.
"""

add_comment(EPIC, FINAL_GATE_COMMENT)

print()
print("TP0 JIRA GOVERNANCE: OK")
print("TP0 GATE: CLOSED / VALIDATED")