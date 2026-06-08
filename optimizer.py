# optimizer.py

def optimize_system(cpu, ram):

    recommendations = []

    if cpu > 85:
        recommendations.append(
            "Close unnecessary applications to reduce CPU usage."
        )

    if ram > 85:
        recommendations.append(
            "Close memory-heavy applications."
        )

    if cpu > 70 and ram > 70:
        recommendations.append(
            "Consider restarting the system."
        )

    if not recommendations:
        recommendations.append(
            "System is performing normally."
        )

    return recommendations