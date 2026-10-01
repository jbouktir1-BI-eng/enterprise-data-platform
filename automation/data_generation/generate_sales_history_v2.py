"""
Component   : Sales History v2 Generator
Technology  : Python 3
Techniques  : Rule-Based Historical Transaction Generation,
              Referential Integrity, Commercial Eligibility
Used in     : TP1 - Multi-Source Ingestion

Purpose:
Generate synthetic sales history from 2019-01-01 through 2026-12-31.

Business Rules:
- Customer must be valid and active.
- Account owner must match the customer's commercial assignment.
- Products must be eligible for the customer's segment.
- Non-consumer orders use a valid customer contract when one exists.
- Order dates and contract usage must be temporally coherent.
- Every order contains exactly three order lines.

Data Classification:
SYNTHETIC
"""

import csv
import random
from collections import defaultdict, Counter
from datetime import date, timedelta
from pathlib import Path

random.seed(55)

ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / "data/source/master"
CONTRACT_DIR = ROOT / "data/source/contracts"
OUT = ROOT / "data/source/sales_v2"
OUT.mkdir(parents=True, exist_ok=True)

START_DATE = date(2019, 1, 1)
END_DATE = date(2026, 12, 31)
ORDER_COUNT = 80_000
LINES_PER_ORDER = 3


def read_csv(path):
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


customers = read_csv(MASTER / "customers_v2.csv")
assignments = read_csv(MASTER / "account_assignments_v2.csv")
products = read_csv(MASTER / "products_v2.csv")
eligibility = read_csv(MASTER / "customer_product_eligibility.csv")
contracts = read_csv(CONTRACT_DIR / "contracts.csv")

customer_map = {r["customer_id"]: r for r in customers}
assignment_map = {r["customer_id"]: r for r in assignments}
product_map = {r["product_id"]: r for r in products}

# TECHNIQUE: Precomputed eligibility pools.
# Avoid repeated full-table scans during transaction generation.
eligible_products = defaultdict(list)

for rule in eligibility:
    if rule["eligible"] == "Yes":
        eligible_products[rule["customer_segment"]].append(rule["product_id"])

contracts_by_customer = defaultdict(list)

for contract in contracts:
    contracts_by_customer[contract["customer_id"]].append(contract)

active_customers = [
    c for c in customers
    if c["customer_status"] == "Active"
    and c["customer_id"] in assignment_map
    and eligible_products[c["customer_segment"]]
]

# Later years receive moderately more transactions to create a realistic
# historical growth pattern without using future forecast data.
YEAR_WEIGHTS = {
    2019: 8,
    2020: 9,
    2021: 10,
    2022: 11,
    2023: 12,
    2024: 14,
    2025: 17,
    2026: 19,
}

years = list(YEAR_WEIGHTS)
year_weights = list(YEAR_WEIGHTS.values())

orders = []
order_lines = []

for order_number in range(1, ORDER_COUNT + 1):

    customer = random.choice(active_customers)
    customer_id = customer["customer_id"]
    segment = customer["customer_segment"]

    owner = assignment_map[customer_id]

    year = random.choices(
        years,
        weights=year_weights,
        k=1
    )[0]

    year_start = date(year, 1, 1)
    year_end = date(year, 12, 31)

    order_date = year_start + timedelta(
        days=random.randint(0, (year_end - year_start).days)
    )

    # TECHNIQUE: Temporal contract matching.
    # Use only contracts active on the order date.
    valid_contracts = []

    for contract in contracts_by_customer.get(customer_id, []):
        contract_start = date.fromisoformat(contract["start_date"])
        contract_end = date.fromisoformat(contract["end_date"])

        if contract_start <= order_date <= contract_end:
            valid_contracts.append(contract)

    contract_id = (
        random.choice(valid_contracts)["contract_id"]
        if valid_contracts
        else ""
    )

    order_id = f"ORD-{order_number:08}"

    orders.append({
        "order_id": order_id,
        "customer_id": customer_id,
        "employee_id": owner["account_owner_employee_id"],
        "contract_id": contract_id,
        "order_date": order_date.isoformat(),
        "customer_segment": segment,
        "sales_organization": owner["sales_organization"],
        "region": customer["region"],
        "currency": customer["preferred_currency"],
        "status": random.choices(
            ["Completed", "Shipped", "Cancelled"],
            weights=[82, 16, 2],
            k=1
        )[0],
        "data_classification": "SYNTHETIC"
    })

    product_pool = eligible_products[segment]

    selected_products = random.sample(
        product_pool,
        k=min(LINES_PER_ORDER, len(product_pool))
    )

    for line_number, product_id in enumerate(selected_products, 1):

        product = product_map[product_id]

        # Synthetic commercial pricing for the transaction layer.
        # Product Master remains independent from transactional price history.
        unit_price = round(
            random.uniform(100, 25_000),
            2
        )

        quantity = random.randint(1, 10)

        discount_pct = random.choice([
            0, 0, 0, 5, 5, 10, 10, 15, 20
        ])

        gross_amount = round(unit_price * quantity, 2)

        net_amount = round(
            gross_amount * (1 - discount_pct / 100),
            2
        )

        order_lines.append({
            "order_id": order_id,
            "line_number": line_number,
            "product_id": product_id,
            "portfolio": product["portfolio"],
            "workload": product["workload"],
            "quantity": quantity,
            "unit_price": unit_price,
            "discount_pct": discount_pct,
            "gross_amount": gross_amount,
            "net_amount": net_amount,
            "data_classification": "SYNTHETIC"
        })


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


write_csv(OUT / "orders_v2.csv", orders)
write_csv(OUT / "order_lines_v2.csv", order_lines)


# ---------------- VALIDATION ----------------

errors = 0

if len(orders) != ORDER_COUNT:
    errors += 1

if len(order_lines) != ORDER_COUNT * LINES_PER_ORDER:
    errors += 1

for order in orders:
    if order["customer_id"] not in customer_map:
        errors += 1

    assignment = assignment_map.get(order["customer_id"])

    if not assignment:
        errors += 1
        continue

    if order["employee_id"] != assignment["account_owner_employee_id"]:
        errors += 1

    if order["sales_organization"] != assignment["sales_organization"]:
        errors += 1

order_map = {r["order_id"]: r for r in orders}

for line in order_lines:
    order = order_map.get(line["order_id"])

    if not order:
        errors += 1
        continue

    if line["product_id"] not in eligible_products[order["customer_segment"]]:
        errors += 1


year_counts = Counter(
    date.fromisoformat(r["order_date"]).year
    for r in orders
)

print(f"Orders              : {len(orders):,}")
print(f"Order lines         : {len(order_lines):,}")
print(f"Active customers    : {len(active_customers):,}")
print(f"Validation errors   : {errors:,}")

print("\n=== ORDERS BY YEAR ===")
for year in range(2019, 2027):
    print(f"{year}: {year_counts[year]:>6,}")

print(
    "\nSALES HISTORY V2:",
    "OK" if errors == 0 else "FAILED"
)
