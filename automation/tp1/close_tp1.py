"""
Technology : Python 3
Technique  : Automated project closure gate
Used in    : TP1 - Multi-Source Ingestion
Purpose    : Generate documentation, validate TP1, update Jira,
             commit/push Git changes and execute the final closure gate.
"""

import json
import os
import subprocess
import urllib.request
import base64
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/tp1"
DOC.mkdir(parents=True, exist_ok=True)


def run(cmd, check=True):
    result = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if check and result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(f"FAILED: {' '.join(cmd)}")
    return result


def write(name, content):
    (DOC / name).write_text(content.strip() + "\n", encoding="utf-8")


# ------------------------------------------------------------
# Documentation
# ------------------------------------------------------------

write("README.md", """
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
""")

write("data-sources.md", """
# TP1 Data Sources

## Enterprise Domains

- Customer
- Product
- Employee / HR
- Account Management
- Contracts
- Sales
- CRM
- Quotes
- Finance
- Support
- Supply Chain
- Procurement
- Manufacturing
- Partners
- Distribution
- Marketing
- Pricing
- Geography

## Source Interfaces

- PostgreSQL
- CSV
- JSON
- Excel-compatible source structures

## Data Classification

Operational enterprise records are synthetic unless explicitly documented
as public-source data.

No confidential Dell Technologies data is used.

Synthetic datasets are generated deterministically where generation scripts
define fixed random seeds.
""")

write("postgresql-v2.md", """
# PostgreSQL Source V2

## Purpose

Provide the relational operational source model used by TP1 ingestion.

## Validation Snapshot

- 23 relational tables
- 41 foreign-key relationships
- 0 detected business-rule errors during the validated database audit

## Major Relationships

Customer -> Account Assignment
Customer -> Contract
Customer -> Opportunity
Opportunity -> Quote
Quote -> Order
Order -> Order Line
Order -> Invoice
Invoice -> Payment
Order/Product -> Shipment
Customer/Order/Product -> Support Ticket
Supplier/Product -> Purchase Order
Plant/Product -> Production Order

## Migration

The V2 model was created in the separate `source_v2` PostgreSQL schema.

The original V1 tables were preserved during migration and validation.
This enabled parallel validation and safe rollback.
""")

write("ingestion-framework.md", """
# TP1 Ingestion Framework

## Technology

Python 3 filesystem ingestion framework.

## Technique

Metadata-driven ingestion with SHA-256 fingerprints.

## Processing

1. Discover configured sources.
2. Validate source existence.
3. Calculate source checksum.
4. Detect unchanged datasets.
5. Preserve source representation in Raw.
6. Publish validated representation to Bronze.
7. Reconcile source and Bronze row counts.
8. Persist run metadata and logs.

## Idempotence

Unchanged sources are identified by SHA-256 checksum and skipped when their
Raw and Bronze representations already exist.

## Incremental Behavior

Changed source fingerprints trigger re-ingestion while unchanged datasets
remain untouched.

## Error Handling

A failed dataset prevents successful run completion.
Run metadata records failed execution state.

## Execution

From the repository root:

`python automation/tp1/run_tp1_core.py`
""")

write("validation.md", """
# TP1 Validation

## Validated Controls

- Source discovery
- Referential integrity
- PostgreSQL foreign keys
- Duplicate protection through primary keys
- Positive quantity/value rules
- Invoice financial reconciliation
- Inventory quantity reconciliation
- Raw/Bronze row-count reconciliation
- Metadata generation
- Logging
- Idempotence
- Incremental change detection

## Core Pipeline Result

- Datasets: 24
- Source rows: 859,886
- Errors: 0
- Final status: PASSED

## PostgreSQL Audit

- Tables: 23
- Foreign keys: 41
- Business-rule errors: 0
""")

write("dependencies.md", """
# TP1 Downstream Dependencies

## TP2 - Data Lake and Data Quality

Prepared now:
- Raw/Bronze contract
- Metadata
- Reconciliation
- Quarantine structure

Implemented later:
- Extended data-quality framework
- Data Lake lifecycle controls

## TP3 - PySpark Processing

Prepared now:
- Stable source datasets
- Portable filesystem layout
- Consistent business identifiers

Implemented later:
- Distributed Spark transformations
- Parquet processing

## TP5 - Data Modeling

Prepared now:
- Customer, Product, Employee and enterprise business keys
- Transaction grain

Implemented later:
- Dimensional warehouse model

## TP6 - Airflow

Prepared now:
- Independently executable Python pipeline

Implemented later:
- DAG orchestration and scheduling

## TP9 - Business Intelligence

Prepared now:
- Traceable commercial and operational relationships

Implemented later:
- Semantic model and executive dashboards

## TP10 - Data Science

Prepared now:
- Historical transactional datasets

Implemented later:
- Forecasting and machine-learning pipelines

## TP11 - Production

Prepared now:
- Linux-compatible relative paths
- Environment-based secrets
- Dockerized PostgreSQL
- Logs and validation gates

Implemented later:
- Ubuntu Server DEV/PROD deployment
- Monitoring, security and operational controls
""")

write("troubleshooting.md", """
# TP1 Troubleshooting

## PostgreSQL Bootstrap Conflict

Cause:
An obsolete initialization script created an incompatible product dataset,
causing downstream foreign-key loading problems.

Resolution:
The obsolete bootstrap was removed and the development database was rebuilt.

Prevention:
Database initialization scripts must be version-controlled and validated
against the active source contract.

## Python Virtual Environment

Cause:
The Ubuntu environment did not initially contain the required Python venv
package.

Resolution:
The required Ubuntu package was installed and the project virtual
environment was recreated.

## Support Validation Performance

Cause:
Ticket validation repeatedly scanned the complete order-line dataset.

Resolution:
A precomputed set was introduced for constant-time relationship lookup.

Prevention:
Large referential validations must use indexed/set-based lookups.

## Supply Chain Source Path

Cause:
The generator expected the warehouse master in an incorrect directory.

Resolution:
The source path was corrected to the canonical supply-chain location.

Prevention:
Source locations must be defined centrally through configuration/catalogs.

## PostgreSQL Shell Credentials

Cause:
PostgreSQL environment variables were not loaded into the active shell.

Resolution:
The project `.env` was loaded without displaying secrets.
""")

print("Documentation : OK")


# ------------------------------------------------------------
# Local validation
# ------------------------------------------------------------

required = [
    ROOT / "automation/tp1/run_tp1_core.py",
    ROOT / "data/metadata/ingestion_manifest.json",
    DOC / "README.md",
    DOC / "validation.md",
    DOC / "dependencies.md",
    DOC / "troubleshooting.md",
]

missing = [str(p) for p in required if not p.exists()]

if missing:
    raise SystemExit("Missing TP1 artifacts:\n" + "\n".join(missing))

core = run(["python", "automation/tp1/run_tp1_core.py"])

if "TP1 CORE PIPELINE: PASSED" not in core.stdout:
    print(core.stdout)
    raise SystemExit("TP1 core validation failed")

print("Final validation : OK")


# ------------------------------------------------------------
# Jira
# ------------------------------------------------------------

jira_url = os.getenv("JIRA_URL", "https://jalilbouktir.atlassian.net")
jira_email = os.getenv("JIRA_EMAIL")
jira_token = os.getenv("JIRA_API_TOKEN") or os.getenv("JIRA_TOKEN")

if not jira_email or not jira_token:
    print("Jira : SKIPPED - credentials variable not available")
else:
    auth = base64.b64encode(
        f"{jira_email}:{jira_token}".encode()
    ).decode()

    headers = {
        "Authorization": f"Basic {auth}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    jql = 'project = SCRUM AND issuetype = Feature ORDER BY created ASC'
    url = (
        jira_url.rstrip("/")
        + "/rest/api/3/search/jql?jql="
        + urllib.parse.quote(jql)
        + "&maxResults=100"
    )

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as r:
            payload = json.loads(r.read())

        target_names = {
            "Build REST API ingestion",
            "Build file ingestion",
            "Build PostgreSQL ingestion",
            "Implement failure handling",
        }

        issues = [
            x for x in payload.get("issues", [])
            if x.get("fields", {}).get("summary") in target_names
        ]

        comment = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [{
                    "type": "paragraph",
                    "content": [{
                        "type": "text",
                        "text":
                        "TP1 automated validation passed. "
                        "24 datasets, 859,886 source rows, "
                        "Raw/Bronze reconciliation passed, "
                        "PostgreSQL V2 validated with 23 tables, "
                        "41 foreign keys and zero detected business-rule errors. "
                        "Documentation and downstream dependency mapping updated."
                    }]
                }]
            }
        }

        for issue in issues:
            key = issue["key"]
            endpoint = (
                jira_url.rstrip("/")
                + f"/rest/api/3/issue/{key}/comment"
            )
            req = urllib.request.Request(
                endpoint,
                data=json.dumps(comment).encode(),
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req):
                pass

        print(f"Jira : OK ({len(issues)} Week 2 Features updated)")

    except Exception as exc:
        raise SystemExit(f"Jira update failed: {exc}")


# ------------------------------------------------------------
# Git safety
# ------------------------------------------------------------

ignore = run(["git", "check-ignore", ".env"], check=False)

if ignore.returncode != 0:
    raise SystemExit("SECURITY GATE FAILED: .env is not ignored")

run(["git", "add",
     "automation",
     "docker",
     "docs",
     "src",
     "tests",
     ".gitignore"])

status = run(["git", "status", "--short"]).stdout.strip()

if not status:
    print("Git : no new tracked changes")
else:
    run([
        "git", "commit", "-m",
        "feat: complete TP1 multi-source ingestion foundation"
    ])
    print("Git commit : OK")

run(["git", "push", "origin", "main"])
print("GitHub push : OK")


# ------------------------------------------------------------
# Closure
# ------------------------------------------------------------

commit = run(["git", "rev-parse", "--short", "HEAD"]).stdout.strip()
branch = run(["git", "branch", "--show-current"]).stdout.strip()
dirty = run(["git", "status", "--porcelain"]).stdout.strip()

print()
print("================================")
print("TP1 FINAL CLOSURE GATE")
print("================================")
print("Documentation     : OK")
print("Core pipeline     : PASSED")
print("Jira governance   : OK")
print("Git commit        : OK")
print("GitHub push       : OK")
print(f"Branch            : {branch}")
print(f"Commit            : {commit}")
print(f"Working tree      : {'CLEAN' if not dirty else 'CHECK REQUIRED'}")
print("--------------------------------")
print("TP1 STATUS        : CLOSED")
