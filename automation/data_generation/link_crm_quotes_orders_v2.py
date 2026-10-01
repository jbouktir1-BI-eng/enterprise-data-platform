"""
Component   : CRM Quote Order Linker v2
Technology  : Python 3
Technique   : Opportunity-to-Quote-to-Order Lifecycle,
              Quote Versioning, Partial Fulfillment
Used in     : TP1 - Multi-Source Ingestion

Purpose:
Create commercial traceability:
Opportunity -> Quote(s) -> Order(s)

Business Rules:
- Closed Lost opportunities create no orders.
- Opportunities may have multiple quote revisions.
- Closed Won opportunities may map to one or several orders.
- Large Enterprise/Public/Federal deals are more likely to use multiple orders.
- Orders may exist outside CRM opportunities for transactional business.
- Existing Sales History v2 is preserved; linkage is added to it.

Data Classification:
SYNTHETIC
"""

import csv
import json
import random
from collections import defaultdict, Counter
from datetime import date, timedelta
from pathlib import Path

random.seed(57)

ROOT = Path(__file__).resolve().parents[2]
CRM = ROOT / "data/source/crm_v2"
SALES = ROOT / "data/source/sales_v2"
OUT = ROOT / "data/source/quotes_v2"
OUT.mkdir(parents=True, exist_ok=True)


def read_csv(path):
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


with (CRM / "opportunities_v2.json").open(encoding="utf-8") as f:
    opportunities = json.load(f)

orders = read_csv(SALES / "orders_v2.csv")
order_lines = read_csv(SALES / "order_lines_v2.csv")

orders_by_customer = defaultdict(list)

for order in orders:
    orders_by_customer[order["customer_id"]].append(order)

for customer_orders in orders_by_customer.values():
    customer_orders.sort(key=lambda x: x["order_date"])

quotes = []
quote_lines = []

# Lookup used to add CRM references to existing orders.
order_links = {}

quote_number = 1

for opp in opportunities:

    created = date.fromisoformat(opp["created_date"])
    segment = opp["customer_segment"]
    stage = opp["stage"]

    # Lost opportunities can still have quotes, but never fulfilled orders.
    if stage == "Closed Lost":
        revision_count = random.choice([1, 1, 2, 2, 3])
    elif stage == "Closed Won":
        revision_count = random.choice([1, 2, 2, 3])
    else:
        revision_count = random.choice([1, 1, 2])

    accepted_quote_id = ""

    for revision in range(1, revision_count + 1):

        quote_id = f"QTE-{quote_number:08}"
        quote_number += 1

        quote_date = created + timedelta(
            days=(revision - 1) * random.randint(5, 20)
        )

        quoted_value = round(
            float(opp["estimated_value"])
            * random.uniform(0.90, 1.10),
            2
        )

        is_final = revision == revision_count

        if stage == "Closed Won" and is_final:
            quote_status = "Accepted"
            accepted_quote_id = quote_id
        elif stage == "Closed Lost" and is_final:
            quote_status = "Rejected"
        elif is_final:
            quote_status = "Open"
        else:
            quote_status = "Superseded"

        quotes.append({
            "quote_id": quote_id,
            "opportunity_id": opp["opportunity_id"],
            "customer_id": opp["customer_id"],
            "revision_number": revision,
            "quote_date": quote_date.isoformat(),
            "quote_status": quote_status,
            "quoted_value": quoted_value,
            "currency": opp["currency"],
            "owner_employee_id": opp["owner_employee_id"],
            "data_classification": "SYNTHETIC"
        })

        quote_lines.append({
            "quote_id": quote_id,
            "line_number": 1,
            "product_id": opp["product_id"],
            "quantity": 1,
            "quoted_amount": quoted_value,
            "data_classification": "SYNTHETIC"
        })

    # Only Closed Won opportunities can generate order linkage.
    if stage != "Closed Won":
        continue

    available_orders = [
        order
        for order in orders_by_customer.get(opp["customer_id"], [])
        if order["order_id"] not in order_links
        and date.fromisoformat(order["order_date"]) >= created
    ]

    if not available_orders:
        continue

    # Large institutional projects are more likely to be fulfilled
    # through multiple purchase orders.
    if segment in (
        "Enterprise",
        "Public Sector",
        "Federal/Government",
        "Education",
        "Healthcare"
    ):
        requested_orders = random.choices(
            [1, 2, 3, 4],
            weights=[35, 30, 20, 15],
            k=1
        )[0]
    else:
        requested_orders = random.choices(
            [1, 2],
            weights=[80, 20],
            k=1
        )[0]

    selected = available_orders[:requested_orders]

    for sequence, order in enumerate(selected, 1):
        order_links[order["order_id"]] = {
            "opportunity_id": opp["opportunity_id"],
            "quote_id": accepted_quote_id,
            "project_order_sequence": sequence
        }


# Add CRM lineage to Sales Orders.
linked_orders = []

for order in orders:
    link = order_links.get(order["order_id"], {})

    row = dict(order)
    row["opportunity_id"] = link.get("opportunity_id", "")
    row["quote_id"] = link.get("quote_id", "")
    row["project_order_sequence"] = link.get(
        "project_order_sequence", ""
    )

    linked_orders.append(row)


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


write_csv(OUT / "quotes_v2.csv", quotes)
write_csv(OUT / "quote_lines_v2.csv", quote_lines)
write_csv(SALES / "orders_linked_v2.csv", linked_orders)


# ---------------- VALIDATION ----------------

errors = 0

opp_map = {
    o["opportunity_id"]: o
    for o in opportunities
}

quote_map = {
    q["quote_id"]: q
    for q in quotes
}

for order in linked_orders:

    if not order["opportunity_id"]:
        continue

    opp = opp_map.get(order["opportunity_id"])
    quote = quote_map.get(order["quote_id"])

    if not opp or not quote:
        errors += 1
        continue

    if opp["stage"] != "Closed Won":
        errors += 1

    if quote["quote_status"] != "Accepted":
        errors += 1

    if order["customer_id"] != opp["customer_id"]:
        errors += 1


linked_count = sum(
    bool(o["opportunity_id"])
    for o in linked_orders
)

transactional_count = len(linked_orders) - linked_count

orders_per_opportunity = Counter(
    o["opportunity_id"]
    for o in linked_orders
    if o["opportunity_id"]
)

multi_order_projects = sum(
    count > 1
    for count in orders_per_opportunity.values()
)

lost_with_orders = sum(
    1
    for o in linked_orders
    if o["opportunity_id"]
    and opp_map[o["opportunity_id"]]["stage"] == "Closed Lost"
)

print(f"Opportunities         : {len(opportunities):,}")
print(f"Quotes                : {len(quotes):,}")
print(f"Quote lines           : {len(quote_lines):,}")
print(f"Orders                : {len(linked_orders):,}")
print(f"CRM-linked orders     : {linked_count:,}")
print(f"Transactional orders  : {transactional_count:,}")
print(f"Multi-order projects  : {multi_order_projects:,}")
print(f"Lost opps with orders : {lost_with_orders:,}")
print(f"Validation errors     : {errors:,}")

print(
    "\nCRM -> QUOTE -> ORDER:",
    "OK" if errors == 0 and lost_with_orders == 0 else "FAILED"
)
