def analyze_system(cpu, ram, disk):

    observation = []
    decision = []

    if cpu > 85:
        observation.append("High CPU Usage")
        decision.append("Optimization Recommended")

    if ram > 85:
        observation.append("High RAM Usage")
        decision.append("Memory Optimization Recommended")

    if disk > 90:
        observation.append("Disk Almost Full")
        decision.append("Junk Cleanup Recommended")

    if not observation:
        observation.append("System Healthy")
        decision.append("No Action Needed")

    return observation, decision