import json
from datetime import datetime, timezone
from pathlib import Path

from src.server_models import ServerHardware
from src.server_diagnostics import diagnose_server


PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"


def generate_report(servers: list[ServerHardware]) -> dict:
    """Generate a diagnostic report for simulated servers."""

    results = [diagnose_server(server) for server in servers]

    passed = sum(result["status"] == "PASS" for result in results)
    failed = sum(result["status"] == "FAIL" for result in results)

    return {
        "report_name": "Server Hardware Validation Report",
        "environment": "SIMULATION",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total_servers": len(results),
            "passed": passed,
            "failed": failed
        },
        "results": results
    }


def save_report(report: dict) -> Path:
    """Save a diagnostic report as a JSON file."""

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    report_path = REPORTS_DIR / "diagnostic_report.json"

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    return report_path