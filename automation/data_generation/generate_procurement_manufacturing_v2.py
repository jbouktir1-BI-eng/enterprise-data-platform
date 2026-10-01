"""
Component   : Procurement & Manufacturing History v2
Technology  : Python 3
Technique   : Referentially Consistent Operational History
Used in     : TP1 - Multi-Source Ingestion

Purpose:
Generate 2019-2026 procurement and manufacturing transactions using
valid suppliers, plants and Product Master v2 identifiers.

Data Classification:
SYNTHETIC
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(61)

ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / "data/source/master"
PROC = ROOT / "data/source/procurement_v2"
MFG = ROOT / "data/source/manufacturing_v2"

PROC.mkdir(parents=True, exist_ok=True)
MFG.mkdir(parents=True, exist_ok=True)

PO_COUNT = 25_000
PRODUCTION_COUNT = 30_000


def read_csv(path):
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


products = read_csv(MASTER / "products_v2.csv")
suppliers = read_csv(ROOT / "data/source/procurement/suppliers.csv")
plants = read_csv(ROOT / "data/source/manufacturing/plants.csv")

product_ids = [r["product_id"] for r in products]
supplier_ids = [r["supplier_id"] for r in suppliers]
plant_ids = [r["plant_id"] for r in plants]

start = date(2019, 1, 1)
end = date(2026, 12, 31)
days = (end - start).days

purchase_orders = []

for i in range(1, PO_COUNT + 1):
    po_date = start + timedelta(days=random.randint(0, days))

    purchase_orders.append({
        "purchase_order_id": f"PO-{i:08}",
        "supplier_id": random.choice(supplier_ids),
        "product_id": random.choice(product_ids),
        "purchase_order_date": po_date.isoformat(),
        "quantity": random.randint(10, 1000),
        "unit_cost": round(random.uniform(50, 15000), 2),
        "status": random.choices(
            ["Received", "Open", "Cancelled"],
            weights=[88, 9, 3],
            k=1
        )[0],
        "data_classification": "SYNTHETIC"
    })

production_orders = []

for i in range(1, PRODUCTION_COUNT + 1):
    production_date = start + timedelta(days=random.randint(0, days))

    production_orders.append({
        "production_order_id": f"MFG-{i:08}",
        "plant_id": random.choice(plant_ids),
        "product_id": random.choice(product_ids),
        "production_date": production_date.isoformat(),
        "planned_quantity": random.randint(10, 1000),
        "actual_quantity": random.randint(5, 1000),
        "status": random.choices(
            ["Completed", "In Progress", "Cancelled"],
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


write_csv(PROC / "purchase_orders_v2.csv", purchase_orders)
write_csv(MFG / "production_orders_v2.csv", production_orders)

# Fast referential validation.
product_set = set(product_ids)
supplier_set = set(supplier_ids)
plant_set = set(plant_ids)

errors = 0

for row in purchase_orders:
    if row["product_id"] not in product_set:
        errors += 1
    if row["supplier_id"] not in supplier_set:
        errors += 1

for row in production_orders:
    if row["product_id"] not in product_set:
        errors += 1
    if row["plant_id"] not in plant_set:
        errors += 1

print(f"Purchase orders     : {len(purchase_orders):,}")
print(f"Production orders   : {len(production_orders):,}")
print(f"Validation errors   : {errors:,}")

print(
    "PROCUREMENT + MANUFACTURING V2:",
    "OK" if errors == 0 else "FAILED"
)
