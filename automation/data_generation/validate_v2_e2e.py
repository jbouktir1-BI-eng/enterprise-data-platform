"""
Technology : Python 3
Technique  : Set-Based End-to-End Referential Integrity Validation
Used in    : TP1 - Multi-Source Ingestion
Purpose    : Fast validation of TP1 v2 cross-domain relationships.
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def csv_rows(path):
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))

def json_rows(path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)

customers = csv_rows(ROOT / "data/source/master/customers_v2.csv")
products = csv_rows(ROOT / "data/source/master/products_v2.csv")
employees = csv_rows(ROOT / "data/source/master/employees_v2.csv")
assignments = csv_rows(ROOT / "data/source/master/account_assignments_v2.csv")

orders = csv_rows(ROOT / "data/source/sales_v2/orders_linked_v2.csv")
lines = csv_rows(ROOT / "data/source/sales_v2/order_lines_v2.csv")
opps = json_rows(ROOT / "data/source/crm_v2/opportunities_v2.json")
quotes = csv_rows(ROOT / "data/source/quotes_v2/quotes_v2.csv")
invoices = csv_rows(ROOT / "data/source/finance_v2/invoices_v2.csv")
payments = csv_rows(ROOT / "data/source/finance_v2/payments_v2.csv")
tickets = json_rows(ROOT / "data/source/support_v2/tickets_v2.json")
shipments = csv_rows(ROOT / "data/source/supply_chain_v2/shipments_v2.csv")
inventory = csv_rows(ROOT / "data/source/supply_chain_v2/inventory_v2.csv")
pos = csv_rows(ROOT / "data/source/procurement_v2/purchase_orders_v2.csv")
production = csv_rows(ROOT / "data/source/manufacturing_v2/production_orders_v2.csv")

IDS = {
    "customer": {r["customer_id"] for r in customers},
    "product": {r["product_id"] for r in products},
    "employee": {r["employee_id"] for r in employees},
    "order": {r["order_id"] for r in orders},
    "opportunity": {r["opportunity_id"] for r in opps},
    "quote": {r["quote_id"] for r in quotes},
    "invoice": {r["invoice_id"] for r in invoices},
}

errors = []

def fk(rows, field, valid, name):
    invalid = sum(
        1 for r in rows
        if r.get(field) and r[field] not in valid
    )
    if invalid:
        errors.append((name, invalid))

checks = [
    (assignments, "customer_id", IDS["customer"], "Assignment -> Customer"),
    (assignments, "account_owner_employee_id", IDS["employee"], "Assignment -> Employee"),

    (orders, "customer_id", IDS["customer"], "Order -> Customer"),
    (orders, "employee_id", IDS["employee"], "Order -> Employee"),
    (orders, "opportunity_id", IDS["opportunity"], "Order -> Opportunity"),
    (orders, "quote_id", IDS["quote"], "Order -> Quote"),

    (lines, "order_id", IDS["order"], "OrderLine -> Order"),
    (lines, "product_id", IDS["product"], "OrderLine -> Product"),

    (opps, "customer_id", IDS["customer"], "Opportunity -> Customer"),
    (opps, "product_id", IDS["product"], "Opportunity -> Product"),
    (opps, "owner_employee_id", IDS["employee"], "Opportunity -> Employee"),

    (quotes, "opportunity_id", IDS["opportunity"], "Quote -> Opportunity"),
    (quotes, "customer_id", IDS["customer"], "Quote -> Customer"),

    (invoices, "order_id", IDS["order"], "Invoice -> Order"),
    (payments, "invoice_id", IDS["invoice"], "Payment -> Invoice"),

    (tickets, "customer_id", IDS["customer"], "Ticket -> Customer"),
    (tickets, "order_id", IDS["order"], "Ticket -> Order"),
    (tickets, "product_id", IDS["product"], "Ticket -> Product"),

    (shipments, "order_id", IDS["order"], "Shipment -> Order"),
    (shipments, "product_id", IDS["product"], "Shipment -> Product"),

    (inventory, "product_id", IDS["product"], "Inventory -> Product"),
    (pos, "product_id", IDS["product"], "PO -> Product"),
    (production, "product_id", IDS["product"], "Production -> Product"),
]

for args in checks:
    fk(*args)

print("=== TP1 V2 E2E ===")
print(f"Customers         : {len(customers):,}")
print(f"Products          : {len(products):,}")
print(f"Employees         : {len(employees):,}")
print(f"Opportunities     : {len(opps):,}")
print(f"Quotes            : {len(quotes):,}")
print(f"Orders            : {len(orders):,}")
print(f"Order lines       : {len(lines):,}")
print(f"Invoices          : {len(invoices):,}")
print(f"Payments          : {len(payments):,}")
print(f"Tickets           : {len(tickets):,}")
print(f"Shipments         : {len(shipments):,}")
print(f"Inventory         : {len(inventory):,}")
print(f"Purchase orders   : {len(pos):,}")
print(f"Production orders : {len(production):,}")

print(f"\nFailed checks     : {len(errors)}")

for name, count in errors:
    print(f"ERROR: {name}: {count:,}")

print(
    "\nTP1 V2 E2E:",
    "OK" if not errors else "FAILED"
)

if errors:
    raise SystemExit(1)
