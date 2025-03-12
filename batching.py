from message import Message
from typing import List

def get_batches(topo_order: List[int], probabilities: List[List[float]], edge_thresh: float) -> List[List[int]]:
    '''
    Given a topological order and a probability matrix, return the batches of messages.
    '''
    if not topo_order:  # Handle empty case
        return []
    
    batches = []
    batch = [topo_order[0]]  # Start batch with the first node

    for i in range(len(topo_order) - 1):
        if probabilities[topo_order[i]][topo_order[i + 1]] < edge_thresh:
            batch.append(topo_order[i + 1])
        else:
            batches.append(batch)
            batch = [topo_order[i + 1]]

    batches.append(batch)
    return batches

def pretty_print_batches(batches: List[List[int]]):
    for i, batch in enumerate(batches):
        print(f"({batch})", end="   " )
    print()