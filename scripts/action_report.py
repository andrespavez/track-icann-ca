import json
from datetime import datetime, UTC
from pathlib import Path

INPUT_FILE = "data/repos_classified.json"
OUTPUT_FILE = "reports/action_required.md"


def load_data():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def main():

    repos = load_data()

    old_only = sorted(
        [
            r
            for r in repos
            if r.get("status") == "OLD_ONLY"
        ],
        key=lambda r: r["repo"].lower()
    )

    Path("reports").mkdir(
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "# ICANN Root CA Migration\n\n"
        )

        f.write(
            f"Generated: "
            f"{datetime.now(UTC).isoformat()}\n\n"
        )

        f.write(
            f"## OLD_ONLY ({len(old_only)})\n\n"
        )

        for repo in old_only:

            repo_url = (
                f"https://github.com/"
                f"{repo['repo']}"
            )

            f.write(
                f"### {repo['repo']}\n\n"
            )

            f.write(
                f"Repository: {repo_url}\n\n"
            )

            f.write(
                f"Affected files: "
                f"{len(repo.get('files', []))}\n\n"
            )

            f.write(
                "Source locations:\n\n"
            )

            for file_info in repo.get(
                "files",
                []
            ):

                f.write(
                    f"- {file_info['html_url']}\n"
                )

            f.write("\n---\n\n")

    print(
        f"Created {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()