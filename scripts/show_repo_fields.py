import json

with open("data/repos.json", "r", encoding="utf-8") as f:
    repos = json.load(f)

repo = repos[0]

print(json.dumps(repo, indent=2))
