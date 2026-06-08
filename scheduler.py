
import time


def start_scheduler(task_function):

    while True:

        task_function()

        print("\nNext check in 60 seconds...\n")

        time.sleep(60)