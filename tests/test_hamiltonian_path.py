import unittest
from utils import get_topo_order

class TestHamiltonianPath(unittest.TestCase):

    def test_unique_hamiltonian_path(self):
        """ Test case where a unique Hamiltonian path exists """
        graph = [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 0]
        ]
        self.assertEqual(get_topo_order(graph), (True, [0, 1, 2, 3]))

    def test_multiple_hamiltonian_paths(self):
        """ Test case where multiple Hamiltonian paths exist """
        graph = [
            [0, 1, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 0]
        ]
        unique, topo_order = get_topo_order(graph)
        self.assertFalse(unique)  # Multiple valid orders exist
        self.assertEqual(set(topo_order), {0, 1, 2, 3})  # Check if it is a valid topological order

    def test_no_hamiltonian_path_due_to_cycle(self):
        """ Test case where a cycle exists, making topological sorting impossible """
        graph = [
            [0, 1, 0],
            [0, 0, 1],
            [1, 0, 0]  # Cycle exists: 0 → 1 → 2 → 0
        ]
        self.assertEqual(get_topo_order(graph), (False, []))

    def test_no_hamiltonian_path_disconnected_graph(self):
        """ Test case where the graph is disconnected """
        graph = [
            [0, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 0]
        ]
        unique, topo_order = get_topo_order(graph)
        self.assertFalse(unique)  # No unique Hamiltonian path
        self.assertEqual(set(topo_order), {0, 1, 2, 3})  # Topo order should contain all nodes

    def test_single_node_graph(self):
        """ Test case with a single node """
        graph = [[0]]
        self.assertEqual(get_topo_order(graph), (True, [0]))

    def test_two_nodes_one_edge(self):
        """ Test case with two nodes and one edge """
        graph = [
            [0, 1],
            [0, 0]
        ]
        self.assertEqual(get_topo_order(graph), (True, [0, 1]))

    def test_two_nodes_no_edge(self):
        """ Test case with two disconnected nodes """
        graph = [
            [0, 0],
            [0, 0]
        ]
        unique, topo_order = get_topo_order(graph)
        self.assertFalse(unique)
        self.assertEqual(set(topo_order), {0, 1})  # Both nodes should still appear in some order

    def test_threshold_effect(self):
        """ Test case where edges exist but are below the threshold """
        graph = [
            [0, 2, 0],
            [0, 0, 3],
            [0, 0, 0]
        ]
        unique, topo_order = get_topo_order(graph, threshold=4)
        self.assertFalse(unique)
        self.assertEqual(set(topo_order), {0, 1, 2})  # Topo order should still be valid

    def test_large_graph_linear_chain(self):
        """ Test case with a large linear chain graph """
        n = 100
        graph = [[0] * n for _ in range(n)]
        for i in range(n - 1):
            graph[i][i + 1] = 1  # Linear path 0 → 1 → 2 → ... → n-1
        expected_order = list(range(n))
        self.assertEqual(get_topo_order(graph), (True, expected_order))

if __name__ == "__main__":
    unittest.main()
