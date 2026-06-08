from monitor import *

print("GhostHawk System Monitor")
print("-" * 30)

print("CPU Usage:", get_cpu_usage(), "%")
print("RAM Usage:", get_ram_usage(), "%")
print("Disk Usage:", get_disk_usage(), "%")

print("\nTop Processes:")

for process in get_top_processes():
    print(process)

from logger import write_log

write_log("GhostHawk monitoring started")

print("Log saved successfully.")

from monitor import *
from decision_engine import *

cpu = get_cpu_usage()
ram = get_ram_usage()
disk = get_disk_usage()

observation, decision = analyze_system(cpu, ram, disk)

print("\n[GhostHawk Analysis]\n")

print("Observation:")
for item in observation:
    print("-", item)

print("\nDecision:")
for item in decision:
    print("-", item)

from organizer import organize_downloads

organize_downloads("downloads_test")

print("Downloads organized successfully.")
from cleaner import scan_junk

junk_count, total_size = scan_junk("downloads_test")

print("\nJunk Analysis")
print("Junk Files:", junk_count)
print("Junk Size:", total_size, "bytes")
from optimizer import optimize_system

recommendations = optimize_system(cpu, ram)

print("\nOptimization Recommendations")

for item in recommendations:
    print("-", item)

def ghosthawk_cycle():

    cpu = get_cpu_usage()
    ram = get_ram_usage()
    disk = get_disk_usage()

    print("\n[GhostHawk Autonomous Check]")

    print("CPU:", cpu)
    print("RAM:", ram)
    print("Disk:", disk)

from scheduler import start_scheduler

start_scheduler(ghosthawk_cycle)