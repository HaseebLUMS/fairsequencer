from collections import deque
from typing import List, Tuple
import time


def get_curr_time() -> int:
    '''in microseconds'''
    return time.time_ns() // 1000

def get_topo_order(graph: List[List[float]]) -> Tuple[bool, List[int]]:
    """
    Given a graph represented as an adjacency matrix, returns (is_there_unique_order, topological_order).
    """
    unique = True
    n = len(graph)
    in_degree = [0] * n
    adj_list = {i: [] for i in range(n)}

    # Build adjacency list and compute in-degrees
    for i in range(n):
        for j in range(i + 1, n):  
            if graph[i][j] > graph[j][i]:
                adj_list[i].append(j)
                in_degree[j] += 1

            elif graph[j][i] > graph[i][j]:
                adj_list[j].append(i)
                in_degree[i] += 1

            elif graph[i][j] == graph[j][i] == 0.5:
                adj_list[i].append(j)
                in_degree[j] += 1
                unique = False  # Multiple valid orders exist due to equal probability tie

    # Start with nodes having in-degree 0
    queue = deque([node for node in range(n) if in_degree[node] == 0])

    topo_order = []
    if len(queue) > 1:
        unique = False  # If multiple starting nodes or isolated nodes exist, uniqueness is False

    visited_count = 0  # Track number of nodes processed

    while queue:
        if len(queue) > 1:
            unique = False  # If multiple sources exist at any stage, uniqueness is False
        node = queue.popleft()
        topo_order.append(node)
        visited_count += 1

        for neighbor in adj_list[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If topological sort doesn't cover all nodes, return empty order (cycle detected)
    if visited_count != n:
        return (False, [])

    return (unique, topo_order)
