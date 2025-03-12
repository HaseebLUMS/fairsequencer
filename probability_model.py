from typing import List
from load_emulator import Message
from error_distribution import Distribution

class ProbabilityModel:
    def __init__(self): pass

    def calculate_probability_matrix_dummy(self, messages: List[Message], distributions: List[Distribution]) -> List[List[float]]:
        matrix = [[0.0 for _ in range(len(messages))] for _ in range(len(messages))]
        for i in range(len(messages)):
            for j in range(i+1, len(messages)):
                matrix[i][j] = 1.0
        return matrix
    
    def calculate_probability_matrix(self, messages: List[Message], distributions: List[Distribution]) -> List[List[float]]:
        return []