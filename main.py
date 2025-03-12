from typing import List
from error_distribution import GaussianDistribution as Gus
from load_emulator import LoadEmulator as LE
from probability_model import ProbabilityModel as PM
from message import Message
from batching import get_batches, pretty_print_batches
import utils

N = 5
EDGE_THRESH = 0.75

def main():
    dists = [Gus(0, 10) for _ in range(N)] # create N error distribtions
    emulators = [LE(dist) for dist in dists]  # create N load emulators, each with a different error distribution

    messages: List[Message] = []  # create a list of messages
    groundtruth: List[Message] = []  # create a list of groundtruths, i.e., messages with errors
    for em in emulators:
        samples, groundtruths = em.get_messages_with_groundtruth(1)
        messages.extend(samples)
        groundtruth.extend(groundtruths)

    assert len(messages) == len(dists) == len(groundtruth) == N

    # pass the messages and error distributions to ProbabilityModel
    prob_model = PM()
    prob_matrix = prob_model.calculate_probability_matrix_assuming_guassian(messages, dists)

    # get the topological order
    unique, order = utils.get_topo_order(prob_matrix)

    if unique:
        print("Unique Hamiltonian Path Exists")
        print("Order: ", order)
    else: print("No, Unique Hamiltonian Path Does Not Exist")

    batches = get_batches(order, prob_matrix, EDGE_THRESH)
    pretty_print_batches(batches)


    # 1. Compare with ground truth
    # We would never make i < j => i > j, we may make i < j => i = j (or WOULD WE?)
    # This is a boolean correctness check

    # 2. Check number of batches, more batches => better fairness
    # compare number of batches with a naive technique where any overlapping TrueTime intervals are batched together
    # This is quanititave comparison, showing fairness of one approach over the other

if __name__ == '__main__':
    main()