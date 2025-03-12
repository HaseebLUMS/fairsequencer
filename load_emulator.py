from typing import List
from error_distribution import Distribution
from message import Message
from utils import get_curr_time

class LoadEmulator:
    def __init__(self, distribtuion: Distribution):
        self.distribution = distribtuion

    def get_messages(self, n, ts=None, step=1) -> List[Message]:
        if (ts is None): ts = get_curr_time()
        return [Message(ts + i * step + self.distribution.sample(1)[0]) for i in range(n)]

    def get_messages_with_groundtruth(self, n, ts=None, step=1) -> tuple[List[Message], List[Message]]:
        '''
        Samples, Groundtruth
        '''
        if (ts is None): ts = get_curr_time()
        return [Message(ts + i * step + self.distribution.sample(1)[0]) for i in range(n)], [Message(ts + i * step) for i in range(n)]