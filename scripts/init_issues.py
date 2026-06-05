import json
from pathlib import Path

REPOS_FILE = "data/repos_classified.json"
ISSUES_FILE = "data/issues.json"


def load_repos():
    with open(REPOS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def main():

    repos = load_repos()

    issue_db = {}

    try:

        with open(
            ISSUES_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            issue_db = json.load(f)

    
    except FileNotFoundError:

        issue_db = {}
    
    existing_repos = set(issue_db.keys())
    current_repos = {
        repo["repo"]
        for repo in repos
        }

    added = 0
    preserved = 0

    new_issue_db = {}

    for repo in repos:

        repo_name = repo["repo"]

        if repo_name in issue_db:

            new_issue_db[repo_name] = issue_db[repo_name]
            preserved += 1

        else:

            new_issue_db[repo_name] = {
                "issue_status": "NOT_CONTACTED",
                "issue_url": None,
                "priority": "NORMAL",
                "notes": ""
            }

            added += 1        
    
    removed = len(
        existing_repos - current_repos
    )
    
    Path("data").mkdir(
        exist_ok=True
    )

    with open(
        ISSUES_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            new_issue_db,
            f,
            indent=2
        )

    print(
        f"Updated {ISSUES_FILE}"
    )

    print(
        f"Added: {added}"
    )

    print(
        f"Removed: {removed}"
    )

    print(
        f"Preserved: {preserved}"
    )

if __name__ == "__main__":
    main()