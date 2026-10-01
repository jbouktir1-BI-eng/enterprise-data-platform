import csv
import json
import random
from pathlib import Path

random.seed(42)

ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / "data" / "source" / "master"
MASTER.mkdir(parents=True, exist_ok=True)

REGIONS = {
    "EMEA": ["Morocco", "France", "Germany", "Spain", "United Kingdom"],
    "AMER": ["United States", "Canada", "Brazil", "Mexico"],
    "APJ": ["Japan", "India", "Australia", "Singapore"]
}

FAMILIES = [
    ("PowerEdge", "ISG"),
    ("PowerStore", "ISG"),
    ("PowerScale", "ISG"),
    ("Latitude", "CSG"),
    ("Precision", "CSG"),
    ("OptiPlex", "CSG"),
    ("Alienware", "CSG")
]

def write_csv(name, fields, rows):
    path = MASTER / name
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"{name:25} {len(rows):>8,}")

customers = []
for i in range(1, 10001):
    region = random.choice(list(REGIONS))
    customers.append({
        "customer_id": f"CUST-{i:06}",
        "customer_name": f"Enterprise Customer {i:06}",
        "segment": random.choice(["Enterprise", "Mid-Market", "SMB", "Public"]),
        "region": region,
        "country": random.choice(REGIONS[region]),
        "status": random.choice(["Active"] * 9 + ["Inactive"])
    })

products = []
for i in range(1, 1501):
    family, bu = random.choice(FAMILIES)
    products.append({
        "product_id": f"PROD-{i:05}",
        "product_name": f"{family} Model {i:05}",
        "product_family": family,
        "business_unit": bu,
        "list_price": round(random.uniform(500, 50000), 2),
        "lifecycle": random.choice(["Active"] * 8 + ["EOL", "Launch"])
    })

employees = []
for i in range(1, 801):
    employees.append({
        "employee_id": f"EMP-{i:05}",
        "employee_name": f"Employee {i:05}",
        "department": random.choice(
            ["Sales", "Finance", "Supply Chain", "Support",
             "Marketing", "Manufacturing", "IT"]
        ),
        "role": random.choice(
            ["Analyst", "Engineer", "Manager", "Specialist", "Director"]
        )
    })

write_csv(
    "customers.csv",
    customers[0].keys(),
    customers
)

write_csv(
    "products.csv",
    products[0].keys(),
    products
)

write_csv(
    "employees.csv",
    employees[0].keys(),
    employees
)

geography = [
    {"region": region, "country": country}
    for region, countries in REGIONS.items()
    for country in countries
]

with (MASTER / "geography.json").open("w", encoding="utf-8") as f:
    json.dump(geography, f, indent=2)

print(f"{'geography.json':25} {len(geography):>8,}")
print("\nMASTER DATA: OK")
