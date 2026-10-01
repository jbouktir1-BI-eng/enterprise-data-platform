"""
Component   : Customer Master v2 Generator
Technology  : Python 3
Technique   : Master Data Management (MDM) and rule-based data generation
Used in     : TP1 - Multi-Source Ingestion

Purpose:
Create a reproducible customer master where segmentation, industry,
commercial value, sales ownership, credit profile and purchasing
eligibility are logically related.

Data Classification:
SYNTHETIC - No real customer or personal data is used.

Downstream Consumers:
CRM, Sales, Contracts, Finance, Support, Forecasting and BI.
"""

import csv
import random
from pathlib import Path

random.seed(50)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/source/master"
OUT.mkdir(parents=True, exist_ok=True)

SEGMENTS = {
    "Consumer": {
        "weight": 28,
        "sales_org": "Consumer Sales",
        "value_tiers": ["Consumer"],
        "employee_range": (1, 5),
        "payment_terms": ["Prepaid", "Card"],
        "credit_range": (0, 5000),
        "eligible_portfolios": "Client & Edge|Support Services"
    },
    "SMB": {
        "weight": 20,
        "sales_org": "SMB Sales",
        "value_tiers": ["Standard", "Growth"],
        "employee_range": (10, 249),
        "payment_terms": ["Prepaid", "Net 15", "Net 30"],
        "credit_range": (10000, 100000),
        "eligible_portfolios": "Client & Edge|Infrastructure|Software|Cloud & Services"
    },
    "Mid-Market": {
        "weight": 17,
        "sales_org": "Commercial Sales",
        "value_tiers": ["Growth", "Key Account"],
        "employee_range": (250, 999),
        "payment_terms": ["Net 30", "Net 45"],
        "credit_range": (100000, 500000),
        "eligible_portfolios": "Client & Edge|Infrastructure|Software|Cloud & Services|AI & Data"
    },
    "Enterprise": {
        "weight": 15,
        "sales_org": "Enterprise Sales",
        "value_tiers": ["Key Account", "Strategic"],
        "employee_range": (1000, 50000),
        "payment_terms": ["Net 30", "Net 45", "Net 60"],
        "credit_range": (500000, 5000000),
        "eligible_portfolios": "Infrastructure|Client & Edge|Software|Cloud & Services|AI & Data"
    },
    "Public Sector": {
        "weight": 8,
        "sales_org": "Public Sector Sales",
        "value_tiers": ["Standard", "Key Account", "Strategic"],
        "employee_range": (100, 20000),
        "payment_terms": ["Net 30", "Net 60"],
        "credit_range": (100000, 3000000),
        "eligible_portfolios": "Infrastructure|Client & Edge|Software|Cloud & Services|AI & Data"
    },
    "Federal/Government": {
        "weight": 4,
        "sales_org": "Federal Sales",
        "value_tiers": ["Key Account", "Strategic"],
        "employee_range": (500, 50000),
        "payment_terms": ["Net 30", "Net 60"],
        "credit_range": (500000, 5000000),
        "eligible_portfolios": "Infrastructure|Client & Edge|Software|Cloud & Services|AI & Data"
    },
    "Education": {
        "weight": 4,
        "sales_org": "Education Sales",
        "value_tiers": ["Standard", "Growth", "Key Account"],
        "employee_range": (50, 15000),
        "payment_terms": ["Net 30", "Net 60"],
        "credit_range": (50000, 1500000),
        "eligible_portfolios": "Client & Edge|Infrastructure|Software|Cloud & Services|AI & Data"
    },
    "Healthcare": {
        "weight": 4,
        "sales_org": "Healthcare Sales",
        "value_tiers": ["Growth", "Key Account", "Strategic"],
        "employee_range": (50, 25000),
        "payment_terms": ["Net 30", "Net 45", "Net 60"],
        "credit_range": (100000, 3000000),
        "eligible_portfolios": "Infrastructure|Client & Edge|Software|Cloud & Services|AI & Data"
    }
}

INDUSTRIES = {
    "Consumer": ["Consumer"],
    "SMB": ["Retail", "Services", "Technology", "Manufacturing", "Construction"],
    "Mid-Market": ["Retail", "Banking", "Technology", "Manufacturing", "Telecom", "Energy"],
    "Enterprise": ["Banking", "Telecom", "Manufacturing", "Energy", "Technology", "Retail"],
    "Public Sector": ["Government", "Municipality", "Public Administration"],
    "Federal/Government": ["Federal Government", "Defense", "National Agency"],
    "Education": ["University", "School System", "Research"],
    "Healthcare": ["Hospital", "Healthcare Network", "Life Sciences"]
}

REGIONS = ["EMEA", "AMER", "APJ"]

segments = list(SEGMENTS)
weights = [SEGMENTS[s]["weight"] for s in segments]

rows = []

for i in range(1, 10001):
    segment = random.choices(segments, weights=weights, k=1)[0]
    rule = SEGMENTS[segment]

    commercial_value = random.choice(rule["value_tiers"])
    employees = random.randint(*rule["employee_range"])
    credit_limit = random.randint(*rule["credit_range"])

    rows.append({
        "customer_id": f"CUST-{i:06}",
        "customer_name": f"Synthetic Customer {i:06}",
        "customer_segment": segment,
        "industry": random.choice(INDUSTRIES[segment]),
        "commercial_value_tier": commercial_value,
        "employee_count": employees,
        "region": random.choice(REGIONS),
        "sales_organization": rule["sales_org"],
        "account_type": (
            "Named Account"
            if commercial_value in ("Key Account", "Strategic")
            else "Territory Account"
        ),
        "credit_rating": random.choice(["A", "B", "C"]),
        "credit_limit": credit_limit,
        "default_payment_terms": random.choice(rule["payment_terms"]),
        "preferred_currency": random.choice(["USD", "EUR", "GBP"]),
        "contract_required": (
            "Yes"
            if segment not in ("Consumer", "SMB")
            else random.choice(["Yes", "No"])
        ),
        "eligible_portfolios": rule["eligible_portfolios"],
        "customer_status": random.choice(["Active"] * 9 + ["Inactive"]),
        "data_classification": "SYNTHETIC",
        "source_provider": "Enterprise Data Platform Generator"
    })

path = OUT / "customers_v2.csv"

with path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Customers : {len(rows):,}")

print("\n=== SEGMENT DISTRIBUTION ===")
for segment in segments:
    count = sum(r["customer_segment"] == segment for r in rows)
    print(f"{segment:20} {count:>6,}")

print("\n=== BUSINESS RULE VALIDATION ===")

errors = 0

for r in rows:
    expected_sales_org = SEGMENTS[r["customer_segment"]]["sales_org"]

    if r["sales_organization"] != expected_sales_org:
        errors += 1

print(f"Sales ownership errors : {errors}")
print("CUSTOMER MASTER V2:", "OK" if errors == 0 else "FAILED")
