import json
import sys

REPOS_FILE = "data/repos_classified.json"


def load_repos():
    with open(
        REPOS_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def find_repo(repos, repo_name):

    for repo in repos:

        if repo["repo"] == repo_name:
            return repo

    return None


def main():

    if len(sys.argv) != 2:

        print(
            "Usage:\n"
            "python scripts/generate_issue.py "
            "<repo>"
        )
        return

    repo_name = sys.argv[1]

    repos = load_repos()

    repo = find_repo(
        repos,
        repo_name
    )

    if not repo:

        print(
            f"Repository not found: "
            f"{repo_name}"
        )
        return

    if repo["status"] != "OLD_ONLY":

        print( 
            f"Repository status is " 
            f"{repo['status']}. " 
            f"No outreach issue needed." 
        ) 
        return

    print(
        "# ICANN DNSSEC Trust Anchor Certificate Update\n"
    )

    print(
        "Hello maintainers,\n"
    )

    print(
        "IANA has published a new Certificate Authority (CA) "
        "certificate used to validate the authenticity of the "
        "DNS root zone trust anchors file (`root-anchors.xml`).\n"
    )   

    print(
        "The updated certificate bundle is available at:\n"
    )
    
    print( 
        "https://data.iana.org/root-anchors/icannbundle.pem\n" 
    ) 
    
    print(
        "The bundle currently contains both the existing "
        "certificate and the replacement certificate. "
        "Signatures chaining to the new certificate are "
        "expected to be published in 2028, at which point "
        "relying parties will need to validate using the "
        "new certificate.\n"
    ) 
    
    print( 
        "Affected file(s):\n" 
    )

    for file_info in repo.get("files", []):

        print(
            f"* {file_info['path']}"
        )

    print()

    print(
        "Please review whether the trust anchor validation "
        "material in this repository should be updated to "
        "include the current contents of `icannbundle.pem`.\n"
    )

    print( 
        "Considerations for updating the trust anchor "
        "are described in RFC 9718, "
        "*DNSSEC Trust Anchor Publication for the Root Zone*.\n"
    )

    print(
        "Thank you."
    )


if __name__ == "__main__":
    main()