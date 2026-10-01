import csv
import random
from pathlib import Path

random.seed(43)

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "data" / "source"

def write_csv(folder, filename, fields, rows):
    path = BASE / folder
    path.mkdir(parents=True, exist_ok=True)

    with (path / filename).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"{folder}/{filename:30} {len(rows):>8,}")

# Suppliers
suppliers = [{
    "supplier_id": f"SUP-{i:04}",
    "supplier_name": f"Supplier {i:04}",
    "supplier_type": random.choice(
        ["Components", "Semiconductors", "Logistics", "Services"]
    ),
    "country": random.choice(
        ["United States", "China", "Taiwan", "Germany", "Japan", "India"]
    ),
    "status": random.choice(["Active"] * 9 + ["Inactive"])
} for i in range(1, 301)]

# Partners / Alliances / Resellers
partners = [{
    "partner_id": f"PAR-{i:05}",
    "partner_name": f"Partner {i:05}",
    "partner_type": random.choice(
        ["Distributor", "Reseller", "Alliance", "Integrator", "Cloud Partner"]
    ),
    "tier": random.choice(["Authorized", "Gold", "Platinum"]),
    "region": random.choice(["EMEA", "AMER", "APJ"]),
    "status": random.choice(["Active"] * 9 + ["Inactive"])
} for i in range(1, 501)]

# Manufacturing plants
plants = [{
    "plant_id": f"PLANT-{i:03}",
    "plant_name": f"Manufacturing Plant {i:03}",
    "country": random.choice(
        ["United States", "Mexico", "Brazil", "China", "India", "Poland"]
    ),
    "capacity_class": random.choice(["Medium", "Large", "Strategic"])
} for i in range(1, 13)]

# Distribution warehouses
warehouses = [{
    "warehouse_id": f"WH-{i:03}",
    "warehouse_name": f"Distribution Center {i:03}",
    "region": random.choice(["EMEA", "AMER", "APJ"]),
    "warehouse_type": random.choice(
        ["Regional", "Central", "Partner"]
    )
} for i in range(1, 31)]

write_csv(
    "procurement", "suppliers.csv",
    suppliers[0].keys(), suppliers
)

write_csv(
    "partners", "partners.csv",
    partners[0].keys(), partners
)

write_csv(
    "manufacturing", "plants.csv",
    plants[0].keys(), plants
)

write_csv(
    "supply_chain", "warehouses.csv",
    warehouses[0].keys(), warehouses
)

print("\nEXTERNAL MASTER DATA: OK")
