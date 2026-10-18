import logging
import time

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field, field_validator

from src.logging_config import configure_logging
from src.server_inventory import create_simulated_servers
from src.server_models import ServerHardware
from src.server_diagnostics import diagnose_server
from src.repair_workflow import repair_and_retest
from src.repair_history import save_repair_record, load_repair_history


# --------------------------------------------------
# Application Configuration
# --------------------------------------------------

app = FastAPI(
    title="RACK//OPS API",
    description="Server validation, diagnostics, and repair automation API.",
    version="2.0.0-dev",
)

configure_logging()
logger = logging.getLogger("rack_ops.api")


# --------------------------------------------------
# HTTP Request Logging
# --------------------------------------------------

@app.middleware("http")
async def log_http_requests(request: Request, call_next):
    start_time = time.perf_counter()

    try:
        response = await call_next(request)

        duration_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2,
        )

        logger.info(
            "HTTP request completed",
            extra={
                "event": "http_request",
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            },
        )

        return response

    except Exception:
        logger.exception(
            "HTTP request failed",
            extra={
                "event": "http_request_failed",
                "method": request.method,
                "path": request.url.path,
            },
        )
        raise


# --------------------------------------------------
# Request Validation
# --------------------------------------------------

class RepairRequest(BaseModel):
    rack_id: str = Field(min_length=1)
    repairs: dict = Field(min_length=1)
    repair_notes: str = Field(min_length=1)

    @field_validator("repairs")
    @classmethod
    def validate_repairs(cls, repairs: dict) -> dict:
        allowed_fields = {
            "cpu_temperature",
            "memory_utilization",
            "disk_temperature",
            "disk_healthy",
            "power_supply_healthy",
            "network_connected",
        }

        invalid_fields = set(repairs) - allowed_fields

        if invalid_fields:
            raise ValueError(
                f"Unsupported repair fields: {sorted(invalid_fields)}"
            )

        return repairs


# --------------------------------------------------
# Shared Server Lookup
# --------------------------------------------------

def find_server(rack_id: str) -> ServerHardware:
    """Find a simulated server or return HTTP 404."""

    for server in create_simulated_servers():
        if server.rack_id == rack_id:
            return server

    raise HTTPException(
        status_code=404,
        detail=f"Server '{rack_id}' not found",
    )


# --------------------------------------------------
# Health Endpoint
# --------------------------------------------------

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "rack-ops-api",
    }


# --------------------------------------------------
# Server Inventory Endpoints
# --------------------------------------------------

@app.get(
    "/api/v1/servers",
    response_model=list[ServerHardware],
    tags=["Servers"],
)
def get_servers():
    return create_simulated_servers()


@app.get(
    "/api/v1/servers/{rack_id}",
    response_model=ServerHardware,
    tags=["Servers"],
)
def get_server(rack_id: str):
    return find_server(rack_id)


# --------------------------------------------------
# Diagnostic Endpoint + Structured Logging
# --------------------------------------------------

@app.get(
    "/api/v1/diagnostics/{rack_id}",
    tags=["Diagnostics"],
)
def get_server_diagnostics(rack_id: str):
    server = find_server(rack_id)
    result = diagnose_server(server)

    logger.info(
        "Server diagnostic completed",
        extra={
            "event": "diagnostic_completed",
            "rack_id": rack_id,
            "severity": result["severity"],
            "status": result["status"],
        },
    )

    return result


# --------------------------------------------------
# Repair Endpoint + Structured Logging
# --------------------------------------------------

@app.post(
    "/api/v1/repairs",
    tags=["Repairs"],
)
def create_repair(request: RepairRequest):
    """Simulate a repair, retest, and save its history."""

    server = find_server(request.rack_id)

    logger.info(
        "Simulated server repair started",
        extra={
            "event": "repair_started",
            "rack_id": request.rack_id,
        },
    )

    try:
        record = repair_and_retest(
            server=server,
            repairs=request.repairs,
            repair_notes=request.repair_notes,
        )

    except ValueError as error:
        logger.warning(
            "Simulated server repair rejected",
            extra={
                "event": "repair_rejected",
                "rack_id": request.rack_id,
            },
        )

        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    save_repair_record(record)

    logger.info(
        "Simulated server repair completed",
        extra={
            "event": "repair_completed",
            "rack_id": request.rack_id,
            "status": record["final_diagnostic"]["status"],
            "severity": record["final_diagnostic"]["severity"],
        },
    )

    return record


# --------------------------------------------------
# Repair History Endpoint
# --------------------------------------------------

@app.get(
    "/api/v1/repairs/history",
    tags=["Repairs"],
)
def get_repair_history():
    return load_repair_history()
