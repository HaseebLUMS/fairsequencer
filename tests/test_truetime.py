import unittest
from typing import List, NamedTuple
from truetime import truetime

# Define Message and Distribution classes
class Message(NamedTuple):
    ts: float

class Distribution(NamedTuple):
    stddev: float

class TestTrueTime(unittest.TestCase):
    
    def test_no_messages(self):
        self.assertEqual(truetime([], [], EDGE_THRESH=0.1), [])

    def test_single_message(self):
        self.assertEqual(truetime([Message(10)], [Distribution(1)], EDGE_THRESH=0.1), [[0]])

    def test_two_non_overlapping_messages(self):
        self.assertEqual(
            truetime([Message(10), Message(20)], [Distribution(1), Distribution(1)], EDGE_THRESH=0.1),
            [[0], [1]]
        )

    def test_two_overlapping_messages(self):
        self.assertEqual(
            truetime([Message(10), Message(11)], [Distribution(2), Distribution(2)], EDGE_THRESH=0.1),
            [[0, 1]]
        )

    def test_multiple_overlapping_messages(self):
        self.assertEqual(
            truetime([Message(10), Message(12), Message(14)], [Distribution(2), Distribution(2), Distribution(2)], EDGE_THRESH=0.1),
            [[0, 1, 2]]
        )

    def test_mixed_overlapping_and_non_overlapping_messages(self):
        self.assertEqual(
            truetime(
                [Message(10), Message(12), Message(30), Message(32)], 
                [Distribution(2), Distribution(2), Distribution(1), Distribution(1)], 
                EDGE_THRESH=0.1
            ),
            [[0, 1], [2, 3]]
        )

    def test_large_stddev_causing_full_overlap(self):
        self.assertEqual(
            truetime(
                [Message(10), Message(20), Message(30)], 
                [Distribution(15), Distribution(15), Distribution(15)], 
                EDGE_THRESH=0.1
            ),
            [[0, 1, 2]]
        )

    def test_edge_case_intervals_just_touching(self):
        self.assertEqual(
            truetime([Message(10), Message(16)], [Distribution(2), Distribution(2)], EDGE_THRESH=0.1),
            [[0, 1]]
        )

if __name__ == "__main__":
    unittest.main()