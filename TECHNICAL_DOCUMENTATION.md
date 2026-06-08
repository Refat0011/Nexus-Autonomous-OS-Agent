# Nexus Autonomous OS Optimization & Recovery Agent — Technical Documentation

## Introduction

The Nexus Autonomous OS Optimization & Recovery Agent is a modular Python system designed to observe Windows system state, analyze resource pressures, make automated maintenance decisions, execute tasks, verify improvements, and recommend recovery actions. It is designed for university-level system engineering analysis and can be used as a proof-of-concept autonomous operations agent.

## System Design

The system is structured as a layered agent architecture:

- **Observation Layer**: Collects telemetry from the host OS.
- **Decision Layer**: Interprets telemetry and generates action recommendations.
- **Planning Layer**: Compiles work items into an executable maintenance plan.
- **Execution Layer**: Performs cleanup, organization, and logging.
- **Verification Layer**: Measures effect and confirms success.
- **Recovery Layer**: Provides a strategy when operating thresholds are breached.

The design emphasizes separation of concerns, readability, and extensibility.

## Architecture Diagram Explanation

The following diagrams describe the component relationships and data movement:

- **Observe → Analyze → Decide → Act → Verify → Recover**: The core agent lifecycle.
- **Module Dependency Diagram**: How each Python module depends on others.
- **Data Flow Diagram**: Information flow from system metrics through decision-making to action logs.
- **Agent Workflow Diagram**: The high-level runtime sequence of the autonomous agent.

Refer to `ARCHITECTURE_DIAGRAMS.md` for the full Mermaid diagrams.

## Module-by-Module Explanation

### monitor.py

`monitor.py` provides the observation layer:

- `get_cpu_usage()` uses `psutil.cpu_percent(interval=1)`.
- `get_ram_usage()` uses `psutil.virtual_memory().percent`.
- `get_disk_usage()` measures Windows `C:\` usage.
- `get_top_processes()` lists the top five memory-consuming processes.

This module is called by `dashboard.py` and `main.py` to supply live telemetry.

### decision_engine.py

`decision_engine.py` implements simple if-then rules:

- Detects high CPU, RAM, or disk usage.
- Returns observational statements and corresponding decisions.
- When no issue is detected, it returns a healthy state.

This module supports the dashboard's reasoning panel.

### planner.py

`planner.py` builds a maintenance plan based on current metrics:

- Adds memory optimization tasks if RAM is high.
- Adds storage cleanup when disk usage is high.
- Adds junk removal when junk files exist.
- Always suggests organizing the downloads folder.

The plan is then executed or displayed in the UI.

### optimizer.py

`optimizer.py` provides optimization recommendations:

- Suggests application closure for CPU/RAM high use.
- Recommends restart when both CPU and RAM are elevated.
- Returns a normal state message when no issue is present.

### organizer.py

`organizer.py` is responsible for file organization within the `downloads_test` folder:

- Creates category folders for images, documents, videos, code, and others.
- Moves files into the appropriate folder.
- Prevents folder recursion by skipping directories.

This module is used in the action execution flow and as a standalone utility.

### verification.py

`verification.py` implements a lightweight verification strategy:

- `verify_action(before, after)` returns a status and improvement delta.
- It is used to confirm whether cleanup reduced a metric value.

### history.py

`history.py` persists system snapshots using `pandas`:

- Writes `CPU`, `RAM`, `DISK`, and `HEALTH` values to `history.csv`.
- Uses append mode to preserve historical snapshots.

### report_generator.py

`report_generator.py` creates a text-based summary report:

- Writes current metrics, health interpretation, and optimization recommendations.
- Includes historical performance summary derived from `history.csv`.

### dashboard.py

`dashboard.py` is the Streamlit front end and the primary orchestrator:

- Loads system metrics and computes health scores.
- Renders six navigation pages.
- Provides manual and autonomous mode controls.
- Calls `execute_maintenance_cycle()` during plan execution.
- Integrates recovery activation and report generation.

### action_executor.py

`action_executor.py` coordinates execution and verification:

- Scans junk files using `cleaner.scan_junk()`.
- Builds a plan from `planner.generate_plan()`.
- Executes cleanup and organization tasks.
- Uses `verify_action()` to validate improvement.
- Appends action history via `history_logger.save_action()`.

This module contains logic for file deletion, moving downloads, and post-action metric evaluation.

## Data Flow

Data flows through Nexus as follows:

1. `dashboard.py` requests system metrics from `monitor.py`.
2. Metrics are passed to `decision_engine.py` and `planner.py`.
3. The generated plan is executed by `action_executor.py`.
4. After action execution, `verification.py` confirms results.
5. Historical metrics are stored by `history.py`.
6. Report generation reads from `history.csv` and writes a summary text file.

## Agent Decision Logic

The decision logic is rule-based and threshold-driven:

- CPU > 85% triggers optimization recommendations.
- RAM > 85% triggers memory optimization planning.
- Disk > 90% triggers storage cleanup planning.
- Chart and dashboard panels expose these decisions.

## Recovery Logic

Recovery logic is activated when system pressure crosses safety thresholds:

- RAM above 85% can activate recovery strategies.
- CPU above 85% can also trigger recovery recommendations.
- Recovery severity is assigned as Critical, High, Medium, or Low.
- The dashboard exposes a recovery execution button.

## Health Score Calculation Logic

Health scoring uses threshold bands:

- CPU, RAM, and disk each map to 100/80/60/40 score bands.
- Overall health is the average of the three scores.
- The System Health dashboard converts the score into status labels.

## Action Logging Logic

Action logging uses two files:

- `action_history.txt` records each executed plan item and its status.
- `history.csv` records periodic system snapshots for trend analysis.

Logs include timestamps, action descriptions, files affected, and status.

## Performance Verification Logic

Verification compares before and after metrics:

- If the after value is lower than the before value, the action is deemed successful.
- Improvement deltas are calculated for the dashboard summary.
- When no improvement is observed, actions are marked as “No Significant Improvement.”

## Error Handling

Nexus uses defensive error handling in multiple places:

- File deletion is wrapped in `try/except` blocks to avoid hard failures.
- Process iteration skips inaccessible processes.
- Report generation handles missing history data gracefully.
- Dashboard control logic avoids invalid state transitions.

## Future Scalability Design

The current architecture supports scalability through:

- Modular separation of monitoring, decision-making, planning, and execution.
- Add-on modules for platform abstraction and cloud integration.
- Future support for containerized deployment or microservice boundaries.
- A potential event bus to replace direct function calls with asynchronous task handling.

This design allows the agent to grow into a production-grade autonomous maintenance platform.
