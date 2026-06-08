import os
import shutil
from datetime import datetime

import psutil

from cleaner import scan_junk
from planner import generate_plan
from verification import verify_action
from history_logger import save_action
from logger import write_log

DOWNLOADS_FOLDER_NAME = "downloads_test"
JUNK_EXTENSIONS = {".tmp", ".log", ".bak"}


def get_project_root():
    return os.path.abspath(os.path.dirname(__file__))


def get_downloads_folder():
    downloads_folder = os.path.join(get_project_root(), DOWNLOADS_FOLDER_NAME)
    os.makedirs(downloads_folder, exist_ok=True)
    return downloads_folder


def scan_junk_summary(folder_path):
    junk_count, total_size = scan_junk(folder_path)
    return {
        "count": junk_count,
        "size": total_size
    }


def build_health_score(cpu, ram, disk):
    cpu_score = 100 if cpu < 50 else 80 if cpu < 70 else 60 if cpu < 85 else 40
    ram_score = 100 if ram < 60 else 80 if ram < 75 else 60 if ram < 90 else 40
    disk_score = 100 if disk < 70 else 80 if disk < 80 else 60 if disk < 90 else 40
    overall = int((cpu_score + ram_score + disk_score) / 3)
    return {
        "cpu_score": cpu_score,
        "ram_score": ram_score,
        "disk_score": disk_score,
        "overall": overall
    }


def get_priority_list(cpu, ram, disk, junk_count):
    priorities = []

    if ram > 90:
        priorities.append({"level": "Critical", "issue": "RAM usage above 90%", "details": "Immediate recovery and memory reduction needed."})

    if disk > 85:
        priorities.append({"level": "High", "issue": "Disk usage above 85%", "details": "Storage cleanup should run soon."})

    if junk_count > 20:
        priorities.append({"level": "Medium", "issue": f"{junk_count} junk files detected", "details": "Remove temporary and log files."})

    if not priorities:
        priorities.append({"level": "Low", "issue": "No urgent issues", "details": "System is stable."})

    return priorities


def append_action_history(action, status, files_affected=None):
    save_action(action, status, files_affected)
    write_log(f"Action executed: {action} - {status}")


def load_action_history(limit=20):
    if not os.path.exists("action_history.txt"):
        return []

    with open("action_history.txt", "r", encoding="utf-8") as history_file:
        lines = history_file.readlines()

    lines = [line.strip() for line in lines if line.strip()]
    return lines[-limit:][::-1]


def generate_recovery_plan(cpu, ram):
    recovery_config = {
        "active": False,
        "strategy": [],
        "confidence": 0,
        "severity": "Low"
    }

    if ram > 85:
        recovery_config["active"] = True
        recovery_config["severity"] = "Critical" if ram > 92 else "High" if ram > 88 else "Medium"
        recovery_config["confidence"] = min(99, int((ram - 80) * 5))
        recovery_config["strategy"] = [
            "🔴 Close background applications consuming high memory",
            "🔴 Clear browser cache and close unused tabs",
            "🔴 Disable startup programs not in use",
            "🟡 Run automatic cleanup on temporary files",
            "🟡 Free up RAM by stopping non-essential services",
            "⚪ Consider system restart if memory remains above 90%"
        ]

    elif cpu > 85:
        recovery_config["active"] = True
        recovery_config["severity"] = "High"
        recovery_config["confidence"] = min(95, int((cpu - 80) * 4))
        recovery_config["strategy"] = [
            "Identify CPU-intensive processes using Task Manager",
            "Close or restart problematic applications",
            "Check for malware using Windows Defender",
            "Disable unnecessary background services"
        ]
    
    return recovery_config


def cleanup_downloads_junk(folder_path):
    deleted_files = []
    deleted_count = 0

    for root, _, files in os.walk(folder_path):
        for file_name in files:
            extension = os.path.splitext(file_name)[1].lower()
            if extension in JUNK_EXTENSIONS:
                file_path = os.path.join(root, file_name)
                try:
                    os.remove(file_path)
                    deleted_files.append(os.path.relpath(file_path, get_project_root()))
                    deleted_count += 1
                except Exception:
                    continue

    return deleted_count, deleted_files


def organize_downloads_folder(folder_path):
    moved_files = []
    categories = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
        "Documents": [".docx", ".doc", ".txt", ".pdf", ".pptx", ".xlsx"],
        "Videos": [".mp4", ".mkv", ".avi", ".mov"],
        "Code": [".py", ".cpp", ".c", ".java", ".js", ".ts", ".html", ".css"]
    }

    for root, _, files in os.walk(folder_path):
        if root == folder_path:
            for file_name in files:
                source_path = os.path.join(root, file_name)
                extension = os.path.splitext(file_name)[1].lower()
                category_folder = None

                for category, extensions in categories.items():
                    if extension in extensions:
                        category_folder = os.path.join(folder_path, category)
                        break

                if category_folder is None:
                    category_folder = os.path.join(folder_path, "Others")

                os.makedirs(category_folder, exist_ok=True)
                destination_path = os.path.join(category_folder, file_name)
                try:
                    shutil.move(source_path, destination_path)
                    moved_files.append(os.path.relpath(destination_path, get_project_root()))
                except Exception:
                    continue

    return moved_files


def execute_maintenance_cycle(cpu, ram, disk, downloads_folder, autonomous=False):
    before_junk_count, before_junk_size = scan_junk(downloads_folder)
    plan = generate_plan(cpu, ram, disk, before_junk_count)
    if not plan:
        plan = ["Review system status and maintain current configuration."]

    action_records = []
    current_stats = {
        "cpu": cpu,
        "ram": ram,
        "disk": disk,
        "junk_count": before_junk_count,
        "junk_size": before_junk_size
    }

    for item in plan:
        action_result = {
            "action": item,
            "status": "Skipped",
            "details": "No direct action performed.",
            "verification": None,
            "files": []
        }

        if "junk" in item.lower() or "cleanup" in item.lower():
            deleted_count, deleted_files = cleanup_downloads_junk(downloads_folder)
            after_junk_count, after_junk_size = scan_junk(downloads_folder)
            verification_status, improvement = verify_action(before_junk_count, after_junk_count)
            action_result.update({
                "status": "Completed",
                "details": f"Deleted {deleted_count} junk files.",
                "verification": {
                    "metric": "Junk Files",
                    "before": before_junk_count,
                    "after": after_junk_count,
                    "improvement": improvement,
                    "status": verification_status
                },
                "files": deleted_files
            })
            append_action_history(item, action_result["status"], deleted_files)
            current_stats["junk_count"] = after_junk_count
            current_stats["junk_size"] = after_junk_size

        elif "organize" in item.lower():
            moved_files = organize_downloads_folder(downloads_folder)
            action_result.update({
                "status": "Completed",
                "details": f"Organized {len(moved_files)} download items.",
                "verification": {
                    "metric": "Downloads Organization",
                    "before": None,
                    "after": None,
                    "improvement": len(moved_files),
                    "status": "Organized Files"
                },
                "files": moved_files
            })
            append_action_history(item, action_result["status"], moved_files)

        elif "memory" in item.lower() or "optimize" in item.lower():
            action_result.update({
                "status": "Recommended",
                "details": "Memory relief suggested through application management.",
                "verification": {
                    "metric": "RAM Usage",
                    "before": current_stats["ram"],
                    "after": current_stats["ram"],
                    "improvement": 0,
                    "status": "Recommendation Only"
                }
            })
            append_action_history(item, action_result["status"], [])

        else:
            append_action_history(item, action_result["status"], [])

        action_records.append(action_result)

    new_cpu = psutil.cpu_percent(interval=1)
    new_ram = psutil.virtual_memory().percent
    new_disk = psutil.disk_usage("C:\\").percent
    after_junk_count, after_junk_size = scan_junk(downloads_folder)

    overall_verification = {
        "cpu": verify_action(current_stats["cpu"], new_cpu),
        "ram": verify_action(current_stats["ram"], new_ram),
        "junk": verify_action(current_stats["junk_count"], after_junk_count)
    }

    return {
        "plan": plan,
        "actions": action_records,
        "before": current_stats,
        "after": {
            "cpu": new_cpu,
            "ram": new_ram,
            "disk": new_disk,
            "junk_count": after_junk_count,
            "junk_size": after_junk_size
        },
        "verification": overall_verification,
        "autonomous": autonomous
    }
