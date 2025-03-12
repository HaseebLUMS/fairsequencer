import unittest
from batching import get_batches

class TestGetBatches(unittest.TestCase):

    def test_basic_case(self):
        topo_order = [0, 1, 2, 3, 4]
        probabilities = [
            [0.0, 0.9, 0.1, 0.4, 0.8],
            [0.9, 0.0, 0.85, 0.2, 0.3],
            [0.1, 0.85, 0.0, 0.95, 0.05],
            [0.4, 0.2, 0.95, 0.0, 0.7],
            [0.8, 0.3, 0.05, 0.7, 0.0]
        ]
        edge_thresh = 0.2
        expected = [[0], [1], [2], [3], [4]]
        self.assertEqual(get_batches(topo_order, probabilities, edge_thresh), expected)

    def test_all_nodes_together(self):
        topo_order = [0, 1, 2, 3]
        probabilities = [
            [0.0, 0.9, 0.8, 0.95],
            [0.9, 0.0, 0.85, 0.9],
            [0.8, 0.85, 0.0, 0.9],
            [0.95, 0.9, 0.9, 0.0]
        ]
        edge_thresh = 1
        expected = [[0, 1, 2, 3]]  # All nodes form a single batch
        self.assertEqual(get_batches(topo_order, probabilities, edge_thresh), expected)

    def test_each_node_separate(self):
        topo_order = [0, 1, 2, 3]
        probabilities = [
            [0.0, 0.1, 0.1, 0.1],
            [0.1, 0.0, 0.1, 0.1],
            [0.1, 0.1, 0.0, 0.1],
            [0.1, 0.1, 0.1, 0.0]
        ]
        edge_thresh = 0
        expected = [[0], [1], [2], [3]]  # Each node forms its own batch
        self.assertEqual(get_batches(topo_order, probabilities, edge_thresh), expected)

    def test_empty_topo_order(self):
        topo_order = []
        probabilities = []
        edge_thresh = 0.5
        expected = []
        self.assertEqual(get_batches(topo_order, probabilities, edge_thresh), expected)

if __name__ == "__main__":
    unittest.main()
