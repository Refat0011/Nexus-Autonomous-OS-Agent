from datetime import datetime


def write_log(message):

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("logs/system_log.txt", "a") as file:
        file.write(f"[{current_time}] {message}\n")