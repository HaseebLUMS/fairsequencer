import time
import unittest

from unittest.mock import MagicMock
from load_emulator import LoadEmulator
from error_distribution import Distribution

class TestLoadEmulator(unittest.TestCase):
    def setUp(self):
        self.distribution = MagicMock(spec=Distribution)
        self.distribution.sample.return_value = [0]
        self.emulator = LoadEmulator(self.distribution)

    def test_get_messages(self):
        messages = self.emulator.get_messages(5, ts=1000, step=10)
        self.assertEqual(len(messages), 5)
        self.assertEqual(messages[0].get_ts(), 1000)
        self.assertEqual(messages[1].get_ts(), 1010)
        self.assertEqual(messages[2].get_ts(), 1020)
        self.assertEqual(messages[3].get_ts(), 1030)
        self.assertEqual(messages[4].get_ts(), 1040)

    def test_get_messages_with_groundtruth(self):
        messages, groundtruth = self.emulator.get_messages_with_groundtruth(5, ts=1000, step=10)
        self.assertEqual(len(messages), 5)
        self.assertEqual(len(groundtruth), 5)
        for i in range(5):
            self.assertEqual(messages[i].get_ts(), groundtruth[i].get_ts())

    def test_get_messages_default_ts(self):
        self.distribution.sample.return_value = [5]
        messages = self.emulator.get_messages(3, step=10)
        current_ts = time.time_ns()
        self.assertTrue(all(msg.get_ts() <= current_ts for msg in messages))

    def test_get_messages_with_groundtruth_default_ts(self):
        self.distribution.sample.return_value = [5]
        messages, groundtruth = self.emulator.get_messages_with_groundtruth(3, step=10)
        current_ts = time.time_ns()
        self.assertTrue(all(msg.get_ts() <= current_ts for msg in messages))
        self.assertTrue(all(gt.get_ts() <= current_ts for gt in groundtruth))

        for msg, gt in zip(messages, groundtruth):
            self.assertEqual(msg.get_ts(), gt.get_ts() + 5)

if __name__ == '__main__':
    unittest.main()