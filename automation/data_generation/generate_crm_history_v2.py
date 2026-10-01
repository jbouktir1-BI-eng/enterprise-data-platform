"""
Component   : CRM History v2 Generator
Technology  : Python 3
Techniques  : Historical CRM Generation, Business Rule Enforcement
Used in     : TP1 - Multi-Source Ingestion

Purpose:
Generate CRM opportunities for 2019-2026 consistent with customer
segmentation, account ownership and product eligibility.

Data Classification:
SYNTHETIC
"""

import csv
import json
import random
from datetime import date, timedelta
from pathlib import Path
from collections import defaultdict, Counter

random.seed(56)

ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / "data/source/master"
OUT = ROOT / "data/source/crm_v2"
OUT.mkdir(parents=True, exist_ok=True)

OPPORTUNITY_COUNT = 20_000

def read_csv(path):
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))

customers = read_csv(MASTER / "customers_v2.csv")
assignments = read_csv(MASTER / "account_assignments_v2.csv")
products = read_csv(MASTER / "products_v2.csv")
eligibility = read_csv(MASTER / "customer_product_eligibility.csv")

customer_map = {r["customer_id"]: r for r in customers}
assignment_map = {r["customer_id"]: r for r in assignments}
product_map = {r["product_id"]: r for r in products}

eligible_products = defaultdict(list)

for rule in eligibility:
    if rule["eligible"] == "Yes":
        eligible_products[rule["customer_segment"]].append(rule["product_id"])

active_customers = [
    c for c in customers
    if c["customer_status"] == "Active"
    and c["customer_id"] in assignment_map
]

YEAR_WEIGHTS = {
    2019: 8, 2020: 9, 2021: 10, 2022: 11,
    2023: 12, 2024: 14, 2025: 17, 2026: 19
}

opportunities = []

for i in range(1, OPPORTUNITY_COUNT + 1):
    customer = random.choice(active_customers)
    segment = customer["customer_segment"]
    owner = assignment_map[customer["customer_id"]]

    year = random.choices(
        list(YEAR_WEIGHTS),
        weights=list(YEAR_WEIGHTS.values()),
        k=1
    )[0]

    created = date(year, 1, 1) + timedelta(
        days=random.randint(
            0,
            (date(year, 12, 31) - date(year, 1, 1)).days
        )
    )

    product_id = random.choice(eligible_products[segment])
    product = product_map[product_id]

    stage = random.choices(
        ["Qualified", "Proposal", "Negotiation", "Closed Won", "Closed Lost"],
        weights=[15, 15, 15, 40, 15],
        k=1
    )[0]

    amount = round(random.uniform(5_000, 1_000_000), 2)

    opportunities.append({
        "opportunity_id": f"OPP-{i:07}",
        "customer_id": customer["customer_id"],
        "owner_employee_id": owner["account_owner_employee_id"],
        "product_id": product_id,
        "customer_segment": segment,
        "portfolio": product["portfolio"],
        "workload": product["workload"],
        "created_date": created.isoformat(),
        "stage": stage,
        "estimated_value": amount,
        "currency": customer["preferred_currency"],
        "region": customer["region"],
        "sales_organization": owner["sales_organization"],
        "data_classification": "SYNTHETIC"
    })

output = OUT / "opportunities_v2.json"

with output.open("w", encoding="utf-8") as f:
    json.dump(opportunities, f, indent=2)

# Validation
errors = 0

for opp in opportunities:
    customer = customer_map[opp["customer_id"]]
    assignment = assignment_map[opp["customer_id"]]

    if opp["owner_employee_id"] != assignment["account_owner_employee_id"]:
        errors += 1

    if opp["product_id"] not in eligible_products[customer["customer_segment"]]:
        errors += 1

year_counts = Counter(
    date.fromisoformat(o["created_date"]).year
    for o in opportunities
)

print(f"Opportunities       : {len(opportunities):,}")
print(f"Validation errors   : {errors:,}")

print("\n=== OPPORTUNITIES BY YEAR ===")
for year in range(2019, 2027):
    print(f"{year}: {year_counts[year]:>6,}")

print(
    "\nCRM HISTORY V2:",
    "OK" if errors == 0 else "FAILED"
)
