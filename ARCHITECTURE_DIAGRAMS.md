# Nexus Architecture Diagrams

## Observe → Analyze → Decide → Act → Verify → Recover

```mermaid
flowchart LR
    Observe[Observe\nSystem Metrics]\n    Analyze[Analyze\nResource State]\n    Decide[Decide\nMaintenance Plan]\n    Act[Act\nExecute Tasks]\n    Verify[Verify\nEvaluate Impact]\n    Recover[Recover\nRecovery Strategy]\n
    Observe --> Analyze
    Analyze --> Decide
    Decide --> Act
    Act --> Verify
    Verify --> Recover
    Recover --> Observe
```

## Module Dependency Diagram

```mermaid
flowchart TD
    Dashboard[Dashboard UI]\n    Monitor[monitor.py]\n    Decision[decision_engine.py]\n    Planner[planner.py]\n    Executor[action_executor.py]\n    Verification[verification.py]\n    History[history.py / history_logger.py]\n    Report[report_generator.py]\n    Recommendations[recommendations.py]

    Dashboard --> Monitor
    Dashboard --> Decision
    Dashboard --> Planner
    Dashboard --> Executor
    Dashboard --> History
    Dashboard --> Report
    Dashboard --> Recommendations
    Executor --> Verification
    Executor --> History
    Executor --> Cleaner[cleaner.py]
    Executor --> Organizer[organizer.py]
    Dashboard --> Monitor
```

## Data Flow Diagram

```mermaid
flowchart LR
    SystemMetrics[System Metrics]\n    Monitor[monitor.py]\n    Decision[decision_engine.py]\n    Planner[planner.py]\n    Executor[action_executor.py]\n    Verification[verification.py]\n    History[history.py]\n    UI[dashboard.py]\n    Report[report_generator.py]

    SystemMetrics --> Monitor
    Monitor --> Decision
    Monitor --> Planner
    Decision --> Planner
    Planner --> Executor
    Executor --> Verification
    Executor --> History
    Verification --> UI
    History --> Report
    UI --> Report
```

## Agent Workflow Diagram

```mermaid
flowchart TD
    Start[Start Nexus Agent]\n    Collect[Collect Metrics]\n    Analyze[Analyze Resource Status]\n    Plan[Build Maintenance Plan]\n    Execute[Execute Actions]\n    Verify[Verify Results]\n    Recover[Evaluate Recovery Need]\n    Log[Log History and Actions]\n    End[Return to Observation]

    Start --> Collect
    Collect --> Analyze
    Analyze --> Plan
    Plan --> Execute
    Execute --> Verify
    Verify --> Recover
    Recover --> Log
    Log --> End
    End --> Collect
```
