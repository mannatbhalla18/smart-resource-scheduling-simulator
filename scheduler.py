def fcfs_schedule(processes):
    return sorted(processes, key=lambda p: p.arrival_time)


def sjf_schedule(processes):
    processes = sorted(processes, key=lambda p: p.arrival_time)
    ready_queue = []
    result = []
    time = 0

    while processes or ready_queue:
        # Add arrived processes to ready queue
        while processes and processes[0].arrival_time <= time:
            ready_queue.append(processes.pop(0))

        if ready_queue:
            # Pick process with smallest burst time
            ready_queue.sort(key=lambda p: p.burst_time)
            current = ready_queue.pop(0)
            result.append(current)
            time += current.burst_time
        else:
            # If no process has arrived, move time forward
            time = processes[0].arrival_time

    return result

def round_robin_schedule(processes, time_quantum):
    processes = sorted(processes, key=lambda p: p.arrival_time)
    ready_queue = []
    result = []
    time = 0
    timeline = []

    while processes or ready_queue:
        # Add newly arrived processes
        while processes and processes[0].arrival_time <= time:
            ready_queue.append(processes.pop(0))

        if ready_queue:
            current = ready_queue.pop(0)

            if current.start_time is None:
                current.start_time = time

            # ✅ DEFINE execution_time PROPERLY
            execution_time = min(time_quantum, current.remaining_time)

            # ✅ Store execution segment
            timeline.append((current.pid, time, time + execution_time))

            # Advance time
            time += execution_time
            current.remaining_time -= execution_time

            # Add any new arrivals during execution
            while processes and processes[0].arrival_time <= time:
                ready_queue.append(processes.pop(0))

            if current.remaining_time > 0:
                ready_queue.append(current)
            else:
                current.finish_time = time
                result.append(current)

        else:
            time = processes[0].arrival_time

    return result, timeline