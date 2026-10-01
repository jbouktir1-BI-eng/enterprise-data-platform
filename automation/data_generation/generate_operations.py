import csv
import random
from pathlib import Path

random.seed(46)

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/source"

def read_csv(path):
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(folder, filename, rows):
    out = SOURCE / folder
    out.mkdir(parents=True, exist_ok=True)
    with (out / filename).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print(f"{folder}/{filename:28} {len(rows):>8,}")

products = read_csv(SOURCE / "master/products.csv")
suppliers = read_csv(SOURCE / "procurement/suppliers.csv")
partners = read_csv(SOURCE / "partners/partners.csv")
plants = read_csv(SOURCE / "manufacturing/plants.csv")
warehouses = read_csv(SOURCE / "supply_chain/warehouses.csv")
orders = read_csv(SOURCE / "sales/orders.csv")

purchase_orders = [{
    "purchase_order_id": f"PO-{i:07}",
    "supplier_id": random.choice(suppliers)["supplier_id"],
    "product_id": random.choice(products)["product_id"],
    "quantity": random.randint(10, 1000),
    "unit_cost": round(random.uniform(100, 10000), 2)
} for i in range(1, 25001)]

production_orders = [{
    "production_order_id": f"MFG-{i:07}",
    "plant_id": random.choice(plants)["plant_id"],
    "product_id": random.choice(products)["product_id"],
    "quantity": random.randint(10, 500),
    "status": random.choice(["Completed", "Running", "Planned"])
} for i in range(1, 30001)]

inventory = [{
    "inventory_id": f"STK-{i:07}",
    "warehouse_id": random.choice(warehouses)["warehouse_id"],
    "product_id": random.choice(products)["product_id"],
    "quantity_on_hand": random.randint(0, 5000)
} for i in range(1, 45001)]

shipment_orders = random.sample(orders, 65000)
shipments = [{
    "shipment_id": f"SHP-{i:07}",
    "order_id": order["order_id"],
    "warehouse_id": random.choice(warehouses)["warehouse_id"],
    "status": random.choice(["Delivered", "In Transit", "Preparing"])
} for i, order in enumerate(shipment_orders, 1)]

distribution = [{
    "distribution_id": f"DIST-{i:07}",
    "partner_id": random.choice(partners)["partner_id"],
    "product_id": random.choice(products)["product_id"],
    "quantity": random.randint(1, 200),
    "channel": random.choice(["Distributor", "Reseller", "Integrator"])
} for i in range(1, 40001)]

write_csv("procurement", "purchase_orders.csv", purchase_orders)
write_csv("manufacturing", "production_orders.csv", production_orders)
write_csv("supply_chain", "inventory.csv", inventory)
write_csv("supply_chain", "shipments.csv", shipments)
write_csv("distribution", "sell_out.csv", distribution)

print("\nOPERATIONS DATA: OK")
