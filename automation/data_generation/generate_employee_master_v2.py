"""
Component   : Employee & Organization Master v2
Technology  : Python 3
Techniques  : Organizational Master Data, Role-Based Assignment
Used in     : TP1 - Multi-Source Ingestion

Purpose:
Create a structured enterprise workforce where departments, roles,
customer segments and responsibilities are logically aligned.

Data Classification:
SYNTHETIC - No real employee or personal data is used.
"""

import csv
import random
from pathlib import Path

random.seed(53)

ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / "data/source/master"

ORGANIZATION = {
    "Sales": {
        "count": 300,
        "roles": [
            "Account Executive", "Account Manager",
            "Sales Specialist", "Sales Director"
        ],
        "sales_organizations": [
            "Consumer Sales", "SMB Sales", "Commercial Sales",
            "Enterprise Sales", "Public Sector Sales", "Federal Sales",
            "Education Sales", "Healthcare Sales"
        ]
    },
    "Presales": {
        "count": 100,
        "roles": [
            "Solutions Architect", "Systems Engineer",
            "AI Specialist", "Cloud Specialist",
            "Storage Specialist", "Networking Specialist"
        ]
    },
    "Professional Services": {
        "count": 80,
        "roles": [
            "Consultant", "Implementation Engineer",
            "Project Manager", "Solution Architect"
        ]
    },
    "Support": {
        "count": 100,
        "roles": [
            "Support Engineer", "Technical Support Specialist",
            "Escalation Manager"
        ]
    },
    "Finance": {
        "count": 60,
        "roles": [
            "Financial Analyst", "Billing Specialist",
            "Credit Analyst", "Finance Manager"
        ]
    },
    "Supply Chain": {
        "count": 50,
        "roles": [
            "Supply Planner", "Logistics Specialist",
            "Inventory Analyst"
        ]
    },
    "Marketing": {
        "count": 40,
        "roles": [
            "Campaign Manager", "Marketing Analyst",
            "Demand Generation Specialist"
        ]
    },
    "Product & Engineering": {
        "count": 50,
        "roles": [
            "Product Manager", "Software Engineer",
            "Data Engineer", "AI Engineer"
        ]
    },
    "Management": {
        "count": 20,
        "roles": [
            "Director", "Senior Director",
            "Vice President"
        ]
    }
}

regions = ["EMEA", "AMER", "APJ"]

rows = []
employee_number = 1

for department, config in ORGANIZATION.items():
    for _ in range(config["count"]):
        role = random.choice(config["roles"])

        sales_org = ""
        if department == "Sales":
            sales_org = random.choice(config["sales_organizations"])

        rows.append({
            "employee_id": f"EMP-{employee_number:05}",
            "employee_name": f"Synthetic Employee {employee_number:05}",
            "department": department,
            "role": role,
            "region": random.choice(regions),
            "sales_organization": sales_org,
            "employment_status": random.choice(["Active"] * 9 + ["Inactive"]),
            "data_classification": "SYNTHETIC"
        })

        employee_number += 1

path = MASTER / "employees_v2.csv"

with path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Employees : {len(rows):,}")

print("\n=== DEPARTMENT DISTRIBUTION ===")
for department in ORGANIZATION:
    count = sum(r["department"] == department for r in rows)
    print(f"{department:25} {count:>4}")

print("\nEMPLOYEE MASTER V2: OK")
