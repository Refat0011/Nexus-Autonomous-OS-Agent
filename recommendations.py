def get_recommendation(cpu, ram, disk):

    recommendations = []

    if cpu > 80:
        recommendations.append(
            "Stop CPU-intensive applications."
        )

    if ram > 85:
        recommendations.append(
            "Close memory-heavy applications."
        )

    if disk > 90:
        recommendations.append(
            "Clean unnecessary files from storage."
        )

    if not recommendations:
        recommendations.append(
            "System is operating normally."
        )

    return recommendations