"""
Component   : Commercial Master Generator
Technology  : Python 3
Techniques  : Territory Management, Account Assignment,
              Contract Management, Payment Policy Rules
Used in     : TP1 - Multi-Source Ingestion

Purpose:
Create consistent commercial ownership and contractual conditions for
each customer.

Business Controls:
- Customer segment determines sales organization.
- Strategic/Key Accounts receive named account management.
- Contract and payment terms depend on customer segment.
- Consumer accounts cannot be assigned to enterprise/public sales teams.
- Contract identifiers are traceable to customer identifiers.

Data Classification:
SYNTHETIC - No real customer, employee or contract data is used.
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(52)

ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / "data/source/master"
CONTRACTS = ROOT / "data/source/contracts"
CONTRACTS.mkdir(parents=True, exist_ok=True)

with (MASTER / "customers_v2.csv").open(encoding="utf-8") as f:
    customers = list(csv.DictReader(f))

# Sales organization policy.
SALES_RULES = {
    "Consumer": "Consumer Sales",
    "SMB": "SMB Sales",
    "Mid-Market": "Commercial Sales",
    "Enterprise": "Enterprise Sales",
    "Public Sector": "Public Sector Sales",
    "Federal/Government": "Federal Sales",
    "Education": "Education Sales",
    "Healthcare": "Healthcare Sales",
}

account_assignments = []
contracts = []

for i, customer in enumerate(customers, 1):
    segment = customer["customer_segment"]
    sales_org = SALES_RULES[segment]

    # TECHNIQUE: Account ownership.
    # Named strategic accounts receive dedicated account managers.
    account_model = (
        "Named Account"
        if customer["commercial_value_tier"] in ("Key Account", "Strategic")
        else "Territory Account"
    )

    account_assignments.append({
        "assignment_id": f"ASSIGN-{i:06}",
        "customer_id": customer["customer_id"],
        "customer_segment": segment,
        "sales_organization": sales_org,
        "account_model": account_model,
        "territory": f"{customer['region']}-{sales_org.replace(' ', '-').upper()}",
        "data_classification": "SYNTHETIC"
    })

    # Consumer transactions normally do not require enterprise contracts.
    if segment == "Consumer":
        continue

    start = date(2019, 1, 1) + timedelta(days=random.randint(0, 2555))

    if segment in ("Enterprise", "Public Sector",
                   "Federal/Government", "Education", "Healthcare"):
        duration_months = random.choice([12, 24, 36, 60])
    else:
        duration_months = random.choice([12, 24, 36])

    end = start + timedelta(days=duration_months * 30)

    contracts.append({
        "contract_id": f"CTR-{len(contracts)+1:07}",
        "customer_id": customer["customer_id"],
        "contract_type": random.choice([
            "Master Agreement",
            "Purchase Agreement",
            "Subscription Agreement",
            "Support Agreement",
            "Consumption Agreement"
        ]),
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "duration_months": duration_months,
        "payment_terms": customer["default_payment_terms"],
        "currency": customer["preferred_currency"],
        "credit_limit": customer["credit_limit"],
        "support_level": random.choice([
            "Standard", "Business", "Premium", "Mission Critical"
        ]),
        "renewal_model": random.choice([
            "Manual", "Auto-Renew", "Renegotiation"
        ]),
        "contract_status": (
            "Active" if end >= date(2026, 10, 1) else "Expired"
        ),
        "data_classification": "SYNTHETIC"
    })

def write(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

write(MASTER / "account_assignments.csv", account_assignments)
write(CONTRACTS / "contracts.csv", contracts)

# Validate sales ownership.
errors = sum(
    row["sales_organization"] != SALES_RULES[row["customer_segment"]]
    for row in account_assignments
)

print(f"Account assignments : {len(account_assignments):,}")
print(f"Contracts           : {len(contracts):,}")
print(f"Ownership errors    : {errors:,}")
print(
    "COMMERCIAL MASTER:",
    "OK" if errors == 0 else "FAILED"
)
