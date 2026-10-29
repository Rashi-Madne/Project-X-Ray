from pathlib import Path
import json

project_folder=Path(__file__).resolve().parent
report_path=project_folder / "scorecard_report.json"
with report_path.open(encoding="utf-8")as file:
    report=json.load(file)

checks=report["checks"]
print("total checks:", len(checks))

for check in checks:
    name=check.get("name", "UNKNOWN")

    if "details" not in check:
        print(name, "| MISSING FIELD")
        continue
    details=check["details"]
    print(
        name, 
        "| Type:", type(details).__name__,
        "| Items:", len(details) if isinstance(details,list)else"N/A"
        )