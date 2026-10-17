import pytest

from src.server_models import ServerHardware
from src.server_diagnostics import diagnose_server


@pytest.fixture
def healthy_server():
    """Create reusable simulated server data."""

    return ServerHardware(
        rack_id="TEST-RACK-001",
        server_model="SIMULATED-X86",
        cpu_temperature=65,
        memory_utilization=55,
        disk_temperature=40,
        disk_healthy=True,
        power_supply_healthy=True,
        network_connected=True
    )


def test_healthy_server_passes(healthy_server):
    """Verify a healthy server passes validation."""

    result = diagnose_server(healthy_server)

    assert result["status"] == "PASS"
    assert result["severity"] == "HEALTHY"
    assert result["failure_count"] == 0


def test_cpu_overheating_fails(healthy_server):
    """Verify CPU overheating is detected."""

    server = healthy_server.model_copy(
        update={"cpu_temperature": 95}
    )

    result = diagnose_server(server)

    assert result["status"] == "FAIL"
    assert result["severity"] == "CRITICAL"
    assert result["failure_count"] == 1
    assert result["failures"][0]["component"] == "CPU"


def test_memory_overutilization_fails(healthy_server):
    """Verify excessive memory utilization is detected."""

    server = healthy_server.model_copy(
        update={"memory_utilization": 95}
    )

    result = diagnose_server(server)

    assert result["status"] == "FAIL"
    assert result["severity"] == "WARNING"
    assert result["failure_count"] == 1
    assert result["failures"][0]["component"] == "MEMORY"


def test_disk_failure_detected(healthy_server):
    """Verify disk health failures are detected."""

    server = healthy_server.model_copy(
        update={"disk_healthy": False}
    )

    result = diagnose_server(server)

    assert result["status"] == "FAIL"
    assert result["severity"] == "CRITICAL"
    assert result["failures"][0]["component"] == "DISK"


def test_power_supply_failure_detected(healthy_server):
    """Verify power supply failures are detected."""

    server = healthy_server.model_copy(
        update={"power_supply_healthy": False}
    )

    result = diagnose_server(server)

    assert result["status"] == "FAIL"
    assert result["severity"] == "CRITICAL"
    assert result["failures"][0]["component"] == "POWER"


def test_network_failure_detected(healthy_server):
    """Verify network connectivity failures are detected."""

    server = healthy_server.model_copy(
        update={"network_connected": False}
    )

    result = diagnose_server(server)

    assert result["status"] == "FAIL"
    assert result["severity"] == "WARNING"
    assert result["failures"][0]["component"] == "NETWORK"


def test_multiple_failures_detected(healthy_server):
    """Verify simultaneous hardware failures are classified."""

    server = healthy_server.model_copy(
        update={
            "cpu_temperature": 100,
            "disk_healthy": False,
            "power_supply_healthy": False
        }
    )

    result = diagnose_server(server)

    assert result["status"] == "FAIL"
    assert result["severity"] == "CRITICAL"
    assert result["failure_count"] == 3


def test_threshold_boundary(healthy_server):
    """Verify a value exactly at the threshold passes."""

    server = healthy_server.model_copy(
        update={
            "cpu_temperature": 85,
            "memory_utilization": 90,
            "disk_temperature": 70
        }
    )

    result = diagnose_server(server)

    assert result["status"] == "PASS"
    assert result["failure_count"] == 0