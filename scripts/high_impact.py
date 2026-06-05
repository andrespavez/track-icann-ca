import json

REPOS_FILE = "data/repos_classified.json"
ISSUES_FILE = "data/issues.json"

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():

    repos = load_json(REPOS_FILE)    
    issues = load_json(ISSUES_FILE)

    candidates = [
        r for r in repos
        if r.get("status") == "OLD_ONLY"
    ]

    candidates.sort(
        key=lambda r: (
            (r.get("stars") or 0)
            +
            (r.get("forks") or 0)
        ), 
        reverse=True
    )

    print(
        "\n=== HIGHEST IMPACT REPOSITORIES ===\n"
    )

    for repo in candidates[:25]:

        issue = issues.get(repo["repo"], {})
        priority = issue.get(
            "priority",
            "NORMAL"
        )

        impact = (
            (repo.get("stars") or 0)
            +
            (repo.get("forks") or 0)
        )

        print(
            f"{repo['repo']}\n"
            f"  Impact: {impact}\n"
            f"  Stars: {repo.get('stars', 0)}\n"
            f"  Forks: {repo.get('forks', 0)}\n"
            f"  Priority: {priority}\n"
        )


if __name__ == "__main__":
    main()