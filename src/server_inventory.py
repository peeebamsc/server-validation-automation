from src.server_models import ServerHardware


def create_simulated_servers() -> list[ServerHardware]:
    """Create synthetic server inventory for development and testing."""

    return [
        ServerHardware(
            rack_id="LAB-RACK-001",
            server_model="SIMULATED-X86",
            cpu_temperature=65,
            memory_utilization=55,
            disk_temperature=40,
            disk_healthy=True,
            power_supply_healthy=True,
            network_connected=True,
        ),
        ServerHardware(
            rack_id="LAB-RACK-002",
            server_model="SIMULATED-X86",
            cpu_temperature=95,
            memory_utilization=55,
            disk_temperature=40,
            disk_healthy=False,
            power_supply_healthy=False,
            network_connected=True,
        ),
        ServerHardware(
            rack_id="LAB-RACK-003",
            server_model="SIMULATED-X86",
            cpu_temperature=70,
            memory_utilization=95,
            disk_temperature=75,
            disk_healthy=True,
            power_supply_healthy=True,
            network_connected=False,
        ),
    ]