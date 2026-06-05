import json
from pathlib import Path
from collections import defaultdict

SNAPSHOT_DIR = "data/snapshots"


def load_snapshots():

    files = sorted(
        Path(SNAPSHOT_DIR).glob("snapshot_*.json")
    )

    snapshots = []

    for file in files:

        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        snapshots.append(
            {
                "name": file.name,
                "data": data
            }
        )

    return snapshots


def summarize(data):

    result = defaultdict(int)

    for repo in data:
        result[
            repo.get("status", "UNKNOWN")
        ] += 1

    return result


def build_repo_map(data):

    return {
        repo["repo"]: repo["status"]
        for repo in data
    }


def main():

    snapshots = load_snapshots()

    if len(snapshots) < 2:
        print(
            "Need at least 2 snapshots."
        )
        return

    first = snapshots[0]
    last = snapshots[-1]

    print("\n=== SNAPSHOT SUMMARY ===\n")

    for snap in snapshots:

        summary = summarize(
            snap["data"]
        )

        total = len(
            snap["data"]
        )

        print(
            f"{snap['name']}"
        )

        print(
            f"  TOTAL: {total}"
        )

        print(
            f"  OLD_ONLY: "
            f"{summary.get('OLD_ONLY',0)}"
        )

        print(
            f"  OLD_AND_NEW: "
            f"{summary.get('OLD_AND_NEW',0)}"
        )

        print(
            f"  NEW_ONLY: "
            f"{summary.get('NEW_ONLY',0)}"
        )

        print("")

    print(
        "\n=== STATUS CHANGES ===\n"
    )

    old_map = build_repo_map(
        first["data"]
    )

    new_map = build_repo_map(
        last["data"]
    )

    changes = []

    for repo, old_status in old_map.items():

        new_status = new_map.get(
            repo
        )

        if (
            new_status
            and old_status != new_status
        ):

            changes.append(
                (
                    repo,
                    old_status,
                    new_status
                )
            )

    if not changes:

        print(
            "No repository status changes detected."
        )

    else:

        for (
            repo,
            old_status,
            new_status
        ) in sorted(changes):

            print(
                f"{repo}"
            )

            print(
                f"  {old_status}"
                f" -> "
                f"{new_status}"
            )

            print()

    print(
        "\n=== TREND SUMMARY ===\n"
    )

    def count(data, status):

        return sum(
            1
            for r in data
            if r.get("status") == status
        )

    for status in [
        "OLD_ONLY",
        "OLD_AND_NEW",
        "NEW_ONLY"
    ]:

        before = count(
            first["data"],
            status
        )

        after = count(
            last["data"],
            status
        )

        delta = after - before

        print(
            f"{status:15}"
            f"{before:5}"
            f" -> "
            f"{after:5}"
            f" ({delta:+d})"
        )


if __name__ == "__main__":
    main()