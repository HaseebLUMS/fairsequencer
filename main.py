from error_distribution import GaussianDistribution as Gus
from load_emulator import LoadEmulator as LE
from probability_model import ProbabilityModel as PM
from utils import get_topo_order

N = 3
EDGE_THRESH = 0.8

def main():
    dists = [Gus() for _ in range(N)] # create N error distribtions
    emulators = [LE(dist) for dist in dists]  # create N load emulators, each with a different error distribution
    messages = [em.get_messages(N) for em in emulators] # Get one message from each load emulator

    # pass the messages and error distributions to ProbabilityModel
    prob_model = PM()
    prob_matrix = prob_model.calculate_probability_matrix_dummy(messages, dists)

    # get the topological order
    unique, order = get_topo_order(prob_matrix, EDGE_THRESH)

    if unique: print("Unique Hamiltonian Path Exists")
    else: print("No, Unique Hamiltonian Path Does Not Exist")
    
    print("Order: ", order)

if __name__ == '__main__':
    main()