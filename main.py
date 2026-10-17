from rich.console import Console
from rich.table import Table

from src.server_models import ServerHardware
from src.report_generator import generate_report, save_report


console = Console()


def main():
    servers = [
        ServerHardware(
            rack_id="LAB-RACK-001",
            server_model="SIMULATED-X86",
            cpu_temperature=65,
            memory_utilization=55,
            disk_temperature=40,
            disk_healthy=True,
            power_supply_healthy=True,
            network_connected=True
        ),
        ServerHardware(
            rack_id="LAB-RACK-002",
            server_model="SIMULATED-X86",
            cpu_temperature=95,
            memory_utilization=75,
            disk_temperature=45,
            disk_healthy=False,
            power_supply_healthy=False,
            network_connected=True
        ),
        ServerHardware(
            rack_id="LAB-RACK-003",
            server_model="SIMULATED-X86",
            cpu_temperature=70,
            memory_utilization=95,
            disk_temperature=75,
            disk_healthy=True,
            power_supply_healthy=True,
            network_connected=False
        )
    ]

    report = generate_report(servers)
    report_path = save_report(report)

    table = Table(title="Server Hardware Validation Results")

    table.add_column("Rack ID")
    table.add_column("Status")
    table.add_column("Severity")
    table.add_column("Failures")

    for result in report["results"]:
        table.add_row(
            result["rack_id"],
            result["status"],
            result["severity"],
            str(result["failure_count"])
        )

    console.print(table)

    summary = report["summary"]

    console.print(
        f"\nTotal Servers: {summary['total_servers']}"
        f"\nPassed: {summary['passed']}"
        f"\nFailed: {summary['failed']}"
    )

    console.print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()