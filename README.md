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

<img width="3204" height="1774" alt="image" src="https://github.com/user-attachments/assets/cac5c327-d911-4015-a11d-d60c8be7cea8" />


### Production-Style Infrastructure Automation (v2.0.0 Development)

RACK//OPS is a server validation and debug automation project designed to simulate hardware diagnostics, repair workflows, and infrastructure operations.

The project combines Python-based hardware validation with a REST API, an interactive dashboard, automated testing, containerization, and structured logging.

Infrastructure and Automation

* Python and Pydantic: Validate simulated server hardware metrics and enforce input constraints.
* FastAPI: Provide REST endpoints for server inventory, hardware diagnostics, simulated repairs, and repair history.
* Streamlit: Display server health, diagnostic results, and repair workflows through an interactive dashboard.
* Docker: Package the dashboard and API into separate container images.
* Docker Compose: Define the dashboard and API services with shared persistent storage. Multi-container startup and persistence verification are in progress.
* GitHub Actions: Automatically run Python tests and build a Docker image for CI validation.
* Structured JSON Logging: Capture HTTP requests, execution times, diagnostic severity, and repair events.

Automated Validation

The current test suite contains 42 passing automated tests, covering server diagnostics, reporting, repair workflows, API behavior, request validation, and logging formatting.

The GitHub Actions pipeline has successfully completed both the Python test job and Docker image build job.

REST API

Method	Endpoint	Purpose
GET	/health	API health check
GET	/api/v1/servers	List simulated servers
GET	/api/v1/servers/{rack_id}	Retrieve server details
GET	/api/v1/diagnostics/{rack_id}	Execute hardware diagnostics
POST	/api/v1/repairs	Simulate repairs and retesting
GET	/api/v1/repairs/history	Retrieve saved repair records

Interactive API documentation is available at /docs when the API service is running.

Engineering Focus

This project demonstrates practical skills in server hardware validation, Python automation, API development, automated testing, Docker containerization, CI pipelines, and infrastructure observability.

Development status: v2.0.0 infrastructure integration is in progress. All 42 tests and the GitHub Actions container build have passed. Docker Compose runtime verification remains pending.

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
| Python 3.11 | Core application development and automation |
| Pydantic | Hardware data modeling and input validation |
| FastAPI | REST API development and hardware diagnostics endpoints |
| Streamlit | Interactive infrastructure monitoring dashboard |
| Docker | Containerization of dashboard and API services |
| Docker Compose | Multi-container orchestration and persistent volumes |
| Pytest | Automated unit and API testing |
| Rich | Terminal dashboards and formatted output |
| JSON | Configuration, diagnostic reporting, and structured logging |
| Git | Version control |
| GitHub | Source code hosting |
| GitHub Actions | Continuous integration, automated testing, and Docker image builds |

## Project Structure

server-validation-automation/
├── .github/
│   └── workflows/
│       └── python-tests.yml
├── .streamlit/
│   └── config.toml
├── config/
│   └── settings.json
├── docs/
│   └── screenshots/
├── reports/
├── src/
│   ├── __init__.py
│   ├── api.py
│   ├── logging_config.py
│   ├── repair_history.py
│   ├── repair_workflow.py
│   ├── report_generator.py
│   ├── server_diagnostics.py
│   ├── server_inventory.py
│   └── server_models.py
├── tests/
│   ├── test_api.py
│   ├── test_diagnostics.py
│   ├── test_logging.py
│   ├── test_repair_workflow.py
│   └── test_reporting.py
├── .dockerignore
├── .gitignore
├── compose.yaml
├── dashboard.py
├── Dockerfile
├── Dockerfile.api
├── LICENSE
├── main.py
├── README.md
└── requirements.txt


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

Repair records are stored persistently in reports/repair_history.json.

The repair-history module supports saving and retrieving simulated repair records. Docker containers are configured to share a named volume for persistent repair-history storage.

Shared-volume operation across the dashboard and API containers is pending final runtime verification.

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

**Total: 20 automated tests passing.** (10/15/2026)

Latest Verified Test Results

42 automated tests passing

The test suite covers:

* Hardware diagnostics and threshold validation
* JSON diagnostic reporting
* Repair and retest workflows
* Persistent repair-history operations
* FastAPI endpoints and request validation
* Structured JSON logging

The complete test suite can be executed using:

python -m pytest -v

GitHub Actions has successfully executed the automated tests and Docker image build on the feature/production-infrastructure branch.



## Continuous Integration

RACK//OPS uses GitHub Actions to automate Python testing and Docker image builds.

The CI pipeline validates application functionality and verifies that the application can be packaged into a Docker image.

The workflow is defined in:

.github/workflows/python-tests.yml

CI Pipeline

The workflow contains two jobs:

1. Python Tests

* Checks out the repository.
* Configures Python 3.11.
* Installs project dependencies.
* Executes the complete pytest test suite.
* Reports test results.

2. Docker Image Build

* Runs after the Python Tests job succeeds.
* Checks out the repository.
* Configures Docker Buildx.
* Builds the application Docker image.
* Verifies that the Docker image builds successfully without publishing it to a container registry.

Workflow Triggers

The CI pipeline runs automatically when:

* Changes are pushed to main.
* Changes are pushed to feature/production-infrastructure.
* A pull request targets main.
* The workflow is manually triggered through GitHub Actions.

Latest Verified CI Results

* 42 automated Python tests passing
* Python Tests job: Successful
* Docker Image Build job: Successful
* GitHub Actions workflow: RACK OPS CI

The CI pipeline provides automated regression testing and container build validation throughout infrastructure development.

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

### Roadmap

Completed

* [x]	Python project setup and virtual environment
* [x]	Simulated server hardware models
* [x]	Configurable diagnostic thresholds
* [x]	Automated hardware validation
* [x]	Hardware failure classification
* [x]	JSON diagnostic report generation
* [x]	Terminal-based validation dashboard
* [x]	Simulated hardware repair and retesting
* [x]	Initial and post-repair diagnostic comparison
* [x]	Automated repair workflow tests
* [x]	Simulated server rack inventory
* [x]	Persistent JSON repair history
* [x]	Multiple simulated diagnostic and repair records
* [x]	Interactive Streamlit infrastructure dashboard
* [x]	Server rack visualization and hardware health indicators
* [x]	FastAPI REST API development
* [x]	REST endpoints for server inventory and diagnostics
* [x]	REST endpoints for simulated repairs and repair history
* [x]	Pydantic API request validation
* [x]	Structured JSON application logging
* [x]	Docker containerization of dashboard and API services
* [x]	Docker Compose service configuration
* [x]	Docker Compose image builds
* [x]	GitHub Actions continuous integration
* [x]	Automated Docker image builds in GitHub Actions
* [x]	42 automated tests passing locally
* [x]	Successful GitHub Actions test and Docker build pipeline

Planned Enhancements

* [ ]	Docker Compose multi-container runtime verification
* [ ]	Verify shared persistent repair history between API and dashboard
* [ ]	Data integrity validation for saved repair records
* [ ]	Structured repair-history JSON export functionality
* [ ]	Expanded API integration and infrastructure testing
* [ ]	Additional infrastructure automation workflows
* [ ]	Production-style deployment configuration
* [ ]	Finalize v2.0.0 documentation
* [ ]	Merge infrastructure development branch into main
* [ ]	Publish RACK//OPS v2.0.0 GitHub release

## Disclaimer

This project is an independent educational simulation.

All server models, hardware metrics, failure scenarios, and repair operations use synthetic data.

The application does not connect to production servers, modify physical hardware, or use proprietary employer information.

Diagnostic thresholds and repair scenarios are provided for educational and software testing purposes only.
