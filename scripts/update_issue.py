import json
import sys

ISSUES_FILE = "data/issues.json"


VALID_STATUSES = {
    "NOT_CONTACTED",
    "ISSUE_OPEN",
    "ISSUE_CLOSED",
    "FIX_MERGED"
}


def load_issues():
    with open(
        ISSUES_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def save_issues(data):
    with open(
        ISSUES_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            indent=2
        )


def main():

    if len(sys.argv) < 3:

        print(
            "Usage:\n"
            "python scripts/update_issue.py "
            "<repo> <status> [issue_url]"
        )

        return

    repo = sys.argv[1]
    status = sys.argv[2]

    if status not in VALID_STATUSES:

        print(
            f"Invalid status: {status}"
        )

        return

    issue_url = None

    if len(sys.argv) > 3:
        issue_url = sys.argv[3]

    issues = load_issues()

    if repo not in issues:

        print(
            f"Repository not found: {repo}"
        )

        return

    issues[repo]["issue_status"] = status

    if issue_url:
        issues[repo]["issue_url"] = issue_url

    save_issues(issues)

    print(
        f"Updated {repo} -> {status}"
    )


if __name__ == "__main__":
    main()