from datetime import datetime, timezone

from src.server_models import ServerHardware
from src.server_diagnostics import diagnose_server


def repair_and_retest(
    server: ServerHardware,
    repairs: dict,
    repair_notes: str
) -> dict:
    """
    Simulate server repairs and record diagnostic results
    before and after the repair.
    """

    initial_result = diagnose_server(server)

    if not repair_notes.strip():
        raise ValueError("Repair notes cannot be empty.")

    if not repairs:
        raise ValueError("At least one repair change is required.")

    # Validate the repaired server using Pydantic.
    repaired_data = server.model_dump()
    repaired_data.update(repairs)

    repaired_server = ServerHardware.model_validate(repaired_data)

    final_result = diagnose_server(repaired_server)

    return {
        "rack_id": server.rack_id,
        "repair_timestamp": datetime.now(timezone.utc).isoformat(),
        "repair_notes": repair_notes,
        "changes": repairs,
        "initial_diagnostic": initial_result,
        "final_diagnostic": final_result,
        "repair_successful": (
            initial_result["status"] == "FAIL"
            and final_result["status"] == "PASS"
        )
    }