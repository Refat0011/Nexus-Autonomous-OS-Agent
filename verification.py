def verify_action(before, after):

    if after < before:

        return (
            "Optimization Successful",
            before - after
        )

    return (
        "No Significant Improvement",
        0
    )