import json
from collections import Counter

REPOS_FILE = "data/repos_classified.json"
ISSUES_FILE = "data/issues.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():

    repos = load_json(REPOS_FILE)
    issues = load_json(ISSUES_FILE)

    old_only = [
        r
        for r in repos
        if r.get("status") == "OLD_ONLY"
    ]

    campaign_counter = Counter()

    for repo in old_only:

        repo_name = repo["repo"]

        issue_info = issues.get(
            repo_name,
            {}
        )

        status = issue_info.get(
            "issue_status",
            "NOT_CONTACTED"
        )

        campaign_counter[status] += 1

    print("\n=== CAMPAIGN REPORT ===\n")

    print(
        f"Repositories requiring action: "
        f"{len(old_only)}\n"
    )

    old_and_new = sum(
        1
        for r in repos
        if r.get("status") == "OLD_AND_NEW"
    )

    new_only = sum(
        1
        for r in repos
        if r.get("status") == "NEW_ONLY"
    )

    print(
        f"Already compliant "
        f"(OLD_AND_NEW): {old_and_new}"
    )

    print(
        f"Fully migrated "
        f"(NEW_ONLY): {new_only}\n"
    )

    for status in [
        "NOT_CONTACTED",
        "CONTACTED",
        "ISSUE_OPEN",
        "ISSUE_CLOSED",
        "FIX_MERGED"
    ]:

        print(
            f"{status:15}"
            f"{campaign_counter.get(status, 0)}"
        )

    print("\n=== NEXT ACTIONS ===\n")

    not_contacted = []

    for repo in old_only:

        repo_name = repo["repo"]

        issue_info = issues.get(
            repo_name,
            {}
        )

        if (
            issue_info.get(
                "issue_status",
                "NOT_CONTACTED"
            )
            == "NOT_CONTACTED"
        ):
            not_contacted.append(
                repo_name
            )

    print(
        f"{len(not_contacted)} repositories "
        f"have not been contacted yet.\n"
    )

    for repo in sorted(
        not_contacted[:20]
    ):
        print(
            f"- {repo}"
        )

    if len(not_contacted) > 20:
        print(
            f"\n... and "
            f"{len(not_contacted)-20} more"
        )


if __name__ == "__main__":
    main()