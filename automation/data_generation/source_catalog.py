SOURCE_CATALOG = {
    "sales":         {"type": "postgresql", "domain": "Sales"},
    "product":       {"type": "postgresql", "domain": "Product"},
    "crm":           {"type": "api_json",   "domain": "CRM"},
    "finance":       {"type": "excel_csv",  "domain": "Finance"},
    "pricing":       {"type": "api_csv",    "domain": "Pricing"},
    "supply_chain":  {"type": "csv",        "domain": "Supply Chain"},
    "procurement":   {"type": "excel_csv",  "domain": "Procurement"},
    "manufacturing": {"type": "csv_json",   "domain": "Manufacturing"},
    "partners":      {"type": "api_json",   "domain": "Partners & Alliances"},
    "distribution":  {"type": "csv",        "domain": "Distribution"},
    "support":       {"type": "api_json",   "domain": "Support"},
    "hr":            {"type": "excel",      "domain": "HR"},
    "marketing":     {"type": "api_csv",    "domain": "Marketing"},
    "geography":     {"type": "json",       "domain": "Geography"},
    "forecast":      {"type": "excel",      "domain": "Targets & Forecast"},
}

if __name__ == "__main__":
    for name, cfg in SOURCE_CATALOG.items():
        print(f"{name:15} | {cfg['type']:12} | {cfg['domain']}")
    print(f"\nTOTAL SOURCES: {len(SOURCE_CATALOG)}")
