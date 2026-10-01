import csv
import json
import random
from pathlib import Path

random.seed(47)

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/source"

def read_csv(path):
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(folder, filename, rows):
    out = SOURCE / folder
    out.mkdir(parents=True, exist_ok=True)
    with (out / filename).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"{folder}/{filename:25} {len(rows):>8,}")

customers = read_csv(SOURCE / "master/customers.csv")
products = read_csv(SOURCE / "master/products.csv")
employees = read_csv(SOURCE / "master/employees.csv")
partners = read_csv(SOURCE / "partners/partners.csv")

# Support
tickets = [{
    "ticket_id": f"TKT-{i:07}",
    "customer_id": random.choice(customers)["customer_id"],
    "product_id": random.choice(products)["product_id"],
    "priority": random.choice(["Low", "Medium", "High", "Critical"]),
    "status": random.choice(["Closed", "Resolved", "Open", "Escalated"]),
    "resolution_hours": random.randint(1, 240)
} for i in range(1, 40001)]

support_dir = SOURCE / "support"
support_dir.mkdir(parents=True, exist_ok=True)

with (support_dir / "tickets.json").open("w", encoding="utf-8") as f:
    json.dump(tickets, f)

# Marketing
leads = [{
    "lead_id": f"LEAD-{i:07}",
    "customer_id": random.choice(customers)["customer_id"],
    "campaign_id": f"CMP-{random.randint(1,100):04}",
    "channel": random.choice(["Web", "Email", "Event", "Partner", "Social"]),
    "status": random.choice(["New", "Qualified", "Converted", "Lost"])
} for i in range(1, 30001)]

write_csv("marketing", "leads.csv", leads)

# Pricing
pricing = [{
    "price_id": f"PRICE-{i:06}",
    "product_id": product["product_id"],
    "partner_id": random.choice(partners)["partner_id"],
    "list_price": product["list_price"],
    "discount_pct": random.choice([0, 5, 10, 15, 20, 25])
} for i, product in enumerate(products, 1)]

write_csv("pricing", "pricing.csv", pricing)

# Forecast
forecast = []
for i in range(1, 25001):
    forecast.append({
        "forecast_id": f"FC-{i:07}",
        "product_id": random.choice(products)["product_id"],
        "employee_id": random.choice(employees)["employee_id"],
        "region": random.choice(["EMEA", "AMER", "APJ"]),
        "quarter": random.choice(["Q1", "Q2", "Q3", "Q4"]),
        "forecast_revenue": round(random.uniform(10000, 1000000), 2)
    })

write_csv("forecast", "forecast.csv", forecast)

print(f"support/tickets.json{'':13} {len(tickets):>8,}")
print("\nBUSINESS DATA: OK")
