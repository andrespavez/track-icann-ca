import json
from datetime import datetime, UTC
from pathlib import Path

INPUT_FILE = "data/repos_classified.json"
SNAPSHOT_DIR = "data/snapshots"


def main():

    Path(SNAPSHOT_DIR).mkdir(exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    timestamp = datetime.now(UTC).strftime("%Y-%m-%d_%H-%M-%S")

    output_path = f"{SNAPSHOT_DIR}/snapshot_{timestamp}.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"\nSaved snapshot: {output_path}")


if __name__ == "__main__":
    main()