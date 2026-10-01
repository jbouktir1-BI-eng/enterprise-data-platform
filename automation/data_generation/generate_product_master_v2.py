"""
Component   : Enterprise Product Master v2
Technology  : Python 3
Technique   : Hierarchical Master Data Management (MDM)
Used in     : TP1 - Multi-Source Ingestion

Purpose:
Build a technology-neutral enterprise product and solution hierarchy.

Important:
Product taxonomy is inspired by publicly documented enterprise technology
portfolios. Generated product records and commercial attributes are synthetic.

Supports:
Hardware, Software, SaaS, Cloud, AI, Networking, Storage, Security,
Telemetry, Services, Ready Nodes, Appliances, Validated Designs,
Workload-Ready Bundles and consumption-based offerings.
"""

import csv
import random
from pathlib import Path

random.seed(51)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/source/master"

CATALOG = [
    # Portfolio, Category, Family, Offering, Workload, Minimum Customer Tier

    ("Client & Edge", "Client", "Business PCs",
     "Hardware", "End User Computing", "Consumer"),

    ("Client & Edge", "Workstation", "Professional Workstations",
     "Hardware", "Engineering", "SMB"),

    ("Infrastructure", "Compute", "Enterprise Servers",
     "Hardware", "General Compute", "SMB"),

    ("Infrastructure", "Storage", "Block Storage",
     "Hardware", "Database", "Mid-Market"),

    ("Infrastructure", "Storage", "File & Object Storage",
     "Hardware", "Data Platform", "Mid-Market"),

    ("Infrastructure", "Networking", "Data Center Networking",
     "Hardware", "Networking", "SMB"),

    ("Infrastructure", "HCI", "Hyperconverged Infrastructure",
     "Appliance", "Virtualization", "Mid-Market"),

    ("AI & Data", "AI Infrastructure", "Accelerated Compute",
     "Solution", "AI/ML", "Enterprise"),

    ("AI & Data", "HPC", "High Performance Computing",
     "Solution", "HPC", "Enterprise"),

    ("AI & Data", "Data Platform", "Analytics Platform",
     "Platform", "Analytics", "Mid-Market"),

    ("Software", "Virtualization", "Virtualization Platform",
     "Software", "Virtualization", "SMB"),

    ("Software", "Security", "Cyber Recovery",
     "Software", "Cybersecurity", "Mid-Market"),

    ("Software", "Observability", "Telemetry & Observability",
     "SaaS", "Observability", "SMB"),

    ("Software", "AIOps", "Infrastructure Intelligence",
     "SaaS", "IT Operations", "Mid-Market"),

    ("Cloud & Services", "Private Cloud", "Private Cloud Platform",
     "Platform", "Private Cloud", "Mid-Market"),

    ("Cloud & Services", "As-a-Service", "Infrastructure as a Service",
     "As-a-Service", "Hybrid Cloud", "Mid-Market"),

    ("Cloud & Services", "Professional Services", "Consulting Services",
     "Service", "Transformation", "SMB"),

    ("Cloud & Services", "Support", "Enterprise Support",
     "Service", "Support", "Consumer"),
]

SOLUTION_TYPES = [
    "Standalone Product",
    "Ready Node",
    "Appliance",
    "Workload-Ready Bundle",
    "Validated Design",
    "Reference Architecture",
    "Integrated System",
    "SaaS Subscription",
    "As-a-Service Offering"
]

rows = []

for i in range(1, 1501):
    portfolio, category, family, offering, workload, minimum_tier = \
        random.choice(CATALOG)

    solution_type = random.choice(SOLUTION_TYPES)

    # SaaS offerings must use subscription-oriented commercial models.
    if offering == "SaaS":
        solution_type = "SaaS Subscription"
        consumption = "Subscription"
        license_model = random.choice(["Per User", "Per Node", "Capacity Based"])

    # As-a-Service offerings use consumption-based commercial models.
    elif offering == "As-a-Service":
        solution_type = "As-a-Service Offering"
        consumption = random.choice(["Pay-per-use", "Consumption Based"])
        license_model = "Subscription"

    else:
        consumption = random.choice(["CapEx", "Subscription", "License"])
        license_model = random.choice([
            "N/A", "Perpetual", "Subscription", "Per Node", "Per Core"
        ])

    rows.append({
        "product_id": f"PROD-{i:05}",
        "portfolio": portfolio,
        "category": category,
        "product_family": family,
        "product_line": f"{family} Line {random.randint(1,10):02}",
        "product_name": f"{family} Offering {i:04}",
        "offering_type": offering,
        "solution_type": solution_type,
        "workload": workload,
        "minimum_customer_tier": minimum_tier,
        "consumption_model": consumption,
        "license_model": license_model,
        "lifecycle": random.choice(["Active"] * 8 + ["Launch", "End-of-Life"]),
        "data_classification": "SYNTHETIC",
        "source_provider": "Enterprise Data Platform Generator"
    })

path = OUT / "products_v2.csv"

with path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Products       : {len(rows):,}")
print(f"Portfolios     : {len(set(r['portfolio'] for r in rows))}")
print(f"Categories     : {len(set(r['category'] for r in rows))}")
print(f"Families       : {len(set(r['product_family'] for r in rows))}")
print(f"Workloads      : {len(set(r['workload'] for r in rows))}")
print(f"Solution types : {len(set(r['solution_type'] for r in rows))}")

print("\nPRODUCT MASTER V2: OK")
