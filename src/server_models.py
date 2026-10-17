from pydantic import BaseModel, Field


class ServerHardware(BaseModel):
    """
    Represents a simulated enterprise server
    and its hardware health metrics.
    """

    rack_id: str = Field(min_length=1)
    server_model: str = Field(min_length=1)

    cpu_temperature: float = Field(ge=0, le=150)
    memory_utilization: float = Field(ge=0, le=100)
    disk_temperature: float = Field(ge=0, le=120)

    disk_healthy: bool
    power_supply_healthy: bool
    network_connected: bool