# TP0 — Development Environment

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
