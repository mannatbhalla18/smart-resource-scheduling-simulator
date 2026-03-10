import matplotlib.pyplot as plt
import numpy as np

# Fixed colors for processes
process_colors = {
    "P1": "#1f77b4",
    "P2": "#ff7f0e",
    "P3": "#2ca02c",
    "P4": "#d62728",
    "P5": "#9467bd",
    "P6": "#8c564b",
    "P7": "#e377c2"
}


def plot_full_dashboard(fcfs_timeline, sjf_timeline, rr_timeline,
                        fcfs_avg, sjf_avg, rr_avg):

    fig = plt.figure(figsize=(14, 10))

    # ---------- BAR GRAPH ----------
    ax_bar = plt.subplot2grid((4, 1), (0, 0))

    labels = ["Waiting Time (avg)", "Turnaround Time (avg)", "CPU Utilization (%)"]
    x = np.arange(len(labels))
    width = 0.25

    ax_bar.bar(x - width, fcfs_avg, width, label="FCFS")
    ax_bar.bar(x, sjf_avg, width, label="SJF")
    ax_bar.bar(x + width, rr_avg, width, label="Round Robin")

    ax_bar.set_title("Algorithm Performance Comparison")
    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels(labels)
    ax_bar.legend()
    ax_bar.grid(True)

    # ---------- Compute max timeline length ----------
    max_time = max(
        max(end for _, _, end in fcfs_timeline),
        max(end for _, _, end in sjf_timeline),
        max(end for _, _, end in rr_timeline)
    )

    # ---------- GANTT DRAW FUNCTION ----------
    def draw_gantt(ax, timeline, title):

        for pid, start, end in timeline:
            ax.broken_barh([(start, end - start)], (10, 8),
                           facecolors=process_colors.get(pid, "#999999"))

            ax.text(start + (end - start) / 2,
                    14,
                    pid,
                    ha='center',
                    va='center',
                    color='white',
                    fontweight='bold')

        ax.set_yticks([])
        ax.set_title(title)
        ax.set_xlim(0, max_time)
        ax.grid(True)

    # ---------- GANTT CHARTS ----------
    ax_fcfs = plt.subplot2grid((4, 1), (1, 0))
    draw_gantt(ax_fcfs, fcfs_timeline, "FCFS")

    ax_sjf = plt.subplot2grid((4, 1), (2, 0))
    draw_gantt(ax_sjf, sjf_timeline, "SJF")

    ax_rr = plt.subplot2grid((4, 1), (3, 0))
    draw_gantt(ax_rr, rr_timeline, "Round Robin")

    ax_rr.set_xlabel("Time")

    plt.tight_layout()

    # Save dashboard image automatically
    plt.savefig("scheduler_dashboard.png", dpi=300)

    plt.show()