import json
from common import priority_score

ISSUES_FILE = "data/issues.json"
REPOS_FILE = "data/repos_classified.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():

    repos = {
        r["repo"]: r
        for r in load_json(REPOS_FILE)
    }

    issues = load_json(ISSUES_FILE)

    queue = []

    for repo_name, issue in issues.items():

        if issue["issue_status"] != "NOT_CONTACTED":
            continue

        repo = repos.get(repo_name)

        if not repo:
            continue

        if repo.get("status") != "OLD_ONLY":
            continue

        stars = repo.get("stars") or 0
        forks = repo.get("forks") or 0

        impact = stars + forks

        score = (
            priority_score(
                issue.get("priority")
            )
            +
            impact
        )

        queue.append({
            "repo": repo_name,
            "priority": issue.get("priority"),
            "impact": impact,
            "score": score,
            "stars": stars,
            "forks": forks
        })

    queue.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    print("\n=== OUTREACH QUEUE ===\n")

    for i, repo in enumerate(queue[:25], start=1):

        print(
            f"{i}. {repo['repo']}\n"
            f"   Priority: {repo['priority']}\n"
            f"   Impact: {repo['impact']}\n"
            f"   Stars: {repo['stars']}\n"
            f"   Forks: {repo['forks']}\n"
        )


if __name__ == "__main__":
    main()