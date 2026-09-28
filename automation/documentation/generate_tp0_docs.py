from pathlib import Path

ROOT = Path("/home/adm_jalilb/projects/enterprise-data-platform")
DOCS = ROOT / "docs"

TP0_SUMMARY = """# TP0 — Development Environment and Project Foundation

## Objective

TP0 establishes the engineering foundation for the Enterprise Data & Decision Intelligence Platform before implementation of production data pipelines.

## Completed Scope

- WSL2 with Ubuntu 24.04.4 LTS
- Python 3.12.3
- Git 2.43.0 and GitHub SSH integration
- Docker 29.8.1 and Docker Compose v5.5.1
- OpenJDK 17.0.20.1
- Visual Studio Code 1.139.1
- DBeaver 25.2.3
- Power BI Desktop
- Repository initialization and source-control baseline
- Jira Scrum project configuration
- Jira REST API authentication
- Automated roadmap and backlog generation
- Jira metadata discovery and TP0 synchronization
- Technical documentation structure

## Canonical Repository Location

WSL:

`/home/adm_jalilb/projects/enterprise-data-platform`

Windows Explorer:

`\\\\wsl$\\Ubuntu\\home\\adm_jalilb\\projects\\enterprise-data-platform`

## Engineering Workflow

`BUILD → TEST → DEBUG → VALIDATE → COMMIT → NEXT`

## TP0 Actual Execution

Date: 2026-09-28

- Start: 14:00
- Measurement point: 17:47
- Gross elapsed time: 3h47
- Break excluded: 15 minutes
- Net recorded work: 3h32

## Sources of Truth

GitHub is the technical source of truth for code, architecture, documentation and version history.

Jira is the operational source of truth for backlog, sprint execution, estimates, worklogs, assignments, priorities and workflow status.

## Result

TP0 completed and validated.

Next engineering phase: Multi-Source Ingestion.
"""

ENVIRONMENT = """# TP0 — Development Environment

## Workstation

| Component | Version / State |
|---|---|
| Host OS | Windows 11 Pro 64-bit |
| Linux environment | WSL2 / Ubuntu 24.04.4 LTS |
| Python | 3.12.3 |
| Git | 2.43.0 |
| Docker | 29.8.1 |
| Docker Compose | v5.5.1 |
| OpenJDK | 17.0.20.1 |
| VS Code | 1.139.1 |
| DBeaver | 25.2.3 |
| Power BI Desktop | Installed |

Docker Desktop is integrated with WSL2.

## Repository

Canonical path:

`/home/adm_jalilb/projects/enterprise-data-platform`

Remote:

`git@github.com:jbouktir1-BI-eng/enterprise-data-platform.git`

Branch:

`main`

Initial commit:

`3751ffb chore: initialize enterprise data platform repository`

## Secret Management

Development Jira credentials are stored locally in:

`/home/adm_jalilb/projects/enterprise-data-platform/.env`

Variable names:

- `JIRA_URL`
- `JIRA_EMAIL`
- `JIRA_API_TOKEN`

Secret values are never stored in documentation or source code.

`.env` is excluded from Git through `.gitignore`.
"""
JIRA_SETUP = """# TP0 — Jira Setup

## Project

- Project: Enterprise Data and Decision Intelligence Platform
- Project key: SCRUM
- Project ID: 10000
- Board: SCRUM board
- Methodology: Scrum

## Workflow

`Idea → To Do → In Progress → In Review → Done`

## Issue Hierarchy

Jira discovery confirmed:

- Epic — hierarchy level 1
- Feature — hierarchy level 0
- Task — hierarchy level 0
- Subtask — hierarchy level -1

Feature and Task are peers. Therefore a native
`Epic → Feature → Task → Subtask` hierarchy is not used.

## Backlog Automation

Automation location:

`automation/jira/`

The automated roadmap contains:

- 12 Epics
- 48 Features
- 328 estimated hours

Scripts implemented:

- `jira_discover.py`
- `backlog_dry_run.py`
- `generate_detailed_backlog.py`
- `create_backlog.py`
- `sync_tp0.py`
- `discover_structure.py`
- `finalize_tp0.py`

## Authentication

Jira REST API authentication was validated with HTTP 200 using a Classic API token stored securely in `.env`.

## Sprint

TP0 was assigned to `SCRUM Sprint 0`.

## TP0 Completion

Epic `SCRUM-5 — W01 Environment & DEV` and its four Features were completed and transitioned to Done.

Recorded TP0 work: 3h32, excluding a 15-minute break.
"""

VALIDATION = """# TP0 — Validation Evidence

## Repository

- Canonical WSL repository path verified
- Git repository initialized
- Main branch active
- GitHub SSH remote configured
- `.env` excluded by `.gitignore`

## Runtime

Python, Git, Docker, Docker Compose and Java installations were validated.

## Jira

- REST API authentication: HTTP 200
- Project discovery: OK
- Jira structure discovery: OK
- Backlog dry-run: OK
- Jira backlog creation: OK
- TP0 synchronization: OK
- TP0 finalization: OK

## Backlog

- Epics: 12
- Features: 48
- Total estimated effort: 328 hours

## TP0

- Status: Done
- Net recorded work: 3h32
- Break excluded: 15 minutes

## Engineering Gate

TP0 technical foundation is ready for source-control validation and final commit before TP1 begins.
"""
TROUBLESHOOTING = """# TP0 — Issues and Resolutions

## Jira URL Typo
Issue: Jira URL initially used `atlassain.net`.

Resolution: corrected to `atlassian.net`.

## Jira Scoped Token Authentication
Issue: scoped API token returned HTTP 401 with scope mismatch.

Resolution: switched to a Classic API token. Authentication returned HTTP 200.

## Jira Hierarchy Assumption
Issue: initial design assumed Feature could parent Task.

Root cause: Jira discovery showed Feature and Task are both hierarchy level 0.

Resolution: use supported Jira hierarchy and avoid invalid parent relationships.

## Incomplete Jira Metadata
Issue: initial tickets lacked execution metadata.

Resolution: discovery and synchronization scripts populated assignment, priority, sprint, dates, estimates, story points, worklogs and final status.

## Sample Jira Tickets
Issue: SCRUM-3 and SCRUM-4 were temporary test tickets.

Resolution: removed during TP0 synchronization.

## Work Time Calculation
Gross session: 3h47.

Break: 15 minutes.

Net Jira worklog: 3h32.

## Missing tree Command
Issue: `tree` was not installed in Ubuntu.

Resolution: used the standard `find` command instead of adding an unnecessary dependency.

## Duplicate Backlog Risk
Issue: `create_backlog.py` is not currently idempotent.

Risk: rerunning it can create duplicate Jira issues.

Resolution: do not rerun blindly. Idempotency is a future automation improvement.

## Documentation Here-Document Failure
Issue: a large Bash here-document paste left the terminal waiting at the `>` continuation prompt.

Resolution: cancelled with Ctrl+C and switched to controlled generation through a Python documentation script.
"""

ARCHITECTURE = """# DEV Environment Architecture

## Purpose

The DEV environment provides a controlled engineering workspace for building and validating the Enterprise Data & Decision Intelligence Platform.

## Logical Architecture

Windows 11 Pro
→ WSL2 / Ubuntu 24.04.4 LTS
→ Git + Python + Java + Docker CLI
→ Enterprise Data Platform repository

External integrations:

- GitHub through SSH
- Jira Cloud through HTTPS REST API
- Docker Desktop through WSL2 integration

## Responsibility Boundaries

### GitHub
Source code, technical documentation, architecture, automation and version history.

### Jira
Planning, estimates, sprint execution, assignments, priorities, worklogs and workflow status.

## Security

Secrets remain outside source control in `.env`.

No credentials or API tokens are committed to Git.

## Environment Strategy

DEV is used for implementation, testing and technical validation.

PROD changes require an explicit approval gate and are not performed directly from DEV without validation.

## Engineering Gate

Changes follow:

`BUILD → TEST → DEBUG → VALIDATE → COMMIT → NEXT`
"""

FILES = {
    "tp0/README.md": TP0_SUMMARY,
    "tp0/environment.md": ENVIRONMENT,
    "tp0/jira-setup.md": JIRA_SETUP,
    "tp0/validation.md": VALIDATION,
    "troubleshooting/tp0-issues.md": TROUBLESHOOTING,
    "architecture/dev-environment.md": ARCHITECTURE,
}

for relative_path, content in FILES.items():
    path = DOCS / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"GENERATED: {path.relative_to(ROOT)}")

print("TP0 DOCUMENTATION: OK")