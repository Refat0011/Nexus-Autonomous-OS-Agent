import os


JUNK_EXTENSIONS = {".tmp", ".log", ".bak"}


def scan_junk(folder_path):
    junk_count = 0
    total_size = 0

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            extension = os.path.splitext(file)[1].lower()
            if extension in JUNK_EXTENSIONS:
                junk_count += 1
                total_size += os.path.getsize(file_path)

    return junk_count, total_size


def clean_junk(folder):
    deleted = 0

    for root, _, files in os.walk(folder):
        for file in files:
            extension = os.path.splitext(file)[1].lower()
            if extension in JUNK_EXTENSIONS:
                try:
                    os.remove(os.path.join(root, file))
                    deleted += 1
                except Exception:
                    continue

    return deleted