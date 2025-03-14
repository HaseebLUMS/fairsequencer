from typing import List
from error_distribution import GaussianDistribution as Gus
from error_distribution import Distribution
from load_emulator import LoadEmulator as LE
from probability_model import ProbabilityModel as PM
from message import Message
from batching import get_batches, pretty_print_batches
import utils

LOG = False

def truetime(messages: List[Message], dists: List[Distribution], EDGE_THRESH: float) -> List[List[int]]:
    time_intervals = []
    for idx, (msg, dist) in enumerate(zip(messages, dists)):
        time_intervals.append((msg.ts - 3 * dist.stddev, msg.ts + 3 * dist.stddev, idx))

    # sort time intervals by start time
    time_intervals.sort(key=lambda x: x[0])

    # for all the overlapping intervals, create a batch
    batches = []
    current_batch = []
    current_end = -float('inf')
    for start, end, idx in time_intervals:
        if start >= current_end:
            if current_batch:
                batches.append(current_batch)
            current_batch = [idx]
            current_end = end
        else:
            current_batch.append(idx)
            current_end = max(current_end, end)
    if current_batch:
        batches.append(current_batch)

    return batches