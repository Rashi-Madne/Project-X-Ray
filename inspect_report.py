
from pathlib import Path
import json

# Locate the project folder automatically, regardless of the
# directory from which this script is executed.
PROJECT_DIR = Path(__file__).resolve().parent
REPORT_PATH = PROJECT_DIR / "scorecard_report.json"


def main():
    # Check whether the report exists.
    if not REPORT_PATH.exists():
        print("ERROR: scorecard_report.json was not found.")
        print("Expected location:", REPORT_PATH)
        print("Please ensure scorecard_probe.py has generated the report.")
        return

    # Load the JSON report.
    try:
        with REPORT_PATH.open("r", encoding="utf-8") as file:
            report = json.load(file)
    except json.JSONDecodeError as error:
        print("ERROR: The report contains invalid JSON.")
        print(error)
        return
    except OSError as error:
        print("ERROR: Could not read the report.")
        print(error)
        return

    # Validate the report structure.
    if not isinstance(report, dict):
        print("ERROR: The report must contain a JSON object.")
        return

    checks = report.get("checks")

    if not isinstance(checks, list):
        print("ERROR: The 'checks' field is missing or is not a list.")
        return

    # Display repository metadata.
    print("=" * 65)
    print("PROJECT X-RAY: SCORECARD REPORT INSPECTION")
    print("=" * 65)

    print("Repository:", report.get("repository", "MISSING"))
    print("Report date:", report.get("report_date", "MISSING"))
    print("Repository commit:", report.get("repository_commit", "MISSING"))
    print("Scorecard version:", report.get("scorecard_version", "MISSING"))
    print("Overall score:", report.get("overall_score", "MISSING"))
    print("Total checks:", len(checks))

    # Inventory every extracted check.
    print("\n" + "=" * 65)
    print("CHECK INVENTORY")
    print("=" * 65)

    missing_names = []
    missing_scores = []
    missing_reasons = []
    missing_documentation_urls = []
    invalid_details = []
    duplicate_names = []

    seen_names = set()

    for index, check in enumerate(checks, start=1):
        print(f"\nCheck #{index}")
        print("-" * 40)

        # Check that each entry is an object.
        if not isinstance(check, dict):
            print("ERROR: Check entry is not a JSON object.")
            invalid_details.append(index)
            continue

        name = check.get("name")
        score = check.get("score")
        reason = check.get("reason")
        details = check.get("details")
        documentation_url = check.get("documentation_url")

        # Count detail entries safely.
        details_count = len(details) if isinstance(details, list) else 0

        print("Name:", name)
        print("Score:", score)
        print("Reason present:", bool(reason))
        print("Details count:", details_count)
        print("Documentation URL present:", bool(documentation_url))

        # Identify missing fields.
        if not isinstance(name, str) or not name.strip():
            missing_names.append(index)
        else:
            if name in seen_names:
                duplicate_names.append(name)
            seen_names.add(name)

        if score is None:
            missing_scores.append(name or f"Check #{index}")

        if not isinstance(reason, str) or not reason.strip():
            missing_reasons.append(name or f"Check #{index}")

        if not isinstance(documentation_url, str) or not documentation_url.strip():
            missing_documentation_urls.append(name or f"Check #{index}")

        if not isinstance(details, list):
            invalid_details.append(name or f"Check #{index}")

    # Print the inventory summary.
    print("\n" + "=" * 65)
    print("INVENTORY SUMMARY")
    print("=" * 65)

    print("Total check entries:", len(checks))
    print("Unique named checks:", len(seen_names))
    print("Missing check names:", missing_names)
    print("Missing scores:", missing_scores)
    print("Missing reasons:", missing_reasons)
    print("Missing documentation URLs:", missing_documentation_urls)
    print("Invalid or missing details lists:", invalid_details)
    print("Duplicate check names:", duplicate_names)

    # Explain what this inspection does and does not establish.
    print("\n" + "=" * 65)
    print("INTERPRETATION")
    print("=" * 65)
    print("This script inventories the extracted JSON report.")
    print("It does not prove that extracted values match the original API.")
    print("Source-by-source comparison is required for that conclusion.")

    print("\nInspection completed.")


if __name__ == "__main__":
    main()
