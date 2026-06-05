import json
from datetime import datetime, timezone

ISSUES_FILE = "data/issues.json"
REPOS_FILE = "data/repos_classified.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def is_recent(updated_at):

    if not updated_at:
        return False

    try:
        dt = datetime.fromisoformat(
            updated_at.replace("Z", "+00:00")
        )

        age_days = (
            datetime.now(timezone.utc) - dt
        ).days

        return age_days <= 365

    except Exception:
        return False


def calculate_priority(repo):

    score = 0

    if repo.get("owner_type") == "Organization":
        score += 30

    if not repo.get("fork", False):
        score += 20

    if not repo.get("archived", False):
        score += 20

    if is_recent(repo.get("updated_at")):
        score += 20

    stars = repo.get("stars") or 0
    forks = repo.get("forks") or 0

    score += min(stars // 100, 50)
    score += min(forks // 50, 30)

    #
    # DNSSEC / Trust Anchor ecosystem boost
    #
    repo_name = repo["repo"].lower()

    critical_keywords = [
        "dnssec",
        "trust-anchor",
        "trust_anchor",
        "unbound",
        "iana",
        "icann",
        "freebsd",
        "openbsd",
        "libreswan",
        "dns",
        "icannbundle"
    ]

    if any(keyword in repo_name for keyword in critical_keywords):
        score += 40

    if score >= 80:
        print(
            f"{repo['repo']}: "
            f"score={score}"
        )
        return "HIGH"

    if score >= 40:
        return "NORMAL"

    return "LOW"


def main():

    issues = load_json(ISSUES_FILE)

    repos = {
        repo["repo"]: repo
        for repo in load_json(REPOS_FILE)
    }

    updated = 0

    for repo_name, issue in issues.items():

        repo = repos.get(repo_name)

        if not repo:
            continue

        #
        # Manual priorities always win
        #
        if issue.get("priority") in [
            "HIGH",
            "NORMAL",
            "LOW"
        ]:
            continue

        issue["priority"] = calculate_priority(repo)

        updated += 1

    save_json(ISSUES_FILE, issues)

    print(
        f"Updated priority "
        f"for {updated} repositories"
    )


if __name__ == "__main__":
    main()