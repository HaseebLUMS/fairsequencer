# fairsequencer
A Probabilistic Sequencer for Fair Total Ordering


First Experiment:

- Simulate everything to find out the number of batches created by my technique vs a naive technique like
    - true time intervals if overlapping, same batch
    - true time intervlas overlap provides probability then do batching using my algo

- See under several clock drfit distributions what are the resuls of the above

TODO:
Get messages from load_emulator, calculate probabilities, make a graph, get topo sort

## Run Tests
`python3 -m unittest discover -s tests`