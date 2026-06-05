import json
from collections import Counter
from pathlib import Path
from glob import glob
from datetime import datetime, UTC
from common import priority_score

REPOS_FILE = "data/repos_classified.json"
ISSUES_FILE = "data/issues.json"
SNAPSHOT_DIR = "data/snapshots"
OUTPUT_FILE = "data/dashboard.html"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_snapshots():

    snapshots = []

    for path in sorted(glob(f"{SNAPSHOT_DIR}/snapshot_*.json")):

        try:
            data = load_json(path)

            counts = Counter(
                r.get("status", "UNKNOWN")
                for r in data
            )

            snapshots.append({
                "file": Path(path).name,
                "OLD_ONLY": counts.get("OLD_ONLY", 0),
                "OLD_AND_NEW": counts.get("OLD_AND_NEW", 0),
                "NEW_ONLY": counts.get("NEW_ONLY", 0),
                "UNKNOWN": counts.get("UNKNOWN", 0)
            })

        except Exception:
            pass

    return snapshots


def build_summary(repos):

    counts = Counter(
        r.get("status", "UNKNOWN")
        for r in repos
    )

    total = len(repos)

    return total, counts


def build_campaign_stats(repos, issues):

    issue_counts = Counter()
    priority_counts = Counter()

    for repo in repos:

        if repo.get("status") != "OLD_ONLY":
            continue

        issue = issues.get(
            repo["repo"]
        )

        if not issue:
            continue

        issue_counts[
            issue.get(
                "issue_status",
                "NOT_CONTACTED"
            )
        ] += 1

        priority_counts[
            issue.get(
                "priority",
                "NORMAL"
            )
        ] += 1

    return (
        issue_counts,
        priority_counts
    )


def build_reach(repos):

    total_stars = 0
    total_forks = 0

    affected_stars = 0
    affected_forks = 0

    for repo in repos:

        stars = repo.get("stars") or 0
        forks = repo.get("forks") or 0

        total_stars += stars
        total_forks += forks

        if repo.get("status") == "OLD_ONLY":

            affected_stars += stars
            affected_forks += forks

    return (
        total_stars,
        total_forks,
        affected_stars,
        affected_forks
    )


def build_targets(repos, issues):

    candidates = []

    for repo in repos:

        if repo.get("status") != "OLD_ONLY":
            continue

        repo_name = repo["repo"]

        issue = issues.get(repo_name)

        if not issue:
            continue

        if issue.get("issue_status") != "NOT_CONTACTED":
            continue

        stars = repo.get("stars", 0) or 0
        forks = repo.get("forks", 0) or 0

        candidates.append({
            "repo": repo_name,
            "priority": issue.get(
                "priority",
                "NORMAL"
            ),
            "stars": stars,
            "forks": forks,
            "impact": stars + forks,
            "owner_type": repo.get(
                "owner_type",
                ""
            )
        })

    candidates.sort(
        key=lambda r:
            priority_score(r["priority"])
            + r["impact"],
        reverse=True
    )

    return candidates


def main():

    repos = load_json(REPOS_FILE)
    issues = load_json(ISSUES_FILE)

    snapshots = load_snapshots()

    total, counts = build_summary(repos)

    issue_counts, priority_counts = (
        build_campaign_stats(repos, issues)
    )

    (
        total_stars,
        total_forks,
        affected_stars,
        affected_forks
    ) = build_reach(repos)

    targets = build_targets(
        repos,
        issues
    )

    migrating = [
        r for r in repos
        if r["status"] == "OLD_AND_NEW"
    ]

    completed = [
        r for r in repos
        if r["status"] == "NEW_ONLY"
    ]

    progress = (
        (
            counts.get(
                "OLD_AND_NEW",
                0
            )
            +
            counts.get(
                "NEW_ONLY",
                0
            )
        )
        / total * 100
    ) if total else 0

    generated_at = (
        datetime.now(UTC)
        .strftime("%Y-%m-%d %H:%M UTC")
    )

    html = f"""
<html>
<head>
<title>ICANN Root CA Migration Dashboard</title>

<style>

body {{
    font-family: Arial, sans-serif;
    margin: 40px;
    background: #f4f6f8;
}}

.card {{
    background: white;
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th, td {{
    border: 1px solid #ddd;
    padding: 8px;
}}

th {{
    background: #f0f0f0;
}}

.metric {{
    font-size: 28px;
    font-weight: bold;
}}

.high {{
    color: #c0392b;
}}

.normal {{
    color: #e67e22;
}}

.low {{
    color: #27ae60;
}}

</style>
</head>

<body>

<div class="card">
<h1>ICANN Root CA Migration Dashboard</h1>
<p>Repositories scanned:</p>
<p class="metric">{total}</p>
</div>

<div class="card">
<h2>Repository Status</h2>

<ul>
<li>OLD_ONLY: {counts.get('OLD_ONLY',0)}</li>
<li>OLD_AND_NEW: {counts.get('OLD_AND_NEW',0)}</li>
<li>NEW_ONLY: {counts.get('NEW_ONLY',0)}</li>
<li>UNKNOWN: {counts.get('UNKNOWN',0)}</li>
</ul>

</div>

<div class="card">
<h2>Campaign Status</h2>

<ul>
<li>NOT_CONTACTED: {issue_counts.get('NOT_CONTACTED',0)}</li>
<li>ISSUE_OPEN: {issue_counts.get('ISSUE_OPEN',0)}</li>
<li>ISSUE_CLOSED: {issue_counts.get('ISSUE_CLOSED',0)}</li>
<li>FIX_MERGED: {issue_counts.get('FIX_MERGED',0)}</li>
</ul>

</div>

<div class="card">
<h2>Priority Breakdown</h2>

<ul>
<li>HIGH: {priority_counts.get('HIGH',0)}</li>
<li>NORMAL: {priority_counts.get('NORMAL',0)}</li>
<li>LOW: {priority_counts.get('LOW',0)}</li>
</ul>

</div>

<div class="card">
<h2>Ecosystem Reach</h2>

<ul>
<li>Total Stars: {total_stars:,}</li>
<li>Total Forks: {total_forks:,}</li>
<li>Affected Stars: {affected_stars:,}</li>
<li>Affected Forks: {affected_forks:,}</li>
</ul>

</div>

<div class="card">
<h2>Migration Progress</h2>

<p class="metric">{progress:.2f}%</p>

</div>

<div class="card">
<h2>Trend History</h2>

<table>

<tr>
<th>Snapshot</th>
<th>OLD_ONLY</th>
<th>OLD_AND_NEW</th>
<th>NEW_ONLY</th>
</tr>
"""

    for snapshot in snapshots:

        html += f"""
<tr>
<td>{snapshot['file']}</td>
<td>{snapshot['OLD_ONLY']}</td>
<td>{snapshot['OLD_AND_NEW']}</td>
<td>{snapshot['NEW_ONLY']}</td>
</tr>
"""

    html += """
</table>
</div>

<div class="card">
<h2>Top Outreach Targets</h2>

<table>

<tr>
<th>Priority</th>
<th>Repository</th>
<th>Stars</th>
<th>Forks</th>
<th>Impact</th>
<th>Owner</th>
</tr>
"""

    for repo in targets[:25]:

        html += f"""
<tr>
<td>{repo['priority']}</td>
<td>{repo['repo']}</td>
<td>{repo['stars']}</td>
<td>{repo['forks']}</td>
<td>{repo['impact']}</td>
<td>{repo['owner_type']}</td>
</tr>
"""

    html += """
</table>
</div>

<div class="card">
<h2>Repositories Already Migrating</h2>
<ul>
"""

    for repo in migrating:

        html += f"<li>{repo['repo']}</li>"

    html += """
</ul>
</div>

<div class="card">
<h2>Completed Repositories</h2>
<ul>
"""

    for repo in completed:

        html += f"<li>{repo['repo']}</li>"

    html += f"""
</ul>
</div>

<div class="card">
<h2>Dashboard Metadata</h2>
<ul>
<li>Generated: {generated_at}</li>
<li>Snapshots: {len(snapshots)}</li>
<li>Repositories: {total}</li>
</ul>
</div>

</body>
</html>
"""

    Path("data").mkdir(exist_ok=True)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)

    print(
        f"Dashboard generated: "
        f"{OUTPUT_FILE}"
)

if __name__ == "__main__":
    main()