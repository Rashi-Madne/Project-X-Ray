
import json

import sys

report_file = sys.argv[1] if len(sys.argv) > 1 else "scorecard_report.json"
with open(report_file, encoding="utf-8") as file:
    report = json.load(file)

# 1. Validate required metadata
required_fields = [
    "repository",
    "report_date",
    "repository_commit",
    "scorecard_version",
    "overall_score",
    "checks",
]

missing_fields = [
    field for field in required_fields
    if field not in report or report[field] is None
]

# 2. Validate the overall score
overall_score = report.get("overall_score")

invalid_overall_score = (
    not isinstance(overall_score, (int, float))
    or isinstance(overall_score, bool)
    or not 0 <= overall_score <= 10
)

# 3. Validate the checks collection
checks = report.get("checks", [])
if not isinstance(checks, list):
    raise ValueError("'checks' must be a list")

# 4. Validate individual scores
invalid_scores = []
missing_names = []

for index, check in enumerate(checks):
    if not isinstance(check, dict):
        invalid_scores.append(f"Check at index {index} is not an object")
        continue

    name = check.get("name")
    score = check.get("score")

    if not isinstance(name, str) or not name.strip():
        missing_names.append(f"Check at index {index}")

    if (
        not isinstance(score, (int, float))
        or isinstance(score, bool)
        or not 0 <= score <= 10
    ):
        invalid_scores.append(name or f"Check at index {index}")

# 5. Check for duplicate names
names = [
    check["name"].strip()
    for check in checks
    if isinstance(check, dict)
    and isinstance(check.get("name"), str)
    and check["name"].strip()
]

duplicates = sorted({
    name for name in names
    if names.count(name) > 1
})

# 6. Display validation results
print("Repository:", report.get("repository"))
print("Scorecard version:", report.get("scorecard_version"))
print("Overall score:", overall_score)
print("Total checks:", len(checks))
print("Missing metadata fields:", missing_fields)
print("Invalid overall score:", invalid_overall_score)
print("Invalid individual scores:", invalid_scores)
print("Missing check names:", missing_names)
print("Duplicate check names:", duplicates)

passed = (
    not missing_fields
    and not invalid_overall_score
    and not invalid_scores
    and not missing_names
    and not duplicates
)

print("Validation result:", "PASS" if passed else "FAIL")

if not passed:
    sys.exit(1)
