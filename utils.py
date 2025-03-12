from collections import deque

def get_topo_order(graph, threshold=1) -> tuple[bool, list[int]]:
    """
    Given a graph represented as an adjacency matrix, returns a [is_there_unique_order, topological_order] tuple.
    """
    n = len(graph)
    in_degree = [0] * n
    adj_list = {i: [] for i in range(n)}

    # Build adjacency list and compute in-degrees
    for i in range(n):
        for j in range(n):
            if graph[i][j] >= threshold:  # Edge exists
                adj_list[i].append(j)
                in_degree[j] += 1

    # Start with nodes having in-degree 0
    queue = deque([node for node in range(n) if in_degree[node] == 0])
    topo_order = []
    unique = True  # Assume unique until proven otherwise

    while queue:
        if len(queue) > 1:
            unique = False  # More than one valid topological sort exists
        node = queue.popleft()
        topo_order.append(node)
        for neighbor in adj_list[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If the topological sort doesn't cover all nodes, return empty order
    if len(topo_order) != n:
        return (False, [])  # No valid topological order (cycle exists)

    # Check if the topological order forms a strict linear path
    for i in range(n - 1):
        if topo_order[i + 1] not in adj_list[topo_order[i]]:
            unique = False  # The order is not a strict linear path

    return (unique, topo_order)
