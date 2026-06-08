def generate_plan(cpu, ram, disk, junk_count):

    plan = []

    if ram > 85:
        plan.append(
            "Optimize memory usage"
        )

    if disk > 90:
        plan.append(
            "Perform storage cleanup"
        )

    if junk_count > 0:
        plan.append(
            f"Remove {junk_count} junk files"
        )

    plan.append(
        "Organize Downloads Folder"
    )

    return plan