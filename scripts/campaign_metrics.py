import json

ISSUES_FILE = "data/issues.json"
REPOS_FILE = "data/repos_classified.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():

    repos = load_json(REPOS_FILE)
    issues = load_json(ISSUES_FILE)

    campaign_repos = [
        r for r in repos
        if r.get("status") == "OLD_ONLY"
    ]

    already_migrated = [
        r for r in repos
        if r.get("status") == "OLD_AND_NEW"
    ]

    status_counts = {}
    priority_counts = {}
    issue_counts = {}

    for repo in repos:

        status = repo.get(
            "status",
            "UNKNOWN"
        )

        status_counts[status] = (
            status_counts.get(status, 0) + 1
        )

    for repo in campaign_repos:

        repo_name = repo["repo"]

        issue = issues.get(repo_name)

        if not issue:
            continue

        priority = issue.get(
            "priority",
            "NORMAL"
        )

        priority_counts[priority] = (
            priority_counts.get(priority, 0) + 1
        )

        state = issue.get(
            "issue_status",
            "NOT_CONTACTED"
        )

        issue_counts[state] = (
            issue_counts.get(state, 0) + 1
        )
        
    total_repositories = len(campaign_repos)
    
    campaign_size = (
        status_counts.get("OLD_ONLY", 0)
    )

    migration_started = (
        status_counts.get("OLD_AND_NEW", 0)
    )

    fully_migrated = (
        status_counts.get("NEW_ONLY", 0)
    )

    completed = (
        issue_counts.get("FIX_MERGED", 0)
        +
        issue_counts.get("NO_ACTION_NEEDED", 0)
    )

    campaign_progress = (
        completed / campaign_size * 100
        if campaign_size
        else 0
    )

    migration_progress = (
        (migration_started + fully_migrated)
        / total_repositories * 100
        if total_repositories
        else 0
    )

    print("\n=== MIGRATION STATUS ===\n")

    print(
        f"Repositories discovered: "
        f"{total_repositories}"
    )

    print(
        f"Need update (OLD_ONLY): "
        f"{campaign_size}"
    )

    print(
        f"Migration started: "
        f"{migration_started}"
    )

    print(
        f"Fully migrated: "
        f"{fully_migrated}"
    )

    print(
        f"\nMigration adoption: "
        f"{migration_progress:.1f}%"
    )

    print("\n=== OUTREACH CAMPAIGN ===\n")

    print(
        f"Campaign scope: "
        f"{campaign_size}"
    )

    print()

    for k, v in sorted(issue_counts.items()):
        print(f"{k:20} {v}")

    print()

    for k, v in sorted(priority_counts.items()):
        print(f"{k:20} {v}")

    print()

    print(
        f"Campaign progress: "
        f"{campaign_progress:.1f}%"
    )

    print("\n=== CAMPAIGN METRICS ===\n")

    print(
        f"Repositories discovered: "
        f"{len(repos)}"
    )

    print(
        f"Repositories requiring action: "
        f"{len(campaign_repos)}"
    )

    print(
        f"Already migrated: "
        f"{len(already_migrated)}"
    )

    print()    

if __name__ == "__main__":
    main()