# Server Validation & Debug Automation

A Python-based server hardware validation simulator designed to demonstrate automated diagnostics, infrastructure monitoring concepts, hardware failure classification, and quality assurance testing.

## Project Overview

This project simulates the validation of enterprise server hardware using configurable diagnostic thresholds.

It evaluates simulated hardware metrics, identifies failures, classifies their severity, and generates structured JSON reports.

All hardware data is synthetic. No proprietary production systems or employer information are used.

## Features

- Automated server hardware validation
- CPU temperature monitoring
- Memory utilization monitoring
- Disk temperature and health checks
- Power supply health checks
- Network connectivity checks
- Configurable diagnostic thresholds
- PASS/FAIL classification
- WARNING/CRITICAL severity classification
- JSON diagnostic report generation
- Terminal-based results dashboard
- Automated testing with pytest

## Technologies

- Python 3.11
- Pydantic
- Pytest
- Rich
- JSON
- Git

## Project Structure

```text
server-validation-automation/
├── config/
│   └── settings.json
├── docs/
├── reports/
├── src/
│   ├── __init__.py
│   ├── server_models.py
│   ├── server_diagnostics.py
│   └── report_generator.py
├── tests/
│   ├── __init__.py
│   ├── test_diagnostics.py
│   └── test_reporting.py
├── .gitignore
├── LICENSE
├── README.md
├── main.py
└── requirements.txt
```

## Installation

Clone the repository:

```bash
git clone https://github.com/peeebamsc/server-validation-automation.git
cd server-validation-automation
```

Create a Python virtual environment:

```powershell
py -3.11 -m venv .venv
```

Activate the environment in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run the Application

```powershell
python main.py
```

The application evaluates three simulated servers and displays a terminal dashboard.

Example:

| Rack ID | Status | Severity | Failures |
|---|---|---|---|
| LAB-RACK-001 | PASS | HEALTHY | 0 |
| LAB-RACK-002 | FAIL | CRITICAL | 3 |
| LAB-RACK-003 | FAIL | WARNING | 3 |

A JSON report is generated at:

```text
reports/diagnostic_report.json
```

## Automated Testing

Run the test suite:

```powershell
python -m pytest -v
```

Current test coverage includes:

- Healthy server validation
- CPU overheating detection
- Memory overutilization detection
- Disk health failure detection
- Power supply failure detection
- Network connectivity failure detection
- Multiple simultaneous failures
- Diagnostic threshold boundaries
- Report summary validation
- Report contents validation
- Timestamp validation
- Empty input handling
- JSON report persistence

**Current result: 13 passing tests.**

## Configuration

Diagnostic thresholds are defined in:

```text
config/settings.json
```

Thresholds are illustrative values used for simulation and should not be interpreted as manufacturer-specific hardware limits.

## Engineering Objectives

This project demonstrates foundational skills in:

- Infrastructure automation
- Hardware diagnostics
- Python development
- Automated quality assurance
- Structured data validation
- Configuration management
- Failure classification
- Technical reporting

## Roadmap

Future enhancements include:

- Simulated server rack inventory
- Repair and retest workflows
- GitHub Actions CI/CD
- Infrastructure monitoring dashboard
- Docker containerization

## Disclaimer

This project is an independent educational simulation using synthetic data. It does not connect to production hardware or use proprietary employer information.