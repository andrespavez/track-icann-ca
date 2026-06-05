import json
import sys

ISSUES_FILE = "data/issues.json"

VALID_PRIORITIES = {
    "HIGH",
    "NORMAL",
    "LOW"
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

    if len(sys.argv) != 3:

        print(
            "Usage:\n"
            "python scripts/set_priority.py "
            "<repo> <priority>"
        )
        return

    repo = sys.argv[1]
    priority = sys.argv[2]

    if priority not in VALID_PRIORITIES:

        print(
            f"Invalid priority: {priority}"
        )
        return

    issues = load_issues()

    if repo not in issues:

        print(
            f"Repository not found: {repo}"
        )
        return

    issues[repo]["priority"] = priority

    save_issues(issues)

    print(
        f"{repo} -> {priority}"
    )


if __name__ == "__main__":
    main()