import json
import os
import requests
from pathlib import Path

CONFIG_FILE = "data/config.json"
INPUT_FILE = "data/repos.json"
OUTPUT_FILE = "data/repos_classified.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def fetch_raw_file(repo, path):
    """
    Fetch file content from GitHub raw endpoint
    """
    url = f"https://raw.githubusercontent.com/{repo}/HEAD/{path}"

    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return None
        return r.text
    except Exception:
        return None


def detect(content, marker):
    """
    Simple substring match
    """
    if not content:
        return False
    return marker in content


def main():

    config = load_json(CONFIG_FILE)
    repos = load_json(INPUT_FILE)

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN environment variable not set")

    # (Not strictly required for raw.githubusercontent, but kept for future expansion)
    headers = {
        "Authorization": f"Bearer {token}"
    }

    old_marker = config["old_root"]["search_strings"][0]
    new_marker = config["new_root"]["search_strings"][0]

    print("\nStarting classification...\n")

    for repo in repos:

        repo_name = repo["repo"]

        has_old = False
        has_new = False

        # check all discovered file locations
        for f in repo.get("files", []):

            content = fetch_raw_file(repo_name, f["path"])

            if detect(content, old_marker):
                has_old = True

            if detect(content, new_marker):
                has_new = True

            # early exit if both found
            if has_old and has_new:
                break

        # classify
        if has_old and has_new:
            status = "OLD_AND_NEW"
        elif has_old and not has_new:
            status = "OLD_ONLY"
        elif not has_old and has_new:
            status = "NEW_ONLY"
        else:
            status = "UNKNOWN"

        repo["status"] = status
        repo["contains_old_root"] = has_old
        repo["contains_new_root"] = has_new

        repo["impact_score"] = (
            (repo.get("stars") or 0)
            +
            (repo.get("forks") or 0)
        )           

        print(f"{repo_name}: {status}")

    Path("data").mkdir(exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(repos, f, indent=2)

    print(f"\nSaved classified results to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()