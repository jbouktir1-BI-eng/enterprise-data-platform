# TP1 - Multi-Source Ingestion

## Purpose

Build a reproducible enterprise multi-source ingestion foundation.

## Architecture

24 source datasets feed a common ingestion framework.

Source -> Raw -> Bronze -> Reconciliation -> Downstream Processing

## Technologies

- Python 3
- PostgreSQL
- Docker
- CSV
- JSON
- Git / GitHub
- Jira

## Controls

- Referential integrity
- Metadata capture
- SHA-256 source fingerprinting
- Idempotent ingestion
- Incremental change detection
- Error logging
- Source-to-Bronze reconciliation
- Business-rule validation
- Secret isolation through environment variables

## Result

TP1 core pipeline passed with zero reconciliation errors.
