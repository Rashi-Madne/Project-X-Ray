
import json
import subprocess
import sys
from pathlib import Path

report_path = Path("scorecard_report.json")
test_path = Path("scorecard_report_test.json")

try:
    with report_path.open(encoding="utf-8") as file:
        report = json.load(file)

    # Create a separate copy and deliberately insert an invalid score.
    test_report = json.loads(json.dumps(report))
    test_report["checks"][0]["score"] = 15

    with test_path.open("w", encoding="utf-8") as file:
        json.dump(test_report, file, indent=2)

    print("Temporary invalid report created.")

    # Run the validator against the invalid report.
    result = subprocess.run(
        [sys.executable, "validate_scores.py", str(test_path)],
        capture_output=True,
        text=True,
        check=False,
    )

    print(result.stdout)

    

    if result.returncode != 1 or "Validation result: FAIL" not in result.stdout:
        print("TEST FAILED: Invalid score was not rejected correctly.")
        if result.stderr:
            print(result.stderr)
        sys.exit(1)

    print("TEST PASSED: Invalid score was rejected correctly.")

finally:
    if test_path.exists():
        test_path.unlink()
        print("Temporary report removed.")
