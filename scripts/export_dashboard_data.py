import json
from collections import Counter
from pathlib import Path
from datetime import datetime, UTC

REPOS_FILE = "data/repos_classified.json"
ISSUES_FILE = "data/issues.json"
SNAPSHOT_DIR = "data/snapshots"
OUTPUT_FILE = "data/dashboard_data.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


repos = load_json(REPOS_FILE)
issues = load_json(ISSUES_FILE)

#
# Repository status summary
#
repo_status = Counter(
    repo.get("status", "UNKNOWN")
    for repo in repos
)

#
# Campaign status summary
#
issue_status = Counter(
    issue.get("issue_status", "NOT_CONTACTED")
    for issue in issues.values()
)

#
# Priority summary
#
priority_counts = Counter(
    issue.get("priority", "NORMAL")
    for issue in issues.values()
)

#
# Top outreach targets
#
top_targets = []

for repo in repos:

    if repo.get("status") != "OLD_ONLY":
        continue

    issue = issues.get(repo["repo"])

    if not issue:
        continue

    if issue.get("issue_status") != "NOT_CONTACTED":
        continue

    top_targets.append({
        "repo": repo["repo"],
        "priority": issue.get("priority"),
        "stars": repo.get("stars", 0) or 0,
        "forks": repo.get("forks", 0) or 0,
        "owner_type": repo.get("owner_type"),
        "impact": repo.get("impact_score", 0)
    })

priority_order = {
    "HIGH": 3,
    "NORMAL": 2,
    "LOW": 1
}

top_targets.sort(
    key=lambda x: (
        priority_order.get(
            x["priority"],
            0
        ),
        x["stars"]
    ),
    reverse=True
)

#
# High priority queue
#
high_priority = [
    t
    for t in top_targets
    if t["priority"] == "HIGH"
]

#
# Snapshot trend data
#
trend = []

snapshot_dir = Path(SNAPSHOT_DIR)

if snapshot_dir.exists():

    for file in sorted(
        snapshot_dir.glob("snapshot_*.json")
    ):

        snapshot = load_json(file)

        status_counts = Counter(
            repo.get("status", "UNKNOWN")
            for repo in snapshot
        )

        trend.append({
            "timestamp": file.stem.replace(
                "snapshot_",
                ""
            ),

            "total": len(snapshot),

            "old_only":
                status_counts.get(
                    "OLD_ONLY",
                    0
                ),

            "old_and_new":
                status_counts.get(
                    "OLD_AND_NEW",
                    0
                ),

            "new_only":
                status_counts.get(
                    "NEW_ONLY",
                    0
                ),

            "unknown":
                status_counts.get(
                    "UNKNOWN",
                    0
                )
        })

#
# Campaign progress
#
total_repos = len(repos)

completed = (
    issue_status.get(
        "FIX_MERGED",
        0
    )
    +
    repo_status.get(
        "OLD_AND_NEW",
        0
    )
    +
    repo_status.get(
        "NEW_ONLY",
        0
    )
)

progress = (
    completed / total_repos * 100
    if total_repos
    else 0
)

#
# Owner statistics
#
owners = Counter(
    repo.get(
        "owner_type",
        "Unknown"
    )
    for repo in repos
)

#
# Impact statistics
#
total_impact = sum(
    repo.get(
        "impact_score",
        0
    )
    for repo in repos
)

average_impact = (
    total_impact / len(repos)
    if repos
    else 0
)

#
# Highest impact repositories
#
high_impact = sorted(
    [
        repo
        for repo in repos
        if repo.get("status") == "OLD_ONLY"
    ],
    key=lambda r: r.get(
        "impact_score",
        0
    ),
    reverse=True
)[:25]


output = {

    "summary": {

        "total": total_repos,

        "old_only":
            repo_status.get(
                "OLD_ONLY",
                0
            ),

        "old_and_new":
            repo_status.get(
                "OLD_AND_NEW",
                0
            ),

        "new_only":
            repo_status.get(
                "NEW_ONLY",
                0
            ),

        "unknown":
            repo_status.get(
                "UNKNOWN",
                0
            )
    },

    "campaign": {
        "progress": round(
            progress,
            1
        ),
        "statuses": dict(
            issue_status
        )
    },

    "priority": dict(
        priority_counts
    ),

    "owners": dict(
        owners
    ),

    "impact": {
        "total": total_impact,
        "average": round(
            average_impact,
            1
        )
    },

    "top_targets":
        top_targets[:25],

    "high_priority":
        high_priority,

    "high_impact": [
    {
        "repo": repo["repo"],
        "impact": repo.get(
            "impact_score",
            0
        ),
        "stars": repo.get(
            "stars",
            0
        ),
        "forks": repo.get(
            "forks",
            0
        ),
        "owner_type": repo.get(
            "owner_type"
        )
    }
    for repo in high_impact
    ],

    "trend":
        trend
}

output["metadata"] = {
    "generated_at": datetime.now(UTC).isoformat(),
    "snapshot_count": len(trend)
}

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:


    json.dump(
        output,
        f,
        indent=2
    )

print(
    f"Created {OUTPUT_FILE}"
)