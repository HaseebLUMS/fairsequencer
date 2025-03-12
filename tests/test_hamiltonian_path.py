import unittest
from typing import List
from collections import deque
from utils import get_topo_order  # Assuming `get_topo_order` is in utils.py

class TestTopoSort(unittest.TestCase):

    def test_unique_linear_order(self):
        """ Test case where a unique topological order exists """
        graph = [
            [0, 0.9, 0, 0],
            [0, 0, 0.9, 0],
            [0, 0, 0, 0.9],
            [0, 0, 0, 0]
        ]
        self.assertEqual(get_topo_order(graph), (True, [0, 1, 2, 3]))

    def test_multiple_valid_orders(self):
        """ Test case where multiple valid topological orders exist """
        graph = [
            [0, 0.7, 0.7, 0],
            [0, 0, 0, 0.9],
            [0, 0, 0, 0.9],
            [0, 0, 0, 0]
        ]
        unique, topo_order = get_topo_order(graph)
        self.assertFalse(unique)  # Multiple valid orders exist
        self.assertEqual(set(topo_order), {0, 1, 2, 3})  # Ensure all nodes are included

    def test_cycle_detected(self):
        """ Test case where a cycle exists, making topological sorting impossible """
        graph = [
            [0, 0.9, 0],
            [0, 0, 0.9],
            [0.9, 0, 0]  # Cycle exists: 0 → 1 → 2 → 0
        ]
        self.assertEqual(get_topo_order(graph), (False, []))

    def test_disconnected_graph(self):
        """ Test case where the graph is disconnected """
        graph = [
            [0, 0.9, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0.9],
            [0, 0, 0, 0]
        ]
        unique, topo_order = get_topo_order(graph)
        self.assertFalse(unique)  # Disconnected graphs should not be unique
        self.assertEqual(set(topo_order), {0, 1, 2, 3})  # Ensure all nodes are included

    def test_single_node(self):
        """ Test case with a single node """
        graph = [[0]]
        self.assertEqual(get_topo_order(graph), (True, [0]))

    def test_two_nodes_one_edge(self):
        """ Test case with two nodes and one edge """
        graph = [
            [0, 0.9],
            [0, 0]
        ]
        self.assertEqual(get_topo_order(graph), (True, [0, 1]))

    def test_two_nodes_disconnected(self):
        """ Test case with two disconnected nodes """
        graph = [
            [0, 0],
            [0, 0]
        ]
        unique, topo_order = get_topo_order(graph)
        self.assertFalse(unique)  # Two disconnected nodes should have multiple valid orders
        self.assertEqual(set(topo_order), {0, 1})  # Should contain both nodes in some order

    def test_large_linear_chain(self):
        """ Test case with a large linear chain graph """
        n = 100
        graph = [[0] * n for _ in range(n)]
        for i in range(n - 1):
            graph[i][i + 1] = 0.9  # Linear path 0 → 1 → 2 → ... → n-1
        expected_order = list(range(n))
        self.assertEqual(get_topo_order(graph), (True, expected_order))

    def test_equal_probabilities(self):
        """ Test case where equal probabilities force arbitrary selection """
        graph = [
            [0, 0.5, 0],
            [0.5, 0, 0.5],
            [0, 0.5, 0]
        ]
        unique, topo_order = get_topo_order(graph)
        self.assertFalse(unique)  # Multiple valid orders exist
        self.assertEqual(set(topo_order), {0, 1, 2})  # Ensure all nodes are included

    def test_graph_with_terminal_node(self):
        """ Test case where a node has no outgoing edges but is not isolated """
        graph = [
            [0, 0.9, 0, 0],  
            [0, 0, 0.8, 0],  
            [0, 0, 0, 0.7],  
            [0, 0, 0, 0]  # Node 3 has no outgoing edges but is NOT isolated
        ]
        unique, topo_order = get_topo_order(graph)
        self.assertTrue(unique)  # There's only one valid order
        self.assertEqual(topo_order, [0, 1, 2, 3])  # Fixed order

if __name__ == "__main__":
    unittest.main()
