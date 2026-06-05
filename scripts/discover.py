import json
import os
import requests
from pathlib import Path

CONFIG_FILE = "data/config.json"
OUTPUT_FILE = "data/repos.json"


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def github_search(query, headers):

    url = "https://api.github.com/search/code"

    all_items = []
    page = 1

    while True:

        response = requests.get(
            url,
            headers=headers,
            params={
                "q": query,
                "per_page": 100,
                "page": page
            }
        )

        if response.status_code != 200:
            print(response.status_code)
            print(response.text)
            break

        data = response.json()

        if page == 1:
            print(f"\nQuery: {query}")
            print(f"Total count: {data.get('total_count')}")

        items = data.get("items", [])

        if not items:
            break

        all_items.extend(items)

        print(f"page {page}: {len(items)} items")

        if len(items) < 100:
            break

        page += 1

    return all_items


def main():

    config = load_config()

    token = os.environ.get("GITHUB_TOKEN")

    if not token:
        raise RuntimeError("GITHUB_TOKEN environment variable not set")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    repos = {}

    search_sets = [
        ("old_root", config["old_root"]["search_strings"]),
        ("new_root", config["new_root"]["search_strings"])
    ]

    for root_type, search_strings in search_sets:

        for search_string in search_strings:

            print(f"\nSearching: {search_string}")

            items = github_search(search_string, headers)

            for item in items:

                repo_name = item["repository"]["full_name"]

                if repo_name not in repos:

                    print(f"Fetching metadata: {repo_name}")

                    metadata_response = requests.get(
                        f"https://api.github.com/repos/{repo_name}",
                        headers=headers
                    )

                    if metadata_response.status_code == 200:
                        metadata = metadata_response.json()
                    else:
                        print(
                            f"Warning: failed metadata lookup "
                            f"for {repo_name}"
                        )
                        metadata = {}

                    repos[repo_name] = {
                        "repo": repo_name,

                        "description": metadata.get("description"),

                        "html_url": metadata.get("html_url"),

                        "stars": metadata.get("stargazers_count"),

                        "forks": metadata.get("forks_count"),

                        "watchers": metadata.get("subscribers_count"),

                        "archived": metadata.get("archived"),

                        "updated_at": metadata.get("updated_at"),

                        "pushed_at": metadata.get("pushed_at"),

                        "open_issues": metadata.get("open_issues_count"),

                        "default_branch": metadata.get("default_branch"),

                        "fork": metadata.get("fork"),

                        "owner_type": metadata.get(
                            "owner",
                            {}
                        ).get("type"),

                        "matches": [],

                        "files": set(),

                        "issue_url": None,

                        "issue_state": None,

                        "contains_old_root": False,

                        "contains_new_root": False,

                        "status": "discovered"
                    }

                repos[repo_name]["matches"].append({
                    "root": root_type,
                    "search": search_string
                })

                repos[repo_name]["files"].add(
                    (item["path"], item["html_url"])
                )

                if root_type == "old_root":
                    repos[repo_name]["contains_old_root"] = True

                if root_type == "new_root":
                    repos[repo_name]["contains_new_root"] = True

    Path("data").mkdir(exist_ok=True)

    # convert sets -> JSON serializable lists
    for repo in repos.values():
        repo["files"] = [
            {"path": p, "html_url": u}
            for (p, u) in repo["files"]
        ]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(list(repos.values()), f, indent=2)

    print(f"\nSaved {len(repos)} repositories to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()