import json
import logging

from src.logging_config import JSONFormatter


def test_json_formatter_produces_valid_json():
    formatter = JSONFormatter()

    record = logging.LogRecord(
        name="rack_ops.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="Diagnostic completed",
        args=(),
        exc_info=None,
    )

    record.event = "diagnostic_completed"
    record.rack_id = "LAB-RACK-002"
    record.severity = "CRITICAL"
    record.status = "FAIL"

    result = json.loads(formatter.format(record))

    assert result["level"] == "INFO"
    assert result["logger"] == "rack_ops.test"
    assert result["message"] == "Diagnostic completed"
    assert result["event"] == "diagnostic_completed"
    assert result["rack_id"] == "LAB-RACK-002"
    assert result["severity"] == "CRITICAL"
    assert result["status"] == "FAIL"
    assert "timestamp" in result


def test_json_formatter_includes_http_metadata():
    formatter = JSONFormatter()

    record = logging.LogRecord(
        name="rack_ops.api",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="HTTP request completed",
        args=(),
        exc_info=None,
    )

    record.event = "http_request"
    record.method = "GET"
    record.path = "/health"
    record.status_code = 200
    record.duration_ms = 6.53

    result = json.loads(formatter.format(record))

    assert result["event"] == "http_request"
    assert result["method"] == "GET"
    assert result["path"] == "/health"
    assert result["status_code"] == 200
    assert result["duration_ms"] == 6.53