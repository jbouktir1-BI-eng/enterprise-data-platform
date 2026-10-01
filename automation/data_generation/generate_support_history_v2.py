"""
Component   : Support History v2
Technology  : Python 3
Technique   : Installed-Base Driven Support Generation, SLA Rules
Used in     : TP1 - Multi-Source Ingestion

Purpose:
Generate support tickets against products actually purchased by customers.

Lineage:
Customer -> Order -> Product -> Support Ticket

Data Classification:
SYNTHETIC
"""

import csv
import json
import random
from collections import defaultdict, Counter
from datetime import date, timedelta
from pathlib import Path

random.seed(59)

ROOT = Path(__file__).resolve().parents[2]
SALES = ROOT / "data/source/sales_v2"
OUT = ROOT / "data/source/support_v2"
OUT.mkdir(parents=True, exist_ok=True)

TICKET_COUNT = 40_000


def read_csv(path):
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


orders = read_csv(SALES / "orders_linked_v2.csv")
lines = read_csv(SALES / "order_lines_v2.csv")

order_map = {r["order_id"]: r for r in orders}

# TECHNIQUE: Installed base.
# Support cases can only reference products previously purchased
# by the same customer.
installed_base = defaultdict(list)

for line in lines:
    order = order_map[line["order_id"]]

    if order["status"] == "Cancelled":
        continue

    installed_base[order["customer_id"]].append({
        "order_id": order["order_id"],
        "product_id": line["product_id"],
        "order_date": order["order_date"]
    })

eligible_customers = [
    customer_id
    for customer_id, assets in installed_base.items()
    if assets
]

tickets = []

for i in range(1, TICKET_COUNT + 1):

    customer_id = random.choice(eligible_customers)
    asset = random.choice(installed_base[customer_id])

    purchase_date = date.fromisoformat(asset["order_date"])

    # Ticket must occur after the related purchase.
    max_days = max(
        0,
        (date(2026, 12, 31) - purchase_date).days
    )

    ticket_date = purchase_date + timedelta(
        days=random.randint(0, max_days)
    )

    severity = random.choices(
        ["P1", "P2", "P3", "P4"],
        weights=[5, 15, 35, 45],
        k=1
    )[0]

    sla_hours = {
        "P1": 4,
        "P2": 8,
        "P3": 24,
        "P4": 48
    }[severity]

    resolution_hours = round(
        random.uniform(
            1,
            sla_hours * random.choice([0.8, 1.0, 1.5, 2.0])
        ),
        2
    )

    sla_met = resolution_hours <= sla_hours

    tickets.append({
        "ticket_id": f"TKT-{i:08}",
        "customer_id": customer_id,
        "order_id": asset["order_id"],
        "product_id": asset["product_id"],
        "ticket_date": ticket_date.isoformat(),
        "severity": severity,
        "sla_target_hours": sla_hours,
        "resolution_hours": resolution_hours,
        "sla_met": "Yes" if sla_met else "No",
        "status": random.choice(["Resolved"] * 9 + ["Open"]),
        "data_classification": "SYNTHETIC"
    })


output = OUT / "tickets_v2.json"

with output.open("w", encoding="utf-8") as f:
    json.dump(tickets, f, indent=2)


# ---------------- VALIDATION ----------------

errors = 0

# TECHNIQUE: Hash-set validation index.
# Build the order/product relationship once instead of scanning
# all order lines for every support ticket.
valid_order_products = {
    (line["order_id"], line["product_id"])
    for line in lines
}

for ticket in tickets:

    order = order_map.get(ticket["order_id"])

    if not order:
        errors += 1
        continue

    if order["customer_id"] != ticket["customer_id"]:
        errors += 1

    if (ticket["order_id"], ticket["product_id"]) not in valid_order_products:
        errors += 1

    if date.fromisoformat(ticket["ticket_date"]) < \
       date.fromisoformat(order["order_date"]):
        errors += 1


severity_counts = Counter(t["severity"] for t in tickets)

sla_met_count = sum(
    t["sla_met"] == "Yes"
    for t in tickets
)

print(f"Tickets             : {len(tickets):,}")
print(f"Validation errors   : {errors:,}")

print("\n=== SEVERITY ===")
for severity in ["P1", "P2", "P3", "P4"]:
    print(f"{severity}: {severity_counts[severity]:>6,}")

print(
    f"\nSLA met             : "
    f"{sla_met_count:,}/{len(tickets):,}"
)

print(
    "SUPPORT HISTORY V2:",
    "OK" if errors == 0 else "FAILED"
)
