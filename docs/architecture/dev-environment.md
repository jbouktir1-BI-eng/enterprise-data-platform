# DEV Environment Architecture

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
