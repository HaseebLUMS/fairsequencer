edge_thresh = 0.8

def main():
    # create N error distribtions
    # create N load emulators
    # Get one message from each load emulator
    # pass the messages and error distributions to ProbabilityModel
    # ProbabilitModel returns a N*N probability matrix
    # Use this matrix to create a graph, where only edges with probability > `edge_thresh` are present
    # Get the topological sort of the matrix
    pass

if __name__ == '__main__':
    main()