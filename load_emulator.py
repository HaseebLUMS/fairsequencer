import time
from typing import List
from error_distribution import Distribution
from message import Message

class LoadEmulator:
    def __init__(self, distribtuion: Distribution):
        self.distribution = distribtuion

    def get_messages(self, n, ts=None, step=1) -> List[Message]:
        if (ts is None): ts = time.time_ns()
        return [Message(ts + i * step + self.distribution.sample()) for i in range(n)]

    def get_messages_with_groundtruth(self, n, ts=None, step=1) -> tuple[List[Message], List[Message]]:
        if (ts is None): ts = time.time_ns()
        return ([Message(ts + i * step + self.distribution.sample()) for i in range(n)],
                [Message(ts + i * step) for i in range(n)])