# fairsequencer
A Probabilistic Sequencer for Fair Total Ordering


First Experiment:

- Simulate everything to find out the number of batches created by my technique vs a naive technique like
    - true time intervals if overlapping, same batch
    - true time intervlas overlap provides probability then do batching using my algo

- See under several clock drfit distributions what are the resuls of the above

Workflow:

    # create N error distribtions
    # create N load emulators
    # Get one message from each load emulator
    # pass the messages and error distributions to ProbabilityModel
    # ProbabilitModel returns a N*N probability matrix
    # Use this matrix to create a graph, where only edges with probability > `edge_thresh` are present
    # Get the topological sort of the matrix


March 13:
    # Dont use graph method, use wins counting method
    # Verify that probability based would lead to an ordering different from naive (rama) method

## Run Tests
`python3 -m unittest discover -s tests -f`