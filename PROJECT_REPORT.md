# Nexus Autonomous OS Optimization & Recovery Agent — Project Report

## Abstract

Nexus is an autonomous optimization and recovery agent designed to observe Windows system health, generate maintenance plans, execute cleanup actions, and validate outcomes. This project demonstrates a full agent lifecycle using Python, Streamlit, and system telemetry.

## Introduction

Automated system maintenance is increasingly important as users rely on personal computers for daily productivity. Nexus provides an accessible and modular solution to manage resource use, reduce junk files, and recover from performance degradation.

## Problem Definition

Many operating systems encounter performance issues due to temporary file accumulation, unmanaged downloads, excessive memory use, and delayed recovery. Manual maintenance is often inconsistent and lacks a clear audit trail.

## System Objectives

- Monitor CPU, RAM, and disk usage continuously.
- Analyze system state with an autonomous reasoning layer.
- Generate and execute prioritized maintenance plans.
- Verify the impact of maintenance operations.
- Provide recovery guidance when thresholds are exceeded.
- Present results through a professional dashboard.

## Methodology

This project uses modular Python development and a Streamlit interface. System telemetry is captured by `psutil`, then analyzed through deterministic rules. The agent generates a plan, executes actions, logs history, and produces a formal report.

## System Architecture

The architecture separates responsibilities into modules:

- Observation: `monitor.py`
- Analysis: `decision_engine.py`
- Planning: `planner.py`
- Execution: `action_executor.py`
- Verification: `verification.py`
- Reporting: `report_generator.py`

A Streamlit front end orchestrates user interaction and autonomous behavior.

## Implementation

The implementation includes:

- `dashboard.py` as the primary UI entrypoint.
- `monitor.py` for real-time metric capture.
- `planner.py` to build actionable maintenance plans.
- `action_executor.py` to perform cleanup and organization.
- `history.py` and `history_logger.py` for persistence.
- `report_generator.py` for exportable system reports.

The project also includes `main.py` and `scheduler.py` as a command-line fallback.

## Results

Nexus successfully produces:

- A system health score.
- A prioritized maintenance plan.
- Executable junk cleanup and downloads organization.
- Verification summaries for each action.
- A recovery strategy when resource usage is elevated.
- Historical logging and report generation.

## Testing

Testing is performed through manual dashboard interactions and simulated system states. Key checks include:

- Correct metric capture from `psutil`.
- Plan generation for high RAM, CPU, and disk states.
- Successful execution of junk cleanup tasks.
- Persistent history recording to `history.csv`.
- Report creation without errors.

## Challenges Faced

- Ensuring Streamlit maintained module state cleanly during development.
- Coordinating file organization and cleanup actions in a safe manner.
- Providing clear, user-facing recovery guidance for critical conditions.

## Lessons Learned

- Modular design simplifies agent logic and debugging.
- Simple threshold rules can provide effective early-stage decision-making.
- Verification and logging are essential to build trust in automated maintenance.
- A dashboard interface greatly improves visibility for autonomous systems.

## Future Scope

Future enhancements may include:

- Cross-platform compatibility.
- Advanced scheduling and background service deployment.
- Report export to PDF and HTML.
- Secure remote monitoring and control.
- Integration with cloud observability platforms.

## Conclusion

Nexus demonstrates a practical, university-level autonomous OS optimization and recovery agent. It successfully combines real-time observation, rule-based decision logic, actionable maintenance, verification, and recovery into a coherent dashboard-driven system.

## References

- Streamlit documentation: https://streamlit.io/
- psutil documentation: https://psutil.readthedocs.io/
- pandas documentation: https://pandas.pydata.org/
- Python standard library documentation: https://docs.python.org/3/