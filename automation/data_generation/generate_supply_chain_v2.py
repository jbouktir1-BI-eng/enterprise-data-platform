"""
Component   : Supply Chain History v2
Technology  : Python 3
Technique   : Order-Driven Supply Chain Generation, Referential Integrity
Used in     : TP1 - Multi-Source Ingestion

Purpose:
Generate inventory snapshots and shipments linked to valid products,
warehouses and customer orders.

Data Classification:
SYNTHETIC
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(60)

ROOT = Path(__file__).resolve().parents[2]
SALES = ROOT / "data/source/sales_v2"
MASTER = ROOT / "data/source/master"
OUT = ROOT / "data/source/supply_chain_v2"
OUT.mkdir(parents=True, exist_ok=True)

INVENTORY_COUNT = 45_000
SHIPMENT_COUNT = 65_000


def read_csv(path):
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


orders = read_csv(SALES / "orders_linked_v2.csv")
lines = read_csv(SALES / "order_lines_v2.csv")
products = read_csv(MASTER / "products_v2.csv")
warehouses = read_csv(ROOT / "data/source/supply_chain/warehouses.csv")

order_map = {r["order_id"]: r for r in orders}
product_ids = {r["product_id"] for r in products}
warehouse_ids = [r["warehouse_id"] for r in warehouses]

valid_lines = [
    line for line in lines
    if order_map[line["order_id"]]["status"] != "Cancelled"
]

inventory = []

for i in range(1, INVENTORY_COUNT + 1):
    product_id = random.choice(tuple(product_ids))
    warehouse_id = random.choice(warehouse_ids)

    snapshot_date = date(2019, 1, 1) + timedelta(
        days=random.randint(
            0,
            (date(2026, 12, 31) - date(2019, 1, 1)).days
        )
    )

    on_hand = random.randint(0, 500)
    reserved = random.randint(0, min(on_hand, 100))

    inventory.append({
        "inventory_id": f"INVST-{i:08}",
        "snapshot_date": snapshot_date.isoformat(),
        "warehouse_id": warehouse_id,
        "product_id": product_id,
        "quantity_on_hand": on_hand,
        "quantity_reserved": reserved,
        "quantity_available": on_hand - reserved,
        "data_classification": "SYNTHETIC"
    })


shipments = []

# Use actual order lines as the shipment source.
selected_lines = random.choices(
    valid_lines,
    k=SHIPMENT_COUNT
)

for i, line in enumerate(selected_lines, 1):
    order = order_map[line["order_id"]]
    order_date = date.fromisoformat(order["order_date"])

    ship_date = order_date + timedelta(
        days=random.randint(1, 14)
    )

    shipments.append({
        "shipment_id": f"SHP-{i:08}",
        "order_id": order["order_id"],
        "customer_id": order["customer_id"],
        "product_id": line["product_id"],
        "warehouse_id": random.choice(warehouse_ids),
        "ship_date": ship_date.isoformat(),
        "quantity_shipped": int(line["quantity"]),
        "shipment_status": random.choices(
            ["Delivered", "In Transit", "Delayed"],
            weights=[90, 7, 3],
            k=1
        )[0],
        "data_classification": "SYNTHETIC"
    })


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


write_csv(OUT / "inventory_v2.csv", inventory)
write_csv(OUT / "shipments_v2.csv", shipments)


# Fast indexed validation.
valid_order_products = {
    (line["order_id"], line["product_id"])
    for line in valid_lines
}

errors = 0

for shipment in shipments:
    if (
        shipment["order_id"],
        shipment["product_id"]
    ) not in valid_order_products:
        errors += 1

    if shipment["warehouse_id"] not in warehouse_ids:
        errors += 1

for row in inventory:
    if row["product_id"] not in product_ids:
        errors += 1

    if row["warehouse_id"] not in warehouse_ids:
        errors += 1

    if (
        int(row["quantity_available"])
        != int(row["quantity_on_hand"])
        - int(row["quantity_reserved"])
    ):
        errors += 1

print(f"Inventory snapshots : {len(inventory):,}")
print(f"Shipments           : {len(shipments):,}")
print(f"Validation errors   : {errors:,}")

print(
    "SUPPLY CHAIN V2:",
    "OK" if errors == 0 else "FAILED"
)
