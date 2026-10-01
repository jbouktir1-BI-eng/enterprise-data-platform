VOLUMES = {
    "customers":          10_000,
    "contacts":           15_000,
    "products":            1_500,
    "employees":             800,
    "suppliers":             300,
    "partners":              500,
    "warehouses":             30,
    "plants":                 12,

    "orders":             80_000,
    "order_lines":       240_000,
    "quotes":             35_000,
    "opportunities":      20_000,

    "invoices":           75_000,
    "payments":           70_000,

    "inventory":          45_000,
    "shipments":          65_000,
    "purchase_orders":    25_000,
    "production_orders":  30_000,

    "support_tickets":    40_000,
    "marketing_leads":    30_000,
    "forecast_rows":      25_000
}

if __name__ == "__main__":
    total = 0
    for table, rows in VOLUMES.items():
        print(f"{table:20} | {rows:>10,}")
        total += rows

    print("-" * 34)
    print(f"{'TOTAL':20} | {total:>10,}")
