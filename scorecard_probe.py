
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_URL = "https://api.scorecard.dev/projects/github.com/ossf/scorecard"


def main():
    request = Request(
        API_URL,
        headers={"User-Agent": "Project-X-Ray/0.1"},
    )

    try:
        with urlopen(request, timeout=20) as response:
            report = json.loads(response.read().decode("utf-8"))

    except (HTTPError, URLError, TimeoutError) as error:
        print(f"Could not retrieve Scorecard report: {error}")
        return

    summary = {
        "repository": report.get("repo", {}).get("name"),
        "report_date": report.get("date"),
        "repository_commit": report.get("repo", {}).get("commit"),
        "scorecard_version": report.get("scorecard", {}).get("version"),
        "overall_score": report.get("score"),
        "checks": [
            {
                "name": check.get("name"),
                "score": check.get("score"),
                "reason": check.get("reason"),
                "details": check.get("details"),
                "documentation_url": (
                    check.get("documentation") or {}
                ).get("url"),
            }
            for check in report.get("checks", [])
        ],
    }

    output_file = "scorecard_report.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2, ensure_ascii=False)

    print(f"Repository: {summary['repository']}")
    print(f"Overall score: {summary['overall_score']}")
    print(f"Checks extracted: {len(summary['checks'])}")
    print(f"Saved structured report to {output_file}")


if __name__ == "__main__":
    main()
