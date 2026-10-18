import json
from pathlib import Path

from issue_tracker.schema import IssueOut

DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "issues.json"


def load_data() -> list[IssueOut]:
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            content = f.read()
            if content.strip():
                return [IssueOut(**item) for item in json.loads(content)]
    return []


def save_data(data: list[IssueOut]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump([item.model_dump() for item in data], f, indent=2)
