import json

REPOS_FILE = "data/repos_classified.json"
ISSUES_FILE = "data/issues.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():

    repos = load_json(REPOS_FILE)
    issues = load_json(ISSUES_FILE)

    queue = {
        "HIGH": [],
        "NORMAL": [],
        "LOW": []
    }

    for repo in repos:

        if repo.get("status") != "OLD_ONLY":
            continue

        repo_name = repo["repo"]

        issue_info = issues.get(
            repo_name,
            {}
        )

        if issue_info.get(
            "issue_status",
            "NOT_CONTACTED"
        ) != "NOT_CONTACTED":
            continue

        priority = issue_info.get(
            "priority",
            "NORMAL"
        )

        queue.setdefault(
            priority,
            []
        ).append(repo_name)

    print("\n=== CAMPAIGN QUEUE ===\n")

    total = 0

    for priority in [
        "HIGH",
        "NORMAL",
        "LOW"
    ]:

        repos_list = sorted(
            queue.get(priority, [])
        )

        total += len(repos_list)

        print(
            f"=== {priority} PRIORITY "
            f"({len(repos_list)}) ===\n"
        )

        for repo in repos_list:
            print(f"- {repo}")

        print()

    print(
        f"Total pending outreach: "
        f"{total}"
    )


if __name__ == "__main__":
    main()