# Nexus Autonomous OS Optimization & Recovery Agent

[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Enabled-orange)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Frame-blue)](https://pandas.pydata.org/)
[![Psutil](https://img.shields.io/badge/psutil-System%20Monitoring-brightgreen)](https://pypi.org/project/psutil/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange)](https://matplotlib.org/)
[![Status](https://img.shields.io/badge/Status-Beta-yellowgreen)](https://github.com/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

## Project Overview

Nexus is an autonomous operating system optimization and recovery agent built to observe system health, analyze resource pressures, generate a prioritized plan, execute maintenance actions, verify results, and recover from critical conditions. It delivers a professional Streamlit dashboard for interactive system maintenance, periodic auto-execution, and evidence-based reporting.

## Problem Statement

Modern Windows systems often suffer from unmanaged temporary files, fragmented downloads, runaway resource use, and delayed recovery after performance degradation. Manual maintenance is time-consuming, inconsistent, and lacks visibility for users or administrators.

## Objectives

- Provide a lightweight autonomous agent for Windows OS health monitoring.
- Automate cleanup, organization, and recovery processes.
- Enable transparent decision-making through a visual dashboard.
- Record activity history and generate formal reports.
- Support both manual execution and autonomous mode.

## Key Features

- Real-time CPU, RAM, disk, and junk file observation.
- Agent reasoning based on current system state.
- Priority-based maintenance plan generation.
- Junk cleanup and downloads organization.
- Recovery plan activation for high resource usage.
- Action history logging and report generation.
- Streamlit-based dashboard for visibility and control.

## System Architecture

Nexus is organized into modular components that separate responsibilities cleanly:

- `monitor.py` collects system metrics and process data.
- `decision_engine.py` evaluates the observed state.
- `planner.py` builds a maintenance plan.
- `action_executor.py` executes cleanup, organization, and verification.
- `verification.py` validates changes after execution.
- `history.py` and `history_logger.py` persist system and action records.
- `dashboard.py` exposes a user interface over Streamlit.

The architecture implements a full Observe → Analyze → Decide → Act → Verify → Recover lifecycle.

## Observe → Analyze → Decide → Act → Verify → Recover Cycle

1. **Observe**: Collect live CPU, RAM, disk, top processes, and junk file statistics.
2. **Analyze**: Interpret observations to identify resource pressure and system risk.
3. **Decide**: Build a context-aware maintenance plan using current metrics.
4. **Act**: Execute cleanup, file organization, and resource optimization actions.
5. **Verify**: Confirm whether actions produced measurable improvement.
6. **Recover**: Trigger recovery recommendations when thresholds are exceeded.

## Technology Stack

- Python 3.12
- Streamlit
- pandas
- psutil
- Standard Python libraries: `os`, `shutil`, `datetime`, `time`

## Installation Guide

1. Clone the repository:

```bash
git clone https://github.com/your-username/project_nexus.git
cd project_nexus
```

2. Create a Python virtual environment:

```bash
python -m venv venv
source venv/Scripts/activate
```

3. Install dependencies:

```bash
pip install streamlit pandas psutil
```

4. Run the dashboard:

```bash
streamlit run dashboard.py
```

5. Open the dashboard in your browser at `http://localhost:8501`.

## Project Structure

- `dashboard.py` — Main Streamlit UI and user interaction layer.
- `monitor.py` — Captures CPU, RAM, disk, and process statistics.
- `decision_engine.py` — Analyzes system telemetry and recommends action.
- `planner.py` — Builds the maintenance plan based on current state.
- `action_executor.py` — Executes maintenance tasks and verifies results.
- `verification.py` — Validates improvements after action execution.
- `history.py` — Stores periodic system snapshots to `history.csv`.
- `history_logger.py` — Logs executed actions to `action_history.txt`.
- `report_generator.py` — Creates output reports for demonstrations.
- `cleaner.py` — Scans and removes junk file types.
- `organizer.py` — Organizes `downloads_test` into file categories.
- `optimizer.py` — Generates optimization recommendations.
- `recommendations.py` — Produces dashboard suggestions.
- `main.py` — CLI-style monitor and scheduler reference implementation.
- `scheduler.py` — Basic periodic execution helper.
- `logs/` — Stores runtime logs for audit and traceability.

## Usage Instructions

1. Start the Streamlit dashboard.
2. Monitor the dashboard metrics and status panels.
3. Use manual mode to review the plan, then click **Execute Plan**.
4. Enable **Autonomous Mode** to let Nexus self-trigger maintenance checks.
5. Review the **Action History** and **Reports** pages for evidence.

## Dashboard Explanation

The dashboard is divided into six sections:

- **Dashboard**: Real-time metrics, top processes, recommendations, and execution summary.
- **System Health**: Health scoring, resource breakdown, and priority queue.
- **Maintenance Plan**: Active plan preview and completed action details.
- **Recovery Center**: Recovery activation and severity-based guidance.
- **Action History**: Historical log of maintenance actions.
- **Reports**: Generate exportable system reports.

## System Health Module

The System Health module calculates a composite health score from CPU, RAM, and disk use. It classifies the system state with thresholds and presents a priority queue for remediation actions.

## Maintenance Plan Module

This module generates the maintenance plan from current metrics. It can include memory optimization, storage cleanup, junk file deletion, and downloads folder organization.

## Recovery Center Module

If resource thresholds are breached, the Recovery Center activates a recovery strategy with severity colors and confidence ratings. It allows the user to execute an emergency recovery flow.

## Action History Module

Executed actions are appended to `action_history.txt`. The dashboard shows the latest history entries and provides traceability for maintenance decisions.

## Reports Module

The Reports module generates a snapshot file with system metrics, health interpretation, optimization recommendations, and historical record summary. The output file is saved in the repository root.

## Autonomous Mode Explanation

When autonomous mode is enabled, Nexus self-triggers a maintenance cycle approximately every 60 seconds and refreshes the dashboard. It enables continuous observation and action without manual intervention.

## Current Limitations

- Designed for Windows systems with `C:\` disk monitoring.
- No advanced machine learning or predictive modeling.
- Does not terminate individual processes automatically.
- Report export is limited to text format.
- Visual screenshots are placeholder references and should be added in production.

## Future Improvements

- Add cross-platform support for Linux and macOS.
- Introduce richer report formats (PDF, HTML).
- Add background service scheduling and remote management.
- Improve action verification with more metrics.
- Extend file categorization and recovery rules.
- Add user authentication and secure logging.

## Screenshots

> Add actual dashboard screenshots to the `/screenshots` folder and update these references.

- ![Dashboard Overview](screenshots/dashboard_overview.png)
- ![System Health](screenshots/system_health.png)
- ![Maintenance Plan](screenshots/maintenance_plan.png)
- ![Recovery Center](screenshots/recovery_center.png)

## Contributors

- Project Nexus Core Team
- Developer: Autonomous OS Optimization Architect

## License

This project is released under the MIT License.

## Acknowledgements

- Streamlit for rapid dashboard prototyping.
- psutil for robust system metrics.
- pandas for history persistence and data handling.
- The open-source community for guidance and tooling.