"""
Component   : Account Owner Assignment
Technology  : Python 3
Technique   : Rule-Based Territory and Sales Ownership Assignment
Used in     : TP1 - Multi-Source Ingestion

Purpose:
Assign each customer to an active Sales employee matching both
sales organization and geographic region.

Business Controls:
- Consumer accounts -> Consumer Sales
- SMB accounts -> SMB Sales
- Mid-Market accounts -> Commercial Sales
- Enterprise accounts -> Enterprise Sales
- Public Sector accounts -> Public Sector Sales
- Federal accounts -> Federal Sales
- Education accounts -> Education Sales
- Healthcare accounts -> Healthcare Sales
- Customer and account owner regions must match
"""

import csv
import random
from collections import defaultdict
from pathlib import Path

random.seed(54)

ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / "data/source/master"

def read_csv(path):
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))

customers = read_csv(MASTER / "customers_v2.csv")
employees = read_csv(MASTER / "employees_v2.csv")
assignments = read_csv(MASTER / "account_assignments.csv")

# TECHNIQUE: Eligibility pool.
# Only active Sales employees can own customer accounts.
sales_pool = defaultdict(list)

for employee in employees:
    if (
        employee["department"] == "Sales"
        and employee["employment_status"] == "Active"
    ):
        key = (
            employee["sales_organization"],
            employee["region"]
        )
        sales_pool[key].append(employee)

customer_map = {
    customer["customer_id"]: customer
    for customer in customers
}

errors = 0
updated = []

for assignment in assignments:
    customer = customer_map[assignment["customer_id"]]

    key = (
        assignment["sales_organization"],
        customer["region"]
    )

    candidates = sales_pool.get(key, [])

    if not candidates:
        errors += 1
        continue

    owner = random.choice(candidates)

    assignment["account_owner_employee_id"] = owner["employee_id"]
    assignment["account_owner_role"] = owner["role"]
    assignment["owner_region"] = owner["region"]

    updated.append(assignment)

if errors:
    print(f"Unassigned accounts : {errors:,}")
    raise SystemExit("ACCOUNT OWNER ASSIGNMENT: FAILED")

output = MASTER / "account_assignments_v2.csv"

fields = list(updated[0].keys())

with output.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(updated)

# Independent validation.
employee_map = {
    employee["employee_id"]: employee
    for employee in employees
}

validation_errors = 0

for assignment in updated:
    customer = customer_map[assignment["customer_id"]]
    employee = employee_map[assignment["account_owner_employee_id"]]

    if employee["department"] != "Sales":
        validation_errors += 1

    if employee["sales_organization"] != assignment["sales_organization"]:
        validation_errors += 1

    if employee["region"] != customer["region"]:
        validation_errors += 1

print(f"Accounts assigned  : {len(updated):,}")
print(f"Unassigned         : {errors:,}")
print(f"Validation errors  : {validation_errors:,}")
print(f"Sales owners used  : {len(set(r['account_owner_employee_id'] for r in updated)):,}")

print(
    "ACCOUNT OWNER ASSIGNMENT:",
    "OK" if validation_errors == 0 else "FAILED"
)
