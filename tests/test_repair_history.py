import json

import pytest

import src.repair_history as repair_history


@pytest.fixture
def temporary_history(tmp_path, monkeypatch):
    """
    Redirect repair-history storage to a temporary directory.

    This prevents tests from modifying actual application reports.
    """

    history_file = tmp_path / "reports" / "repair_history.json"

    monkeypatch.setattr(
        repair_history,
        "REPORTS_DIR",
        history_file.parent
    )

    monkeypatch.setattr(
        repair_history,
        "HISTORY_FILE",
        history_file
    )

    return history_file


@pytest.fixture
def sample_repair_record():
    """Create a simulated server repair record."""

    return {
        "rack_id": "LAB-RACK-002",
        "repair_timestamp": "2026-10-17T18:00:00+00:00",
        "repair_notes": "Simulated disk replacement.",
        "changes": {
            "disk_healthy": True
        },
        "initial_diagnostic": {
            "status": "FAIL",
            "severity": "CRITICAL"
        },
        "final_diagnostic": {
            "status": "PASS",
            "severity": "HEALTHY"
        },
        "repair_successful": True
    }


def test_empty_history_returns_list(temporary_history):
    """A missing history file should return an empty list."""

    result = repair_history.load_repair_history()

    assert result == []


def test_save_repair_record(
    temporary_history,
    sample_repair_record
):
    """Verify that a repair record is saved to JSON."""

    saved_path = repair_history.save_repair_record(
        sample_repair_record
    )

    assert saved_path.exists()
    assert saved_path == temporary_history

    with saved_path.open("r", encoding="utf-8") as file:
        saved_data = json.load(file)

    assert len(saved_data) == 1
    assert saved_data[0] == sample_repair_record


def test_load_repair_history(
    temporary_history,
    sample_repair_record
):
    """Verify that saved repair records can be retrieved."""

    repair_history.save_repair_record(sample_repair_record)

    history = repair_history.load_repair_history()

    assert len(history) == 1
    assert history[0]["rack_id"] == "LAB-RACK-002"
    assert history[0]["repair_successful"] is True


def test_multiple_repairs_preserved(
    temporary_history,
    sample_repair_record
):
    """Verify that saving another repair preserves earlier records."""

    repair_history.save_repair_record(sample_repair_record)

    second_record = {
        **sample_repair_record,
        "rack_id": "LAB-RACK-003",
        "repair_notes": "Simulated power supply replacement."
    }

    repair_history.save_repair_record(second_record)

    history = repair_history.load_repair_history()

    assert len(history) == 2
    assert history[0]["rack_id"] == "LAB-RACK-002"
    assert history[1]["rack_id"] == "LAB-RACK-003"


def test_invalid_history_structure(
    temporary_history
):
    """Verify that a non-list JSON history is rejected."""

    temporary_history.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    temporary_history.write_text(
        '{"invalid": "structure"}',
        encoding="utf-8"
    )

    with pytest.raises(
        ValueError,
        match="Repair history must contain a JSON list"
    ):
        repair_history.load_repair_history()


def test_invalid_history_rejected_when_saving(
    temporary_history,
    sample_repair_record
):
    """Verify that invalid existing history is not overwritten."""

    temporary_history.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    original_content = '{"invalid": "structure"}'

    temporary_history.write_text(
        original_content,
        encoding="utf-8"
    )

    with pytest.raises(
        ValueError,
        match="Repair history must contain a JSON list"
    ):
        repair_history.save_repair_record(
            sample_repair_record
        )

    assert temporary_history.read_text(
        encoding="utf-8"
    ) == original_content