# ICANN CA Migration Tracker

## Quick Start

```bash
make scan # Daily refresh
make status # View campaign status
make dashboard
make outreach-queue # View outreach queue
python scripts/generate_issue.py owner/repo # Generate issue text
python scripts/update_issue.py owner/repo ISSUE_OPEN <issue_url>
python scripts/campaign_report.py
git add .
git commit -m "Daily scan"
git push
```

## Purpose

The ICANN CA Migration Tracker identifies GitHub repositories that contain the existing ICANN trust anchor certificate but not the newly published replacement certificate and tracks outreach efforts to repository maintainers.

The tool supports:

- Repository discovery
- Certificate classification
- Migration tracking
- Outreach campaign management
- Historical trend reporting

---

# Repository Status

Each repository is classified into one of the following states:

| Status | Description |
|----------|----------|
| OLD_ONLY | Repository contains the existing certificate but not the newly published replacement certificate. Action required. |
| OLD_AND_NEW | Repository contains both certificates. No action required. |
| NEW_ONLY | Repository contains only the new certificate. Fully migrated. |
| UNKNOWN | Unable to determine status. |

Only repositories classified as **OLD_ONLY** require outreach.

---

# Campaign Status

Each repository also has a campaign status:

| Status | Description |
|----------|----------|
| NOT_CONTACTED | No outreach performed yet. |
| CONTACTED | Outreach performed by email or Bugzilla. |
| ISSUE_OPEN | GitHub issue has been opened. |
| ISSUE_CLOSED | Issue was closed without migration. |
| FIX_MERGED | Migration completed and fix merged. |

Campaign status is tracked independently from repository status.

---

# Workflow Overview

```text
GitHub Repositories
        ↓
     discover
        ↓
     classify
        ↓
 OLD_ONLY / OLD_AND_NEW / NEW_ONLY
        ↓
 campaign_queue
        ↓
 generate_issue
        ↓
 Open GitHub Issue
        ↓
 update_issue
        ↓
 campaign_report
```

---

# Daily Workflow

## 1. Run a Scan

```bash
make scan
```

This performs:

```text
discover
  ↓
classify
  ↓
report
  ↓
action-report
  ↓
dashboard
  ↓
trend
```

Generated files:

```text
data/repos.json
data/repos_classified.json
reports/action_required.md
data/dashboard.html
```

---

## 2. Review Outreach Queue

```bash
python scripts/campaign_queue.py
```

This displays repositories that:

- Are classified as OLD_ONLY
- Have not yet been contacted
- Are grouped by priority

---

## 3. Generate an Issue

```bash
python scripts/generate_issue.py owner/repository
```

Example:

```bash
python scripts/generate_issue.py freebsd/freebsd-src
```

This generates a ready-to-paste GitHub issue.

---

## 4. Open the GitHub Issue

Create the issue manually in GitHub using the generated template.

---

## 5. Record the Outreach

```bash
python scripts/update_issue.py \
freebsd/freebsd-src \
ISSUE_OPEN \
https://github.com/freebsd/freebsd-src/issues/123
```

---

## 6. Track Campaign Progress

```bash
python scripts/campaign_report.py
```

---

## 7. Save a Historical Snapshot

```bash
make snapshot
```

Snapshots are stored in:

```text
data/snapshots/
```

These snapshots are used to generate trend reports.

---

# Priority Management

Assign repository priority:

```bash
python scripts/set_priority.py \
freebsd/freebsd-src \
HIGH
```

Priority levels:

```text
HIGH
NORMAL
LOW
```

The campaign queue uses these priorities to determine outreach order.

---

# Reporting

## Migration Summary

```bash
python scripts/report.py
```

Provides repository classification statistics.

## Campaign Report

```bash
python scripts/campaign_report.py
```

Provides outreach progress statistics.

## Trend Report

```bash
python scripts/trend.py
```

Compares historical snapshots and shows migration progress over time.

---

# Key Files

## Repository Data

### Raw Discovery Results

```text
data/repos.json
```

### Repository Classification Results

```text
data/repos_classified.json
```

## Campaign Data

### Outreach Tracking Database

```text
data/issues.json
```

Stores:

- Campaign status
- Priority
- Issue URLs
- Notes

## Reports

### Action Required Report

```text
reports/action_required.md
```

Repositories requiring action.

### Dashboard

```text
data/dashboard.html
```

HTML dashboard view.

## Historical Data

```text
data/snapshots/
```

Historical migration snapshots.

---

# Recommended Outreach Strategy

1. Prioritize HIGH priority repositories.
2. Focus on actively maintained upstream projects.
3. Generate issues using `generate_issue.py`.
4. Open issues manually.
5. Update campaign status immediately after opening an issue.
6. Periodically rerun scans and save snapshots.
7. Monitor migration progress over time.

Expected migration path:

```text
OLD_ONLY
    ↓
OLD_AND_NEW
    ↓
NEW_ONLY
```