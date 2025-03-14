from typing import List
from error_distribution import GaussianDistribution as Gus
from load_emulator import LoadEmulator as LE
from probability_model import ProbabilityModel as PM
from message import Message
from batching import get_batches, pretty_print_batches
import tommy
import truetime

N = 5
EDGE_THRESH = 0.75

def main():
    ###### Setup Load ######
    dists = [Gus(0, 2) for _ in range(N)] # create N error distribtions
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
    pretty_print_batches(tommy_batches)

    ###### Get TrueTime Ranking ######
    truetime_batches = truetime.truetime(messages=messages, dists=dists, EDGE_THRESH=EDGE_THRESH)
    pretty_print_batches(truetime_batches)

if __name__ == '__main__':
    main()