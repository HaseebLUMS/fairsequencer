import numpy as np
import random
from typing import List
from error_distribution import GaussianDistribution as Gus
from load_emulator import LoadEmulator as LE
from message import Message
import tommy
import truetime
from utils import get_curr_time
from visualize_correctness import compute_ras
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

# Increase the font size
plt.rcParams.update({'font.size': 16})

# Parameters
N = 5
EDGE_THRESH = 0.75
RUNS_PER_CONFIG = 10

steps = [50]       # Step size variations
# steps = list(range(1, 50, 2))       # Step size variations
vars_ = list(range(1, 121, 2))       # Variance values
mean_range = (0, 20)                # Mean randomly sampled per run

def simulate_and_compute_ras(step, variance):
    ras_tommy_total = 0
    ras_tt_total = 0

    for _ in range(RUNS_PER_CONFIG):
        mean = random.randint(*mean_range)
        dists = [Gus(mean, variance) for _ in range(N)]
        emulators = [LE(dist) for dist in dists]

        messages: List[Message] = []
        groundtruth: List[Message] = []
        ts = get_curr_time()

        for ind, em in enumerate(emulators):
            samples, truths = em.get_messages_with_groundtruth(1, ts + ind * step)
            messages.extend(samples)
            groundtruth.extend(truths)

        tommy_batches = tommy.tommy(messages=messages, dists=dists, EDGE_THRESH=EDGE_THRESH)
        tt_batches = truetime.truetime(messages=messages, dists=dists, EDGE_THRESH=EDGE_THRESH)

        sorted_indices = sorted(range(len(groundtruth)), key=lambda i: groundtruth[i].get_ts())
        truth_batches = [[sorted_indices[i]] for i in range(len(sorted_indices))]

        ras_tommy_total += compute_ras(tommy_batches, truth_batches)
        ras_tt_total += compute_ras(tt_batches, truth_batches)

    return ras_tommy_total / RUNS_PER_CONFIG, ras_tt_total / RUNS_PER_CONFIG

# Run simulations
tommy_points = []
tt_points = []
step_sizes = []

total_runs = len(steps) * len(vars_)
counter = 1

for step in steps:
    for var in vars_:
        print(f"Running {counter}/{total_runs} — step={step}, var={var}")
        ras_tommy, ras_tt = simulate_and_compute_ras(step, var)
        tommy_points.append((var, ras_tommy))
        tt_points.append((var, ras_tt))
        step_sizes.append(step)
        counter += 1

# Normalize step sizes for marker size
min_step, max_step = min(steps), max(steps)
def scale_marker_size(step, base=30, scale=70):
    return base + scale * ((step - min_step) / (max_step - min_step))

import matplotlib.cm as cm

plt.figure(figsize=(7, 4))

# Normalize step size for both size and color
# norm = lambda step: (step - min_step) / (max_step - min_step)
tommy_cmap = cm.Greens
truetime_cmap = cm.Oranges

# Tommy (hollow circle with gradient edge color)
for (var, ras), step in zip(tommy_points, step_sizes):
    color = tommy_cmap(1000)
    # color = tommy_cmap(norm(step))
    plt.scatter(var, ras,
                marker='o',
                facecolors='none',
                edgecolors=color,
                # s=scale_marker_size(step),
                alpha=0.9,
                linewidths=1)

# TrueTime (hollow star with gradient edge color)
for (var, ras), step in zip(tt_points, step_sizes):
    color = truetime_cmap(1000)
    # color = truetime_cmap(norm(step))
    plt.scatter(var, ras,
                marker='*',
                facecolors='none',
                edgecolors=color,
                # s=scale_marker_size(step),
                alpha=0.9,
                linewidths=1)

plt.xlabel("Clocks (Std.) Deviation")
plt.ylabel("Fairness (RAS)")
# plt.grid(True, linestyle='--', alpha=0.5)

# Manual legend
legend_elements = [
    Line2D([0], [0], marker='*', color='darkorange', label='TrueTime',
           markerfacecolor='none', markersize=15, linestyle='None'),
    Line2D([0], [0], marker='o', color='green', label='Tommy',
           markerfacecolor='none', markersize=15, linestyle='None')
]

plt.legend(handles=legend_elements,
           loc='upper right',
        #    bbox_to_anchor=(0.5, 1.02),
           ncol=len(legend_elements),
        #    borderaxespad=0.,
           fontsize=14)

ax = plt.gca()

# Set outer box (spines) to gray
for spine in ax.spines.values():
    spine.set_edgecolor('lightblue')

plt.tight_layout()
plt.savefig("figs/ras.pdf", bbox_inches='tight')
# plt.savefig("figs/ras_step_variation.pdf", bbox_inches='tight')
# plt.show()