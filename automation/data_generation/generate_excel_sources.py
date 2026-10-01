import csv
from pathlib import Path
from openpyxl import Workbook

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/source"

def csv_to_xlsx(csv_path, xlsx_path, sheet):
    with csv_path.open(encoding="utf-8") as f:
        rows = csv.reader(f)

        wb = Workbook(write_only=True)
        ws = wb.create_sheet(sheet)

        count = 0
        for row in rows:
            ws.append(row)
            count += 1

        wb.save(xlsx_path)

    print(f"{xlsx_path.name}: {count - 1:,} data rows")

# HR source
hr = SOURCE / "hr"
hr.mkdir(parents=True, exist_ok=True)

csv_to_xlsx(
    SOURCE / "master/employees.csv",
    hr / "employees.xlsx",
    "Employees"
)

# Forecast source
csv_to_xlsx(
    SOURCE / "forecast/forecast.csv",
    SOURCE / "forecast/forecast.xlsx",
    "Forecast"
)

print("\nEXCEL SOURCES: OK")
