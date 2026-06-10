import json
import sys

ISSUES_FILE = "data/issues.json"


VALID_STATUSES = {
    "NOT_CONTACTED",
    "CONTACTED",
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

    if len(sys.argv) < 4:

        print(
            "Usage:\n"
            "python scripts/update_issue.py "
            "<repo> <status> <issue_url> <notes>"
        )

        return

    repo = sys.argv[1]
    status = sys.argv[2]
    issue_url = sys.argv[3]

    if status not in VALID_STATUSES:

        print(
            f"Invalid status: {status}"
        )

        return

    issues = load_issues()

    if repo not in issues:

        print(
            f"Repository not found: {repo}"
        )

        return

    notes = None

    if len(sys.argv) > 4:
        notes = sys.argv[4]

    issues[repo]["issue_status"] = status
    issues[repo]["issue_url"] = issue_url

    if notes:
        issues[repo]["notes"] = notes

    save_issues(issues)

    print(
        f"Updated {repo} -> {status}"
    )


if __name__ == "__main__":
    main()