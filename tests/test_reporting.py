import json
from datetime import datetime

from src.server_models import ServerHardware
from src.report_generator import generate_report, save_report


def create_server(rack_id, cpu_temperature=65):
    """Create synthetic server hardware for testing."""

    return ServerHardware(
        rack_id=rack_id,
        server_model="SIMULATED-X86",
        cpu_temperature=cpu_temperature,
        memory_utilization=55,
        disk_temperature=40,
        disk_healthy=True,
        power_supply_healthy=True,
        network_connected=True
    )


def test_report_summary():
    """Verify total, passed, and failed server counts."""

    servers = [
        create_server("TEST-001"),
        create_server("TEST-002", cpu_temperature=95),
        create_server("TEST-003")
    ]

    report = generate_report(servers)

    assert report["summary"]["total_servers"] == 3
    assert report["summary"]["passed"] == 2
    assert report["summary"]["failed"] == 1


def test_report_contains_server_results():
    """Verify every server appears in the report."""

    servers = [
        create_server("TEST-001"),
        create_server("TEST-002")
    ]

    report = generate_report(servers)

    assert len(report["results"]) == 2
    assert report["results"][0]["rack_id"] == "TEST-001"
    assert report["results"][1]["rack_id"] == "TEST-002"


def test_report_timestamp():
    """Verify the report contains a valid UTC timestamp."""

    report = generate_report([create_server("TEST-001")])

    timestamp = datetime.fromisoformat(report["generated_at"])

    assert timestamp.tzinfo is not None


def test_empty_server_list():
    """Verify the report handles an empty server list."""

    report = generate_report([])

    assert report["summary"]["total_servers"] == 0
    assert report["summary"]["passed"] == 0
    assert report["summary"]["failed"] == 0
    assert report["results"] == []


def test_report_saved_as_json(tmp_path, monkeypatch):
    """Verify a report is saved and can be read back."""

    import src.report_generator as report_generator

    monkeypatch.setattr(report_generator, "REPORTS_DIR", tmp_path)

    report = generate_report([create_server("TEST-001")])

    report_path = save_report(report)

    assert report_path.exists()

    with report_path.open("r", encoding="utf-8") as file:
        saved_report = json.load(file)

    assert saved_report == report