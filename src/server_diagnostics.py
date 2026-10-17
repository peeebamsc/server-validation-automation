import json
from pathlib import Path

from src.server_models import ServerHardware


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "settings.json"


def load_thresholds() -> dict:
    """Load diagnostic thresholds from the JSON configuration."""

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        settings = json.load(file)

    return settings["diagnostic_thresholds"]


def diagnose_server(server: ServerHardware) -> dict:
    """Evaluate simulated server health and classify failures."""

    thresholds = load_thresholds()
    failures = []

    if server.cpu_temperature > thresholds["max_cpu_temperature_celsius"]:
        failures.append({
            "component": "CPU",
            "severity": "CRITICAL",
            "message": "CPU temperature exceeded threshold"
        })

    if server.memory_utilization > thresholds["max_memory_utilization_percent"]:
        failures.append({
            "component": "MEMORY",
            "severity": "WARNING",
            "message": "Memory utilization exceeded threshold"
        })

    if server.disk_temperature > thresholds["max_disk_temperature_celsius"]:
        failures.append({
            "component": "DISK",
            "severity": "WARNING",
            "message": "Disk temperature exceeded threshold"
        })

    if not server.disk_healthy:
        failures.append({
            "component": "DISK",
            "severity": "CRITICAL",
            "message": "Disk health check failed"
        })

    if not server.power_supply_healthy:
        failures.append({
            "component": "POWER",
            "severity": "CRITICAL",
            "message": "Power supply health check failed"
        })

    if not server.network_connected:
        failures.append({
            "component": "NETWORK",
            "severity": "WARNING",
            "message": "Network connectivity check failed"
        })

    if any(failure["severity"] == "CRITICAL" for failure in failures):
        overall_severity = "CRITICAL"
    elif failures:
        overall_severity = "WARNING"
    else:
        overall_severity = "HEALTHY"

    return {
        "rack_id": server.rack_id,
        "server_model": server.server_model,
        "status": "FAIL" if failures else "PASS",
        "severity": overall_severity,
        "failure_count": len(failures),
        "failures": failures
    }