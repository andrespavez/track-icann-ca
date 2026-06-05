import json
from collections import Counter

INPUT_FILE = "data/repos_classified.json"


def load_data():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def main():

    repos = load_data()

    total = len(repos)

    counts = Counter(
        r.get("status", "UNKNOWN")
        for r in repos
    )

    print("\n=== CA MIGRATION REPORT ===\n")

    print(f"Total repositories scanned: {total}\n")

    for status in [
        "OLD_ONLY",
        "OLD_AND_NEW",
        "NEW_ONLY",
        "UNKNOWN"
    ]:

        count = counts.get(status, 0)

        pct = (
            count / total * 100
            if total
            else 0
        )

        print(
            f"{status:15} "
            f"{count:5} "
            f"({pct:.1f}%)"
        )

    print("\n=== ACTION REQUIRED ===\n")

    old_only = sorted(
        [
            r["repo"]
            for r in repos
            if r.get("status") == "OLD_ONLY"
        ]
    )

    print(
        f"{len(old_only)} repositories "
        f"still use ONLY the old root:\n"
    )

    for repo in old_only:
        print(f"- {repo}")

    print("\n=== MIGRATION IN PROGRESS ===\n")

    migrating = sorted(
        [
            r["repo"]
            for r in repos
            if r.get("status") == "OLD_AND_NEW"
        ]
    )

    if migrating:
        for repo in migrating:
            print(f"- {repo}")
    else:
        print("None")

    print("\n=== COMPLETED ===\n")

    completed = sorted(
        [
            r["repo"]
            for r in repos
            if r.get("status") == "NEW_ONLY"
        ]
    )

    if completed:
        for repo in completed:
            print(f"- {repo}")
    else:
        print("None")


if __name__ == "__main__":
    main()