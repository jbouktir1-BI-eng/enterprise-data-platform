"""
Component   : Customer-Product Eligibility Engine
Technology  : Python 3
Technique   : Rule-Based Eligibility Matrix
Used in     : TP1 - Multi-Source Ingestion

Purpose:
Define which enterprise technology portfolios and workloads can be sold
to each customer segment.

Why:
Referential integrity alone does not guarantee business consistency.
A valid customer_id and product_id combination may still represent an
invalid commercial relationship.

Examples:
- Consumer customers cannot purchase HPC infrastructure.
- Federal accounts cannot be owned by Consumer Sales.
- Enterprise accounts can purchase advanced infrastructure and AI solutions.

Output:
customer_product_eligibility.csv

Downstream:
Sales generation, CRM opportunities, contracts, forecasting and validation.
"""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / "data/source/master"

SEGMENT_RULES = {
    "Consumer": {
        "portfolios": {"Client & Edge", "Cloud & Services"},
        "blocked_workloads": {
            "HPC", "AI/ML", "Database", "Data Platform",
            "Private Cloud", "Hybrid Cloud"
        }
    },

    "SMB": {
        "portfolios": {
            "Client & Edge", "Infrastructure",
            "Software", "Cloud & Services"
        },
        "blocked_workloads": {"HPC"}
    },

    "Mid-Market": {
        "portfolios": {
            "Client & Edge", "Infrastructure", "Software",
            "Cloud & Services", "AI & Data"
        },
        "blocked_workloads": {"HPC"}
    },

    "Enterprise": {
        "portfolios": {
            "Client & Edge", "Infrastructure", "Software",
            "Cloud & Services", "AI & Data"
        },
        "blocked_workloads": set()
    },

    "Public Sector": {
        "portfolios": {
            "Client & Edge", "Infrastructure", "Software",
            "Cloud & Services", "AI & Data"
        },
        "blocked_workloads": set()
    },

    "Federal/Government": {
        "portfolios": {
            "Client & Edge", "Infrastructure", "Software",
            "Cloud & Services", "AI & Data"
        },
        "blocked_workloads": set()
    },

    "Education": {
        "portfolios": {
            "Client & Edge", "Infrastructure", "Software",
            "Cloud & Services", "AI & Data"
        },
        "blocked_workloads": set()
    },

    "Healthcare": {
        "portfolios": {
            "Client & Edge", "Infrastructure", "Software",
            "Cloud & Services", "AI & Data"
        },
        "blocked_workloads": set()
    }
}

with (MASTER / "products_v2.csv").open(encoding="utf-8") as f:
    products = list(csv.DictReader(f))

rows = []

for segment, rule in SEGMENT_RULES.items():
    for product in products:

        eligible = (
            product["portfolio"] in rule["portfolios"]
            and product["workload"] not in rule["blocked_workloads"]
        )

        rows.append({
            "customer_segment": segment,
            "product_id": product["product_id"],
            "portfolio": product["portfolio"],
            "category": product["category"],
            "workload": product["workload"],
            "eligible": "Yes" if eligible else "No",
            "rule_type": "SEGMENT_PRODUCT_ELIGIBILITY"
        })

output = MASTER / "customer_product_eligibility.csv"

with output.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Eligibility rules : {len(rows):,}")

print("\n=== ELIGIBILITY SUMMARY ===")

for segment in SEGMENT_RULES:
    eligible = sum(
        r["customer_segment"] == segment and r["eligible"] == "Yes"
        for r in rows
    )

    blocked = sum(
        r["customer_segment"] == segment and r["eligible"] == "No"
        for r in rows
    )

    print(
        f"{segment:20} "
        f"eligible={eligible:>5,} "
        f"blocked={blocked:>5,}"
    )

print("\nELIGIBILITY MATRIX: OK")
