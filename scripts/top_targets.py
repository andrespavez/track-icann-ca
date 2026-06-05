import json

ISSUES_FILE = "data/issues.json"
REPOS_FILE = "data/repos_classified.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():

    issues = load_json(ISSUES_FILE)

    repos = {
        r["repo"]: r
        for r in load_json(REPOS_FILE)
    }

    candidates = []

    for repo_name, issue in issues.items():

        if issue["issue_status"] != "NOT_CONTACTED":
            continue

        repo = repos.get(repo_name)

        if not repo:
            continue

        candidates.append({
            "repo": repo_name,
            "priority": issue.get("priority", "NORMAL"),
            "stars": repo.get("stars", 0) or 0,
            "forks": repo.get("forks", 0) or 0,
            "impact": (
                (repo.get("stars", 0) or 0)
                +
                (repo.get("forks", 0) or 0)
            ),
            "owner_type": repo.get("owner_type"),
            "updated_at": repo.get("updated_at")
        })

    priority_order = {
        "HIGH": 3,
        "NORMAL": 2,
        "LOW": 1
    }

    candidates.sort(
        key=lambda x: (
            priority_order.get(x["priority"], 0),
            x["impact"]
        ),
        reverse=True
    )

    print("\n=== TOP OUTREACH TARGETS ===\n")

    for repo in candidates[:25]:

        print(
            f"{repo['repo']}\n"
            f"  Priority: {repo['priority']}\n"
            f"  Stars: {repo['stars']}\n"
            f"  Forks: {repo['forks']}\n"
            f"  Owner: {repo['owner_type']}\n"
            f"  Impact: {repo['impact']}\n"   
        )


if __name__ == "__main__":
    main()