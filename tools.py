import numpy as np
from typing import List


class Vector(np.ndarray):
    def __new__(cls, data):

        obj = np.asarray(data)

        # remove all dimensions of size 1 if not removed
        # shape (1,3,1) -> (3,)
        obj = obj.flatten()
        if obj.ndim != 1:
            raise ValueError(f"A Vector must be a 1D array, got {obj.ndim}D.")            

        return obj.view(cls)

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__repr__()



def map_string(string:str, symbol_mapping, UNK=None) -> List:
    if UNK is None:
        UNK = symbol_mapping.get("UNK", -1)
        
    return [symbol_mapping.get(char, UNK) for char in string]

def is_square_matrix(matrix: np.ndarray) -> bool:
    if not isinstance(matrix, np.ndarray):
        matrix = np.array(matrix)
    return matrix.shape[0] == matrix.shape[1]


# checks if any of the input data is None
def validate_input(*input_data, raise_exception=True) -> bool:
    if any(each is None for each in input_data):
        if raise_exception:
            raise ValueError("No input provided.")
        return False
    return True


def is_dependent(matrix) -> bool:
    rank = np.linalg.matrix_rank(matrix)
    vector_num = matrix.shape[1]  # col num = vector num

    return bool(rank < vector_num)

def is_basis(basis_matrix) -> bool:
    if not is_square_matrix(basis_matrix):
        return False
    return not is_dependent(basis_matrix)