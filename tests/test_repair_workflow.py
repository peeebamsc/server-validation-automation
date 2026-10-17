import pytest
from pydantic import ValidationError

from src.server_models import ServerHardware
from src.repair_workflow import repair_and_retest


@pytest.fixture
def failed_server():
    """Create a simulated server with three hardware failures."""

    return ServerHardware(
        rack_id="LAB-RACK-002",
        server_model="SIMULATED-X86",
        cpu_temperature=95,
        memory_utilization=55,
        disk_temperature=40,
        disk_healthy=False,
        power_supply_healthy=False,
        network_connected=True
    )


def test_successful_repair(failed_server):
    """Verify that repairing all failures produces a PASS."""

    repairs = {
        "cpu_temperature": 65,
        "disk_healthy": True,
        "power_supply_healthy": True
    }

    result = repair_and_retest(
        server=failed_server,
        repairs=repairs,
        repair_notes="Simulated cooling, disk, and PSU repairs."
    )

    assert result["initial_diagnostic"]["status"] == "FAIL"
    assert result["initial_diagnostic"]["failure_count"] == 3

    assert result["final_diagnostic"]["status"] == "PASS"
    assert result["final_diagnostic"]["failure_count"] == 0

    assert result["repair_successful"] is True


def test_incomplete_repair(failed_server):
    """Verify that unresolved failures produce a FAIL."""

    repairs = {
        "cpu_temperature": 65
    }

    result = repair_and_retest(
        server=failed_server,
        repairs=repairs,
        repair_notes="Simulated CPU cooling repair only."
    )

    assert result["initial_diagnostic"]["status"] == "FAIL"
    assert result["final_diagnostic"]["status"] == "FAIL"

    assert result["final_diagnostic"]["failure_count"] == 2
    assert result["repair_successful"] is False


def test_empty_repair_notes(failed_server):
    """Verify that repair notes are required."""

    with pytest.raises(ValueError, match="Repair notes cannot be empty"):
        repair_and_retest(
            server=failed_server,
            repairs={"cpu_temperature": 65},
            repair_notes=""
        )


def test_empty_repair_changes(failed_server):
    """Verify that at least one repair change is required."""

    with pytest.raises(ValueError, match="At least one repair change"):
        repair_and_retest(
            server=failed_server,
            repairs={},
            repair_notes="No changes provided."
        )


def test_invalid_repair_value(failed_server):
    """Verify that invalid hardware values are rejected."""

    with pytest.raises(ValidationError):
        repair_and_retest(
            server=failed_server,
            repairs={"cpu_temperature": 200},
            repair_notes="Simulated invalid temperature reading."
        )


def test_repair_preserves_original_server(failed_server):
    """Verify that the original server data remains unchanged."""

    repair_and_retest(
        server=failed_server,
        repairs={"cpu_temperature": 65},
        repair_notes="Simulated CPU cooling repair."
    )

    assert failed_server.cpu_temperature == 95
    assert failed_server.disk_healthy is False
    assert failed_server.power_supply_healthy is False


def test_repair_record_contains_history(failed_server):
    """Verify that initial and final diagnostics are recorded."""

    repairs = {
        "cpu_temperature": 65,
        "disk_healthy": True,
        "power_supply_healthy": True
    }

    result = repair_and_retest(
        server=failed_server,
        repairs=repairs,
        repair_notes="Simulated hardware repair completed."
    )

    assert result["rack_id"] == "LAB-RACK-002"
    assert result["repair_notes"] == "Simulated hardware repair completed."
    assert result["changes"] == repairs

    assert "repair_timestamp" in result
    assert "initial_diagnostic" in result
    assert "final_diagnostic" in result