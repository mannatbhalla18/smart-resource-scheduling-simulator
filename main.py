import random
from process import Process
from scheduler import fcfs_schedule, sjf_schedule, round_robin_schedule
from visualization import plot_full_dashboard

def clone_processes(processes):
    return [
        Process(p.pid, p.arrival_time, p.burst_time)
        for p in processes
    ]


def calculate_overall_metrics(processes):
    for p in processes:
        p.calculate_metrics()

    total_waiting = sum(p.waiting_time for p in processes)
    total_turnaround = sum(p.turnaround_time for p in processes)

    n = len(processes)

    avg_waiting = total_waiting / n
    avg_turnaround = total_turnaround / n

    total_burst = sum(p.burst_time for p in processes)
    total_time = max(p.finish_time for p in processes)

    cpu_utilization = (total_burst / total_time) * 100

    return avg_waiting, avg_turnaround, cpu_utilization

def generate_random_processes(n, max_arrival=10, max_burst=10):
    processes = []
    for i in range(1, n + 1):
        arrival = random.randint(0, max_arrival)
        burst = random.randint(1, max_burst)
        processes.append(Process(f"P{i}", arrival, burst))
    return processes

def main():
    n = int(input("Enter number of processes: "))
    runs = int(input("Enter number of simulations to run: "))
    time_quantum = int(input("Enter time quantum for Round Robin: "))

    fcfs_total = [0, 0, 0]
    sjf_total = [0, 0, 0]
    rr_total = [0, 0, 0]

    # These will store timelines from last run (for visualization)
    fcfs_timeline = []
    sjf_timeline = []
    rr_timeline = []

    for _ in range(runs):
        base_processes = generate_random_processes(n)

        # ---------------- FCFS ----------------
        fcfs_processes = clone_processes(base_processes)
        fcfs_order = fcfs_schedule(fcfs_processes)

        time = 0
        fcfs_timeline = []

        for p in fcfs_order:
            if time < p.arrival_time:
                time = p.arrival_time

            p.start_time = time
            fcfs_timeline.append((p.pid, time, time + p.burst_time))

            time += p.burst_time
            p.finish_time = time

        fcfs_metrics = calculate_overall_metrics(fcfs_order)

        # ---------------- SJF ----------------
        sjf_processes = clone_processes(base_processes)
        sjf_order = sjf_schedule(sjf_processes)

        time = 0
        sjf_timeline = []

        for p in sjf_order:
            if time < p.arrival_time:
                time = p.arrival_time

            p.start_time = time
            sjf_timeline.append((p.pid, time, time + p.burst_time))

            time += p.burst_time
            p.finish_time = time

        sjf_metrics = calculate_overall_metrics(sjf_order)

        # ---------------- Round Robin ----------------
        rr_processes = clone_processes(base_processes)
        rr_order, rr_timeline = round_robin_schedule(rr_processes, time_quantum)

        rr_metrics = calculate_overall_metrics(rr_order)

        # Accumulate totals
        for i in range(3):
            fcfs_total[i] += fcfs_metrics[i]
            sjf_total[i] += sjf_metrics[i]
            rr_total[i] += rr_metrics[i]

    # ---------------- Final Averaged Results ----------------
    print("\nAverage Performance Over", runs, "Simulations")
    print("------------------------------------------------------")
    print("Algorithm     Avg Waiting   Avg Turnaround   CPU Util")
    print("------------------------------------------------------")

    print(f"FCFS         {fcfs_total[0]/runs:<13.2f}{fcfs_total[1]/runs:<17.2f}{fcfs_total[2]/runs:.2f}%")
    print(f"SJF          {sjf_total[0]/runs:<13.2f}{sjf_total[1]/runs:<17.2f}{sjf_total[2]/runs:.2f}%")
    print(f"Round Robin  {rr_total[0]/runs:<13.2f}{rr_total[1]/runs:<17.2f}{rr_total[2]/runs:.2f}%")

    print("------------------------------------------------------")

    fcfs_avg = [fcfs_total[i] / runs for i in range(3)]
    sjf_avg = [sjf_total[i] / runs for i in range(3)]
    rr_avg = [rr_total[i] / runs for i in range(3)]

    plot_full_dashboard(fcfs_timeline,
                    sjf_timeline,
                    rr_timeline,
                    fcfs_avg,
                    sjf_avg,
                    rr_avg)

if __name__ == "__main__":
    main()