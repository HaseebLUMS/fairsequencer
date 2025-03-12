from typing import List
from load_emulator import Message
from error_distribution import Distribution
from scipy.stats import norm

class ProbabilityModel:
    def __init__(self): pass

    def calculate_probability_matrix_dummy(self, messages: List[Message], distributions: List[Distribution]) -> List[List[float]]:
        matrix = [[0.0 for _ in range(len(messages))] for _ in range(len(messages))]
        for i in range(len(messages)):
            for j in range(i+1, len(messages)):
                matrix[i][j] = 1.0
        return matrix
    
    def calculate_probability_matrix(self, messages: List[Message], distributions: List[Distribution]) -> List[List[float]]:
        raise "Not Implemented"

    def calculate_probability_matrix_assuming_guassian(self, messages: List[Message], distributions: List[Distribution]) -> List[List[float]]:
        n = len(messages)
        probability_matrix = [[0.0] * n for _ in range(n)]

        for i in range(n):
            for j in range(n):
                if i != j:
                    T_i, T_j = messages[i].get_ts(), messages[j].get_ts()
                    mu_i, mu_j = distributions[i].mean, distributions[j].mean
                    sigma_i, sigma_j = distributions[i].stddev, distributions[j].stddev

                    # Compute Z-score for normal CDF
                    # -------------------------------------------
                    # Z-score formula:
                    #   Z = (T_j - T_i + (μ_i - μ_j)) / sqrt(σ_i^2 + σ_j^2)
                    #
                    # Interpretation:
                    # - (T_j - T_i) is the observed timestamp difference.
                    # - (μ_i - μ_j) accounts for mean clock offsets.
                    # - sqrt(σ_i^2 + σ_j^2) combines both standard deviations.
                    #
                    # The Z-score standardizes this into a normal distribution, allowing us
                    # to compute the probability that T_i^* occurs before T_j^*.
                    # -------------------------------------------                    
                    z_score = 1.0 * (T_j - T_i + (mu_i - mu_j)) / ((sigma_i**2 + sigma_j**2) ** 0.5)

                    # Convert Z-score to probability using the normal CDF
                    probability_matrix[i][j] = norm.cdf(z_score)

        return probability_matrix
