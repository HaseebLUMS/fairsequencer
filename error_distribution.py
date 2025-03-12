import numpy as np

class Distribution:
    def sample(self, size):
        raise NotImplementedError("This method should be overridden by subclasses")

class GaussianDistribution(Distribution):
    def __init__(self, mean=0, stddev=1):
        self.mean = mean
        self.stddev = stddev

    def sample(self, size=1):
        return np.random.normal(self.mean, self.stddev, size)

class UniformDistribution(Distribution):
    def __init__(self, low=0, high=1):
        self.low = low
        self.high = high
    def sample(self, size=1):
            return np.random.uniform(self.low, self.high, size)

class ExponentialDistribution(Distribution):
    def __init__(self, scale=1):
        self.scale = scale

    def sample(self, size):
        return np.random.exponential(self.scale, size)