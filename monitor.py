import psutil


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def get_ram_usage():
    return psutil.virtual_memory().percent


def get_disk_usage():
    return psutil.disk_usage("C:\\").percent


def get_top_processes():
    processes = []

    for proc in psutil.process_iter():
        try:
            processes.append({
                "pid": proc.pid,
                "name": proc.name(),
                "memory": proc.memory_percent()
            })
        except:
            continue

    processes.sort(
        key=lambda x: x["memory"],
        reverse=True
    )

    return processes[:5]