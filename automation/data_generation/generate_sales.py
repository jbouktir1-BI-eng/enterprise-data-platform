import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(44)

ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / "data/source/master"
OUT = ROOT / "data/source/sales"
OUT.mkdir(parents=True, exist_ok=True)

def ids(filename, key):
    with (MASTER / filename).open(encoding="utf-8") as f:
        return [row[key] for row in csv.DictReader(f)]

customers = ids("customers.csv", "customer_id")
products = ids("products.csv", "product_id")
employees = ids("employees.csv", "employee_id")

start = datetime(2024, 1, 1)

orders = []
order_lines = []

for i in range(1, 80001):
    order_id = f"ORD-{i:07}"
    customer_id = random.choice(customers)
    employee_id = random.choice(employees)
    order_date = start + timedelta(days=random.randint(0, 1000))

    orders.append({
        "order_id": order_id,
        "customer_id": customer_id,
        "employee_id": employee_id,
        "order_date": order_date.date().isoformat(),
        "status": random.choice(
            ["Completed"] * 7 + ["Pending", "Shipped", "Cancelled"]
        )
    })

    # 3 lines/order = 240,000 lines
    for line_number in range(1, 4):
        order_lines.append({
            "order_id": order_id,
            "line_number": line_number,
            "product_id": random.choice(products),
            "quantity": random.randint(1, 20),
            "discount_pct": random.choice([0, 0, 0, 5, 10, 15, 20])
        })

def write(name, rows):
    with (OUT / name).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"{name:20} {len(rows):>10,}")

write("orders.csv", orders)
write("order_lines.csv", order_lines)

print("\nSALES DATA: OK")
