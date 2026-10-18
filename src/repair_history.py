import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"
HISTORY_FILE = REPORTS_DIR / "repair_history.json"


def save_repair_record(record: dict) -> Path:
    """
    Save a simulated server repair record to persistent JSON history.
    """

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    history = []

    if HISTORY_FILE.exists():
        with HISTORY_FILE.open("r", encoding="utf-8") as file:
            history = json.load(file)

        if not isinstance(history, list):
            raise ValueError("Repair history must contain a JSON list.")

    history.append(record)

    with HISTORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(history, file, indent=2)

    return HISTORY_FILE


def load_repair_history() -> list:
    """
    Load previously saved simulated repair records.
    """

    if not HISTORY_FILE.exists():
        return []

    with HISTORY_FILE.open("r", encoding="utf-8") as file:
        history = json.load(file)

    if not isinstance(history, list):
        raise ValueError("Repair history must contain a JSON list.")

    return history