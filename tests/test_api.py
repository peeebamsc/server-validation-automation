from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "rack-ops-api",
    }


def test_get_servers():
    response = client.get("/api/v1/servers")

    assert response.status_code == 200

    servers = response.json()

    assert len(servers) == 3
    assert servers[0]["rack_id"] == "LAB-RACK-001"
    assert servers[1]["rack_id"] == "LAB-RACK-002"
    assert servers[2]["rack_id"] == "LAB-RACK-003"


def test_get_servers_contains_hardware_metrics():
    response = client.get("/api/v1/servers")

    assert response.status_code == 200

    servers = response.json()

    for server in servers:
        assert "rack_id" in server
        assert "server_model" in server
        assert "cpu_temperature" in server
        assert "memory_utilization" in server
        assert "disk_temperature" in server
        assert "disk_healthy" in server
        assert "power_supply_healthy" in server
        assert "network_connected" in server


def test_get_server_by_rack_id():
    response = client.get("/api/v1/servers/LAB-RACK-002")

    assert response.status_code == 200

    server = response.json()

    assert server["rack_id"] == "LAB-RACK-002"
    assert server["cpu_temperature"] == 95
    assert server["disk_healthy"] is False
    assert server["power_supply_healthy"] is False


def test_get_server_not_found():
    response = client.get("/api/v1/servers/LAB-RACK-999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Server 'LAB-RACK-999' not found"
    }


def test_diagnostics_healthy_server():
    response = client.get("/api/v1/diagnostics/LAB-RACK-001")

    assert response.status_code == 200

    result = response.json()

    assert result["rack_id"] == "LAB-RACK-001"
    assert result["status"] == "PASS"
    assert result["severity"] == "HEALTHY"
    assert result["failure_count"] == 0
    assert result["failures"] == []


def test_diagnostics_critical_server():
    response = client.get("/api/v1/diagnostics/LAB-RACK-002")

    assert response.status_code == 200

    result = response.json()

    assert result["rack_id"] == "LAB-RACK-002"
    assert result["status"] == "FAIL"
    assert result["severity"] == "CRITICAL"
    assert result["failure_count"] == 3

    components = [failure["component"] for failure in result["failures"]]

    assert "CPU" in components
    assert "DISK" in components
    assert "POWER" in components


def test_diagnostics_server_not_found():
    response = client.get("/api/v1/diagnostics/LAB-RACK-999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Server 'LAB-RACK-999' not found"
    }

def test_create_repair(tmp_path, monkeypatch):

    import src.api as api
    import src.repair_history as repair_history

    history_file = tmp_path / "repair_history.json"

    monkeypatch.setattr(repair_history, "HISTORY_FILE", history_file)
    monkeypatch.setattr(
        api,
        "save_repair_record",
        repair_history.save_repair_record,
    )

    response = client.post(
        "/api/v1/repairs",
        json={
            "rack_id": "LAB-RACK-002",
            "repairs": {
                "cpu_temperature": 65,
                "disk_healthy": True,
                "power_supply_healthy": True,
            },
            "repair_notes": "Simulated CPU cooling, disk, and PSU repair.",
        },
    )

    assert response.status_code == 200

    result = response.json()

    assert result["rack_id"] == "LAB-RACK-002"
    assert result["initial_diagnostic"]["status"] == "FAIL"
    assert result["final_diagnostic"]["status"] == "PASS"
    assert result["repair_successful"] is True

    assert history_file.exists()

    history_response = client.get("/api/v1/repairs/history")

    assert history_response.status_code == 200
    assert len(history_response.json()) == 1
    assert history_response.json()[0]["rack_id"] == "LAB-RACK-002"


def test_create_repair_unknown_server():
    response = client.post(
        "/api/v1/repairs",
        json={
            "rack_id": "LAB-RACK-999",
            "repairs": {"cpu_temperature": 65},
            "repair_notes": "Simulated repair.",
        },
    )

    assert response.status_code == 404


def test_create_repair_invalid_notes():
    response = client.post(
        "/api/v1/repairs",
        json={
            "rack_id": "LAB-RACK-002",
            "repairs": {"cpu_temperature": 65},
            "repair_notes": "",
        },
    )

    assert response.status_code == 422




def test_create_repair_rejects_identity_change():
    response = client.post(
        "/api/v1/repairs",
        json={
            "rack_id": "LAB-RACK-002",
            "repairs": {"rack_id": "LAB-RACK-999"},
            "repair_notes": "Testing server identity protection.",
        },
    )

    assert response.status_code == 422


def test_create_repair_rejects_unknown_field():
    response = client.post(
        "/api/v1/repairs",
        json={
            "rack_id": "LAB-RACK-002",
            "repairs": {"unknown_component": True},
            "repair_notes": "Testing unsupported repair field.",
        },
    )

    assert response.status_code == 422

    def test_create_repair_rejects_invalid_temperature():
        response = client.post(
            "/api/v1/repairs",
            json={
                "rack_id": "LAB-RACK-002",
                "repairs": {"cpu_temperature": -100},
                "repair_notes": "Testing invalid CPU temperature.",
            },
        )

        assert response.status_code == 422

def test_create_repair_rejects_invalid_temperature():
    response = client.post(
        "/api/v1/repairs",
        json={
            "rack_id": "LAB-RACK-002",
            "repairs": {"cpu_temperature": -100},
            "repair_notes": "Testing invalid CPU temperature.",
        },
    )

    assert response.status_code == 422
