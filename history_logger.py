from datetime import datetime


def save_action(action, status=None, files=None):
    with open(
        "action_history.txt",
        "a",
        encoding="utf-8"
    ) as file:
        file.write(
            f"[{datetime.now()}] {action} | Status: {status or 'Unknown'} | Files: {', '.join(files) if files else 'None'}\n"
        )