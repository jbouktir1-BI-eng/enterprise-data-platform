import csv
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(45)

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/source"
CRM = SOURCE / "crm"
FINANCE = SOURCE / "finance"
CRM.mkdir(parents=True, exist_ok=True)
FINANCE.mkdir(parents=True, exist_ok=True)

def read_csv(path):
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))

customers = read_csv(SOURCE / "master/customers.csv")
orders = read_csv(SOURCE / "sales/orders.csv")

# CRM contacts
contacts = []
for i in range(1, 15001):
    customer = random.choice(customers)
    contacts.append({
        "contact_id": f"CONT-{i:06}",
        "customer_id": customer["customer_id"],
        "contact_role": random.choice([
            "Decision Maker", "Technical", "Procurement",
            "Finance", "Executive"
        ]),
        "status": random.choice(["Active"] * 9 + ["Inactive"])
    })

# CRM opportunities
opportunities = []
for i in range(1, 20001):
    customer = random.choice(customers)
    opportunities.append({
        "opportunity_id": f"OPP-{i:06}",
        "customer_id": customer["customer_id"],
        "stage": random.choice([
            "Qualification", "Discovery", "Proposal",
            "Negotiation", "Won", "Lost"
        ]),
        "estimated_value": round(random.uniform(1000, 250000), 2),
        "probability": random.choice([10, 25, 50, 70, 90, 100])
    })

with (CRM / "contacts.json").open("w", encoding="utf-8") as f:
    json.dump(contacts, f)

with (CRM / "opportunities.json").open("w", encoding="utf-8") as f:
    json.dump(opportunities, f)

# Finance invoices
invoice_orders = random.sample(orders, 75000)

invoices = []
for i, order in enumerate(invoice_orders, 1):
    invoices.append({
        "invoice_id": f"INV-{i:07}",
        "order_id": order["order_id"],
        "customer_id": order["customer_id"],
        "invoice_amount": round(random.uniform(500, 150000), 2),
        "currency": random.choice(["USD", "EUR", "GBP"]),
        "invoice_status": random.choice(
            ["Paid"] * 7 + ["Open", "Overdue"]
        )
    })

payments = []
for i, invoice in enumerate(random.sample(invoices, 70000), 1):
    payments.append({
        "payment_id": f"PAY-{i:07}",
        "invoice_id": invoice["invoice_id"],
        "customer_id": invoice["customer_id"],
        "payment_amount": invoice["invoice_amount"],
        "payment_method": random.choice([
            "Bank Transfer", "Card", "Partner Settlement"
        ])
    })

def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

write_csv(FINANCE / "invoices.csv", invoices)
write_csv(FINANCE / "payments.csv", payments)

print(f"CRM contacts       : {len(contacts):,}")
print(f"CRM opportunities  : {len(opportunities):,}")
print(f"Finance invoices   : {len(invoices):,}")
print(f"Finance payments   : {len(payments):,}")
print("\nCRM + FINANCE DATA: OK")
