import os
from datetime import datetime

import pandas as pd
import streamlit as st

from monitor import get_cpu_usage, get_ram_usage, get_disk_usage, get_top_processes
from decision_engine import analyze_system
from planner import generate_plan
from recommendations import get_recommendation
from report_generator import generate_report
from history import save_history
from action_executor import (
    get_downloads_folder,
    scan_junk_summary,
    build_health_score,
    get_priority_list,
    generate_recovery_plan,
    execute_maintenance_cycle,
    load_action_history,
)


st.set_page_config(
    page_title="Nexus",
    page_icon="🦅",
    layout="wide"
)

st.title("🧠 Nexus Autonomous OS Agent")
st.caption(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


downloads_folder = get_downloads_folder()
cpu = get_cpu_usage()
ram = get_ram_usage()
disk = get_disk_usage()
junk = scan_junk_summary(downloads_folder)
health = build_health_score(cpu, ram, disk)
priority_items = get_priority_list(cpu, ram, disk, junk["count"])
recovery = generate_recovery_plan(cpu, ram)
plan_preview = generate_plan(cpu, ram, disk, junk["count"])

run_plan = False

st.sidebar.title("Nexus Control")
st.sidebar.markdown("#### Operating Mode")
autonomous_mode = st.sidebar.checkbox("Autonomous Mode [ON/OFF]", value=False)

if "last_autonomous_run" not in st.session_state:
    st.session_state.last_autonomous_run = 0

if autonomous_mode:
    st.markdown(
        """
        <meta http-equiv="refresh" content="30">
        """,
        unsafe_allow_html=True
    )

st.sidebar.markdown("---")
nav_page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "System Health",
        "Maintenance Plan",
        "Recovery Center",
        "Action History",
        "Reports",
    ],
)

st.sidebar.markdown("---")
st.sidebar.metric("CPU", f"{cpu}%")
st.sidebar.metric("RAM", f"{ram}%")
st.sidebar.metric("Disk", f"{disk}%")
st.sidebar.metric("Junk Files", f"{junk['count']}")

if autonomous_mode:
    st.sidebar.success("✅ Autonomous execution active")
    import time
    current_time = time.time()
    if current_time - st.session_state.last_autonomous_run > 60:
        st.session_state.last_autonomous_run = current_time
        run_plan = True
else:
    if st.sidebar.button("Execute Plan"):
        run_plan = True

save_history(cpu, ram, disk, health["overall"])

if run_plan:
    cycle = execute_maintenance_cycle(cpu, ram, disk, downloads_folder, autonomous=autonomous_mode)
else:
    cycle = None

if nav_page == "Dashboard":
    st.markdown("## 📊 Nexus Overview")
    st.write("A realistic autonomous OS maintenance dashboard with system observation, health, and agent reasoning.")

    top_row = st.columns(4)
    top_row[0].metric("CPU Usage", f"{cpu}%", delta=f"{max(0, 100-cpu)}% healthier")
    top_row[1].metric("RAM Usage", f"{ram}%", delta=f"{max(0, 100-ram)}% free")
    top_row[2].metric("Disk Usage", f"{disk}%", delta=f"{max(0, 100-disk)}% free")
    top_row[3].metric("Health Score", f"{health['overall']}/100")

    st.divider()
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("System Resource Chart")
        chart_data = pd.DataFrame({"Usage": [cpu, ram, disk]}, index=["CPU", "RAM", "Disk"])
        st.bar_chart(chart_data)

        st.subheader("Top Processes")
        processes = get_top_processes()
        for proc in processes:
            st.write(f"• {proc['name']} (PID {proc['pid']}) — {proc['memory']:.2f}% RAM")

    with col2:
        st.subheader("Agent Reasoning")
        observation, decision = analyze_system(cpu, ram, disk)
        st.markdown("**Observation**")
        for item in observation:
            st.write(f"- {item}")
        st.markdown("**Decision**")
        for item in decision:
            st.write(f"- {item}")
        st.markdown("**Recommendation**")
        for rec in get_recommendation(cpu, ram, disk):
            st.write(f"- {rec}")

    if cycle:
        st.divider()
        st.subheader("Execution Summary")
        if autonomous_mode:
            st.success("Autonomous Mode executed plan successfully.")
        else:
            st.info("Manual execution completed.")

        for action_item in cycle["actions"]:
            card = st.expander(f"{action_item['action']} — {action_item['status']}")
            with card:
                st.write(action_item["details"])
                if action_item["files"]:
                    st.write("Affected files:")
                    for file_path in action_item["files"][:20]:
                        st.write(f"- {file_path}")
                if action_item["verification"]:
                    st.write("Verification:")
                    st.write(action_item["verification"])

elif nav_page == "System Health":
    st.markdown("## 🩺 System Health")
    st.write("Health scores are calculated by CPU, RAM, and disk usage thresholds.")

    status = "Excellent" if health["overall"] >= 90 else "Good" if health["overall"] >= 75 else "Warning" if health["overall"] >= 60 else "Critical"
    color = "green" if health["overall"] >= 90 else "yellow" if health["overall"] >= 75 else "orange" if health["overall"] >= 60 else "red"

    st.metric("Health Status", status, delta=f"{health['overall']}/100")
    st.progress(health["overall"] / 100)
    st.write(f"### Health Breakdown")
    st.write(f"- CPU Score: {health['cpu_score']}\n- RAM Score: {health['ram_score']}\n- Disk Score: {health['disk_score']}")

    st.write("### Priority Queue")
    for priority in priority_items:
        if priority["level"] == "Critical":
            st.error(f"{priority['level']}: {priority['issue']} — {priority['details']}")
        elif priority["level"] == "High":
            st.warning(f"{priority['level']}: {priority['issue']} — {priority['details']}")
        elif priority["level"] == "Medium":
            st.info(f"{priority['level']}: {priority['issue']} — {priority['details']}")
        else:
            st.success(f"{priority['level']}: {priority['issue']} — {priority['details']}")

elif nav_page == "Maintenance Plan":
    st.markdown("## 🛠️ Maintenance Plan")
    st.write("This plan is generated from Nexus observations and current system status.")

    for task in plan_preview:
        st.write(f"- {task}")

    if cycle:
        st.divider()
        st.subheader("Action Execution Details")
        for action_item in cycle["actions"]:
            st.write(f"**{action_item['action']}** — {action_item['status']}")
            st.write(action_item["details"])
            if action_item["verification"]:
                st.write(f"Verification: {action_item['verification']}")
            st.markdown("---")
    else:
        if autonomous_mode:
            st.info("Waiting for the autonomous engine to complete the plan...")
        else:
            st.info("Manual mode is enabled, trigger execution from the sidebar.")

elif nav_page == "Recovery Center":
    st.markdown("## 🚨 Recovery Center")
    if recovery["active"]:
        severity_color = {
            "Critical": "🔴",
            "High": "🟠",
            "Medium": "🟡",
            "Low": "🟢"
        }
        severity = recovery.get("severity", "High")
        st.error(f"{severity_color.get(severity, '⚪')} Recovery Mode Activated — Severity: {severity}")
        st.write("### Recommended Recovery Strategy")
        for step in recovery["strategy"]:
            st.write(step)
        st.write(f"**Recovery Confidence:** {recovery['confidence']}%")
        
        if st.button("🚀 Execute Recovery Plan"):
            cycle = execute_maintenance_cycle(cpu, ram, disk, downloads_folder, autonomous=True)
            st.success("Recovery plan executed!")
            st.write("### Recovery Execution Results")
            for action_item in cycle["actions"]:
                st.write(f"✅ {action_item['action']} — {action_item['status']}")
    else:
        st.success("✅ No recovery needed at this time.")
        st.write("System is operating within safe resource thresholds.")

elif nav_page == "Action History":
    st.markdown("## 📝 Action History")
    history_lines = load_action_history(limit=20)
    if history_lines:
        history_df = pd.DataFrame({"Recent Actions": history_lines})
        st.table(history_df)
    else:
        st.info("No action history available yet.")

elif nav_page == "Reports":
    st.markdown("## 📑 Reports")
    st.write("Generate a delivery-ready summary report for demonstrations.")
    if st.button("Generate System Report"):
        report_file = generate_report(cpu, ram, disk, health["overall"])
        st.success(f"Report generated: {report_file}")
        st.write("Download the report from the project folder.")

    st.write("### Current System Snapshot")
    st.write(f"- CPU: {cpu}%\n- RAM: {ram}%\n- Disk: {disk}%\n- Junk files: {junk['count']}")

st.markdown("---")

st.write("Built for autonomous observation, analysis, decision, action, verification, and recovery.")
