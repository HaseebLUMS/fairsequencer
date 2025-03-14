from typing import List
from error_distribution import GaussianDistribution as Gus
from error_distribution import Distribution
from load_emulator import LoadEmulator as LE
from probability_model import ProbabilityModel as PM
from message import Message
from batching import get_batches, pretty_print_batches
import utils

LOG = False

def tommy(messages: List[Message], dists: List[Distribution], EDGE_THRESH: float) -> List[List[int]]:
    # pass the messages and error distributions to ProbabilityModel
    prob_model = PM()
    prob_matrix = prob_model.calculate_probability_matrix_assuming_guassian(messages, dists)

    # get the topological order
    # TODO: Actually counting wins and ordering by that is equivalent to getting topo order
    unique, order = utils.get_topo_order(prob_matrix)

    if LOG:
        if unique:
            print("Unique Hamiltonian Path Exists")
            print("Order: ", order)
        else: print("No, Unique Hamiltonian Path Does Not Exist")  # why does this ever happen?

    batches = get_batches(order, prob_matrix, EDGE_THRESH)
    if LOG: pretty_print_batches(batches)
    return batches