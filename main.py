import random
from typing import List
from error_distribution import GaussianDistribution as Gus
from load_emulator import LoadEmulator as LE
from probability_model import ProbabilityModel as PM
from message import Message
from batching import get_batches, pretty_print_batches
import tommy
import truetime
import visualize_fairness
import visualize_correctness

N = 5
EDGE_THRESH = 0.75

def main():
    output1: List[List[List[int]]] = []
    output2: List[List[List[int]]] = []
    truths: List[List[List[int]]] = []

    for _ in range(500):
        ###### Setup Load ######
        dists = [Gus(random.randint(0, 30), random.randint(1, 10)) for _ in range(N)] # create N error distribtions
        emulators = [LE(dist) for dist in dists]  # create N load emulators, each with a different error distribution

        messages: List[Message] = []  # create a list of messages
        groundtruth: List[Message] = []  # create a list of groundtruths, i.e., messages with errors
        for em in emulators:
            samples, groundtruths = em.get_messages_with_groundtruth(1)
            messages.extend(samples)
            groundtruth.extend(groundtruths)

        assert len(messages) == len(dists) == len(groundtruth) == N

        ###### Get Tommy Ranking ######
        tommy_batches = tommy.tommy(messages=messages, dists=dists, EDGE_THRESH=EDGE_THRESH)
        output1.append(tommy_batches)

        ###### Get TrueTime Ranking ######
        truetime_batches = truetime.truetime(messages=messages, dists=dists, EDGE_THRESH=EDGE_THRESH)
        output2.append(truetime_batches)


        ###### Gather groundtruths ######
        sorted_indices = sorted(range(len(groundtruth)), key=lambda i: groundtruth[i].get_ts())
        truth_batches = [[sorted_indices[i]] for i in range(len(sorted_indices))]
        truths.append(truth_batches)

    ##### Visualize difference ######
    visualize_fairness.plot_fairness_heatmap(output1, output2)
    visualize_correctness.plot_ras_heatmap(output1, output2, truths)

if __name__ == '__main__':
    main()