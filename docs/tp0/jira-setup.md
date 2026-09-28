# TP0 — Jira Setup

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
