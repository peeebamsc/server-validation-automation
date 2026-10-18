# Server Validation & Debug Automation

A Python-based server hardware validation and repair simulation designed to demonstrate automated diagnostics, infrastructure monitoring concepts, hardware failure classification, repair workflows, and quality assurance testing.

This project demonstrates practical Python automation techniques relevant to server production, hardware debugging, infrastructure operations, and reliability engineering.

## Project Overview

Server Validation & Debug Automation simulates the validation, troubleshooting, and repair of enterprise server hardware using configurable diagnostic thresholds.

The application evaluates simulated hardware metrics, identifies failures, classifies their severity, and generates structured JSON diagnostic reports.

It also supports simulated hardware repairs, allowing diagnostic results to be compared before and after corrective actions.

The project emphasizes:

- Automated hardware diagnostics
- Server failure detection and classification
- Repair and retest workflows
- Configuration-driven validation
- Structured diagnostic reporting
- Automated quality assurance
- Continuous integration and automated testing

**All hardware data is synthetic. No proprietary production systems or employer information are used.**

## RACK//OPS Dashboard

RACK//OPS is an interactive infrastructure operations dashboard built with Python and Streamlit.

The application demonstrates simulated enterprise server diagnostics, hardware failure classification, repair automation, and persistent repair history.

### Dashboard Preview

![RACK//OPS Infrastructure Dashboard](docs/screenshots/rack-ops-dashboard.png)

### Dashboard Features

- Modern dark-themed infrastructure operations interface
- 3D-styled server rack with hardware health indicators
- CPU, memory, disk, power supply, and network diagnostics
- Interactive server selection
- Configurable diagnostic thresholds
- Simulated repair and retest workflows
- Before-and-after diagnostic comparisons
- Persistent JSON repair history
- Automated testing with pytest
- Continuous integration using GitHub Actions

### Launch the Dashboard

Install the project dependencies:

```powershell
python -m pip install -r requirements.txt

## Features

### Automated Hardware Diagnostics

- CPU temperature monitoring
- Memory utilization monitoring
- Disk temperature monitoring
- Disk health validation
- Power supply health checks
- Network connectivity checks
- Configurable diagnostic thresholds
- Automated PASS/FAIL classification
- WARNING/CRITICAL severity classification
- Detection of multiple simultaneous hardware failures

### Repair and Retest Automation

- Simulated hardware repair operations
- Initial and post-repair diagnostic comparison
- Automated post-repair validation
- Repair notes and timestamps
- Validation of simulated repair changes
- Detection of incomplete repairs
- Preservation of original server data
- Structured repair records

### Reporting and Visualization

- Structured JSON diagnostic report generation
- Terminal-based results dashboard
- Server validation summaries
- Failure counts and severity classifications
- Repair validation results
- Initial and post-repair status comparisons

### Automated Quality Assurance

- Unit testing with pytest
- Pydantic data validation
- Hardware diagnostic testing
- JSON report validation
- Repair workflow testing
- GitHub Actions continuous integration
- Automated test execution on repository updates

## Technologies

| Technology | Purpose |
|---|---|
| Python 3.11 | Core application development |
| Pydantic | Hardware data modeling and validation |
| Pytest | Automated unit testing |
| Rich | Terminal dashboards and formatted output |
| JSON | Configuration and diagnostic reporting |
| Git | Version control |
| GitHub | Source code hosting |
| GitHub Actions | Continuous integration and automated testing |

## Project Structure

```text
server-validation-automation/
├── .github/
│   └── workflows/
│       └── python-tests.yml
├── config/
│   └── settings.json
├── docs/
├── reports/
├── src/
│   ├── __init__.py
│   ├── server_models.py
│   ├── server_diagnostics.py
│   ├── report_generator.py
│   └── repair_workflow.py
├── tests/
│   ├── __init__.py
│   ├── test_diagnostics.py
│   ├── test_reporting.py
│   └── test_repair_workflow.py
├── .gitignore
├── LICENSE
├── README.md
├── main.py
└── requirements.txt
```

### Core Modules

**server_models.py**

Defines simulated server hardware models and validates hardware metrics using Pydantic.

**server_diagnostics.py**

Evaluates hardware health metrics against configurable thresholds and identifies potential failures.

**report_generator.py**

Generates structured diagnostic reports and saves validation results in JSON format.

**repair_workflow.py**

Simulates hardware repairs, performs post-repair diagnostics, and records validation results before and after corrective actions.

**main.py**

Runs the application, evaluates simulated servers, generates reports, and displays diagnostic and repair results in the terminal.

## Installation

### 1. Clone the Repository

```powershell
git clone https://github.com/peeebamsc/server-validation-automation.git

cd server-validation-automation
```

### 2. Create a Python Virtual Environment

Python 3.11 is recommended.

```powershell
py -3.11 -m venv .venv
```

### 3. Activate the Virtual Environment

In PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

## Run the Application

Execute:

```powershell
python main.py
```

The application evaluates three simulated servers and displays a terminal-based diagnostic dashboard.

### Example: Initial Server Validation

| Rack ID | Status | Severity | Failures |
|---|---|---|---|
| LAB-RACK-001 | PASS | HEALTHY | 0 |
| LAB-RACK-002 | FAIL | CRITICAL | 3 |
| LAB-RACK-003 | FAIL | WARNING | 3 |

### Validation Summary

```text
Total Servers: 3
Passed: 1
Failed: 2
```

A JSON diagnostic report is generated at:

```text
reports/diagnostic_report.json
```

## Server Repair and Retest Workflow

The application simulates corrective actions for servers that fail initial hardware validation.

The repair workflow automatically performs diagnostics before and after simulated hardware changes.

### Example: Repairing a Failed Server

**Server:** LAB-RACK-002

#### Initial Diagnostic

```text
Status: FAIL
Severity: CRITICAL
Failures: 3
```

The simulated server initially reports:

- CPU temperature exceeding the configured threshold
- Disk health failure
- Power supply health failure

#### Simulated Repairs

The application applies the following simulated changes:

```python
repairs = {
    "cpu_temperature": 65,
    "disk_healthy": True,
    "power_supply_healthy": True
}
```

These changes represent:

1. Correcting an overheating condition
2. Restoring disk health
3. Restoring power supply health

#### Post-Repair Validation

After applying the simulated repairs, the application automatically reruns the diagnostic checks.

| Validation Stage | Status | Severity | Failures |
|---|---|---|---|
| Initial Diagnostic | FAIL | CRITICAL | 3 |
| Post-Repair Retest | PASS | HEALTHY | 0 |

### Repair Result

```text
Repair Successful: True
Repair Notes: Simulated CPU cooling, disk, and PSU repairs.
```

### Repair Record Structure

The repair workflow returns structured information containing:

- Server rack identification
- Repair timestamp
- Repair notes
- Simulated hardware changes
- Initial diagnostic results
- Final diagnostic results
- Repair success status

Repair records are currently generated in memory and displayed in the terminal. Persistent repair-history storage is planned for a future release.

**All repair operations are simulated. The application does not modify physical hardware.**

## Configuration

Diagnostic thresholds are defined in:

```text
config/settings.json
```

Example configuration:

```json
{
  "application": {
    "name": "Server Validation Automation",
    "version": "0.1.0",
    "environment": "simulation"
  },
  "diagnostic_thresholds": {
    "max_cpu_temperature_celsius": 85,
    "max_memory_utilization_percent": 90,
    "max_disk_temperature_celsius": 70
  }
}
```

The diagnostic engine uses these values to evaluate simulated hardware conditions.

**Note:** Thresholds are illustrative and should not be interpreted as manufacturer-specific hardware operating limits.

## Automated Testing

The application uses pytest to validate hardware diagnostics, reporting functionality, and repair workflows.

Run the complete test suite:

```powershell
python -m pytest -v
```

### Test Coverage

#### Hardware Diagnostics — 8 Tests

- Healthy server validation
- CPU overheating detection
- Memory overutilization detection
- Disk health failure detection
- Power supply failure detection
- Network connectivity failure detection
- Multiple simultaneous failures
- Diagnostic threshold boundaries

#### JSON Reporting — 5 Tests

- Report summary validation
- Report contents validation
- Timestamp validation
- Empty server list handling
- JSON report persistence

#### Repair Workflow — 7 Tests

- Successful simulated repairs
- Incomplete repair detection
- Required repair notes validation
- Required repair changes validation
- Invalid repair value rejection
- Original server data preservation
- Repair history validation

### Latest Verified Local Test Results

```text
20 passed in 0.55s
```

**Total: 20 automated tests passing.**

## Continuous Integration

The project uses GitHub Actions to execute automated tests when changes are pushed to the main branch or submitted through a pull request targeting main.

The workflow is defined in:

```text
.github/workflows/python-tests.yml
```

### CI Pipeline

The workflow performs the following operations:

1. Checks out the repository.
2. Configures Python 3.11.
3. Installs project dependencies.
4. Executes the complete pytest test suite.
5. Reports whether the automated tests pass or fail.

### GitHub Actions Workflow

```yaml
name: Python Server Validation Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v5

      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install -r requirements.txt

      - name: Run automated tests
        run: python -m pytest -v
```

The workflow provides automated validation of committed code changes.

## Engineering Objectives

This project demonstrates foundational skills relevant to infrastructure automation, server operations, and reliability engineering.

### Infrastructure and Hardware

- Server hardware diagnostics
- Hardware health validation
- Failure identification and classification
- Repair and retest procedures
- Server troubleshooting simulations
- Configuration-based validation

### Software Engineering

- Python application development
- Modular application architecture
- Data modeling with Pydantic
- Structured JSON reporting
- Automated unit testing
- Error handling and input validation
- Git-based version control

### Quality Assurance and Automation

- Automated validation workflows
- Regression testing
- Test-driven quality improvements
- Continuous integration
- Diagnostic result comparison
- Reproducible testing environments

## Roadmap

### Completed

- [x] Python project setup and virtual environment
- [x] Simulated server hardware models
- [x] Configurable diagnostic thresholds
- [x] Automated hardware validation
- [x] Hardware failure classification
- [x] JSON diagnostic report generation
- [x] Terminal-based validation dashboard
- [x] Simulated hardware repair and retesting
- [x] Initial and post-repair diagnostic comparison
- [x] Automated repair workflow tests
- [x] GitHub Actions continuous integration
- [x] 20 automated tests passing locally

### Planned Enhancements

- [ ] Simulated server rack inventory and asset tracking
- [ ] Persistent repair history and audit logging
- [ ] Multiple diagnostic and repair attempts
- [ ] Structured repair-history JSON exports
- [ ] Data integrity validation for saved repair records
- [ ] Infrastructure monitoring dashboard
- [ ] Docker containerization
- [ ] Expanded automated testing
- [ ] Additional infrastructure automation workflows

## Disclaimer

This project is an independent educational simulation.

All server models, hardware metrics, failure scenarios, and repair operations use synthetic data.

The application does not connect to production servers, modify physical hardware, or use proprietary employer information.

Diagnostic thresholds and repair scenarios are provided for educational and software testing purposes only.