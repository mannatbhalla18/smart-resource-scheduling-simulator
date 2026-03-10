class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority

        self.remaining_time = burst_time

        self.start_time = None
        self.finish_time = None
        self.waiting_time = None
        self.turnaround_time = None

    def calculate_metrics(self):
        self.turnaround_time = self.finish_time - self.arrival_time
        self.waiting_time = self.turnaround_time - self.burst_time