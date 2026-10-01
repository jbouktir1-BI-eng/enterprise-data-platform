"""
Component   : Finance History v2
Technology  : Python 3
Technique   : Order-to-Cash, Financial Reconciliation
Used in     : TP1 - Multi-Source Ingestion

Lineage:
Opportunity -> Quote -> Order -> Invoice -> Payment

Purpose:
Generate invoices and payments from actual Sales v2 order amounts while
preserving CRM, quote, contract and customer traceability.

Data Classification:
SYNTHETIC
"""

import csv
import random
from collections import defaultdict, Counter
from datetime import date, timedelta
from pathlib import Path

random.seed(58)

ROOT = Path(__file__).resolve().parents[2]
SALES = ROOT / "data/source/sales_v2"
MASTER = ROOT / "data/source/master"
OUT = ROOT / "data/source/finance_v2"
OUT.mkdir(parents=True, exist_ok=True)


def read_csv(path):
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


orders = read_csv(SALES / "orders_linked_v2.csv")
lines = read_csv(SALES / "order_lines_v2.csv")
customers = read_csv(MASTER / "customers_v2.csv")

customer_map = {r["customer_id"]: r for r in customers}

lines_by_order = defaultdict(list)

for line in lines:
    lines_by_order[line["order_id"]].append(line)

invoices = []
payments = []

invoice_number = 1
payment_number = 1

for order in orders:

    # Cancelled orders must not generate invoices.
    if order["status"] == "Cancelled":
        continue

    order_total = round(sum(
        float(line["net_amount"])
        for line in lines_by_order[order["order_id"]]
    ), 2)

    customer = customer_map[order["customer_id"]]
    order_date = date.fromisoformat(order["order_date"])

    invoice_date = order_date + timedelta(
        days=random.randint(0, 15)
    )

    terms = customer["default_payment_terms"]

    due_days = {
        "Prepaid": 0,
        "Card": 0,
        "Net 15": 15,
        "Net 30": 30,
        "Net 45": 45,
        "Net 60": 60
    }.get(terms, 30)

    due_date = invoice_date + timedelta(days=due_days)

    invoice_id = f"INV-{invoice_number:08}"
    invoice_number += 1

    # Most invoices are fully paid, while a smaller portion remains
    # partially paid or open to support realistic receivables analysis.
    payment_state = random.choices(
        ["Paid", "Partially Paid", "Open"],
        weights=[88, 7, 5],
        k=1
    )[0]

    if payment_state == "Paid":
        paid_amount = order_total
    elif payment_state == "Partially Paid":
        paid_amount = round(
            order_total * random.uniform(0.20, 0.80), 2
        )
    else:
        paid_amount = 0.0

    balance = round(order_total - paid_amount, 2)

    invoices.append({
        "invoice_id": invoice_id,
        "order_id": order["order_id"],
        "customer_id": order["customer_id"],
        "contract_id": order["contract_id"],
        "opportunity_id": order["opportunity_id"],
        "quote_id": order["quote_id"],
        "invoice_date": invoice_date.isoformat(),
        "due_date": due_date.isoformat(),
        "payment_terms": terms,
        "currency": order["currency"],
        "invoice_amount": order_total,
        "paid_amount": paid_amount,
        "balance_amount": balance,
        "payment_status": payment_state,
        "data_classification": "SYNTHETIC"
    })

    if paid_amount <= 0:
        continue

    # Large invoices may be settled using multiple payments.
    payment_count = (
        random.choice([2, 3])
        if paid_amount >= 100_000 and random.random() < 0.30
        else 1
    )

    remaining = paid_amount

    for sequence in range(1, payment_count + 1):

        if sequence == payment_count:
            amount = remaining
        else:
            amount = round(
                remaining * random.uniform(0.30, 0.60), 2
            )
            remaining = round(remaining - amount, 2)

        payment_date = invoice_date + timedelta(
            days=random.randint(0, max(due_days + 30, 15))
        )

        payments.append({
            "payment_id": f"PAY-{payment_number:09}",
            "invoice_id": invoice_id,
            "customer_id": order["customer_id"],
            "payment_sequence": sequence,
            "payment_date": payment_date.isoformat(),
            "payment_method": random.choice([
                "Bank Transfer",
                "Card",
                "ACH",
                "Wire Transfer"
            ]),
            "currency": order["currency"],
            "payment_amount": amount,
            "data_classification": "SYNTHETIC"
        })

        payment_number += 1


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


write_csv(OUT / "invoices_v2.csv", invoices)
write_csv(OUT / "payments_v2.csv", payments)


# ---------------- RECONCILIATION ----------------

payments_by_invoice = defaultdict(float)

for payment in payments:
    payments_by_invoice[payment["invoice_id"]] += float(
        payment["payment_amount"]
    )

errors = 0

for invoice in invoices:

    invoice_amount = float(invoice["invoice_amount"])
    expected_paid = float(invoice["paid_amount"])
    balance = float(invoice["balance_amount"])

    actual_paid = round(
        payments_by_invoice[invoice["invoice_id"]], 2
    )

    if abs(actual_paid - expected_paid) > 0.01:
        errors += 1

    if abs((expected_paid + balance) - invoice_amount) > 0.01:
        errors += 1

status_counts = Counter(
    invoice["payment_status"]
    for invoice in invoices
)

print(f"Invoices             : {len(invoices):,}")
print(f"Payments             : {len(payments):,}")

print("\n=== PAYMENT STATUS ===")
for status, count in sorted(status_counts.items()):
    print(f"{status:16} {count:>7,}")

print(f"\nReconciliation errors: {errors:,}")

print(
    "FINANCE HISTORY V2:",
    "OK" if errors == 0 else "FAILED"
)
