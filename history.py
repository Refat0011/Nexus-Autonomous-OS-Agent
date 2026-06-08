import pandas as pd
import os


def save_history(
        cpu,
        ram,
        disk,
        health_score):

    data = {
        "CPU": [cpu],
        "RAM": [ram],
        "DISK": [disk],
        "HEALTH": [health_score]
    }

    df = pd.DataFrame(data)

    file_name = "history.csv"

    if os.path.exists(file_name):

        df.to_csv(
            file_name,
            mode="a",
            header=False,
            index=False
        )

    else:

        df.to_csv(
            file_name,
            index=False
        )