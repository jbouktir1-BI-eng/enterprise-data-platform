import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/source"

def csv_ids(path, key):
    with path.open(encoding="utf-8") as f:
        return {r[key] for r in csv.DictReader(f)}

def check_csv_fk(path, field, valid):
    with path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    invalid = sum(1 for r in rows if r[field] not in valid)
    print(f"{path.name:24} {field:15} rows={len(rows):>7,} invalid={invalid:,}")
    return invalid

customers = csv_ids(SOURCE/"master/customers.csv", "customer_id")
products = csv_ids(SOURCE/"master/products.csv", "product_id")
employees = csv_ids(SOURCE/"master/employees.csv", "employee_id")
orders = csv_ids(SOURCE/"sales/orders.csv", "order_id")
suppliers = csv_ids(SOURCE/"procurement/suppliers.csv", "supplier_id")
partners = csv_ids(SOURCE/"partners/partners.csv", "partner_id")

errors = 0

errors += check_csv_fk(SOURCE/"sales/orders.csv", "customer_id", customers)
errors += check_csv_fk(SOURCE/"sales/orders.csv", "employee_id", employees)
errors += check_csv_fk(SOURCE/"sales/order_lines.csv", "product_id", products)
errors += check_csv_fk(SOURCE/"finance/invoices.csv", "order_id", orders)
errors += check_csv_fk(SOURCE/"procurement/purchase_orders.csv", "supplier_id", suppliers)
errors += check_csv_fk(SOURCE/"procurement/purchase_orders.csv", "product_id", products)
errors += check_csv_fk(SOURCE/"distribution/sell_out.csv", "partner_id", partners)
errors += check_csv_fk(SOURCE/"distribution/sell_out.csv", "product_id", products)

with (SOURCE/"support/tickets.json").open(encoding="utf-8") as f:
    tickets = json.load(f)

bad_customer = sum(1 for r in tickets if r["customer_id"] not in customers)
bad_product = sum(1 for r in tickets if r["product_id"] not in products)

errors += bad_customer + bad_product

print(f"{'tickets.json':24} customer_id     rows={len(tickets):>7,} invalid={bad_customer:,}")
print(f"{'tickets.json':24} product_id      rows={len(tickets):>7,} invalid={bad_product:,}")

print("\nSOURCE INTEGRITY:", "OK" if errors == 0 else f"FAILED ({errors} errors)")

raise SystemExit(0 if errors == 0 else 1)
