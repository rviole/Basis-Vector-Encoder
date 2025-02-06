import numpy as np
from typing import List, Iterable

class Vector(np.ndarray):
    """
    A subclass of numpy.ndarray representing a 1D vector with validation. 
    Note: "1D vector" doesn't mean it has only one component, but it means it has only one dimension. 
    For example:
     - [1, 2, 3] or 
     - [1, 2, 3, 4, ..., n]
     - but not [[1, 2], [3, 4]]

    Args:
        data (Iterable): The input data to be converted into a Vector.

    Returns:
        Vector: A 1D numpy array with the name Vector.

    Raises:
        ValueError: If the input data is not 1D.
    """
    def __new__(cls, data: Iterable):
        validate_input(data, raise_exception=True)
        obj = np.asarray(data)

        # Flatten the input data to ensure it is 1D
        obj = obj.flatten()
        if obj.ndim != 1:
            raise ValueError(f"A Vector must be a 1D array, got {obj.ndim}D.")            

        return obj.view(cls)

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__repr__()

def map_string(string: str, symbol_mapping, UNK=None) -> List:
    """
    Maps a string to a list of corresponding values based on a symbol mapping.

    Args:
        string (str): The input string to be mapped.
        symbol_mapping (dict): A dictionary mapping symbols to their corresponding values.
        UNK: The value to use for unknown symbols. Defaults to the value for "UNK" in symbol_mapping or -1, if it exists. If symbol_mapping does not contain "UNK", -1 is used.

    Returns:
        List: A list of mapped values corresponding to the input string.
    """
    if UNK is None:
        UNK = symbol_mapping.get("UNK", -1)
        
    return [symbol_mapping.get(char, UNK) for char in string]

def is_square_matrix(matrix: np.ndarray) -> bool:
    """
    Checks if a given matrix is square-shaped.

    Args:
        matrix (np.ndarray): The input matrix to be checked.

    Returns:
        bool: True if the matrix is square, False otherwise.
    """
    if not isinstance(matrix, np.ndarray):
        matrix = np.array(matrix)
    return matrix.shape[0] == matrix.shape[1]

def validate_input(*input_data, raise_exception=True) -> bool:
    """
    Checks if any of the input data is None.

    Args:
        *input_data: Variable length input data to be checked.
        raise_exception (bool): Whether to raise an exception if any input is None. Defaults to True.

    Returns:
        bool: True if all input data is valid, False otherwise.

    Raises:
        ValueError: If any input data is None and raise_exception is True.
    """
    if any(each is None for each in input_data):
        if raise_exception:
            raise ValueError("No input provided.")
        return False
    return True

def is_dependent(matrix) -> bool:
    """
    Checks if the vectors (columns) in a matrix are linearly dependent.

    Args:
        matrix (np.ndarray): The input matrix to be checked.

    Returns:
        bool: True if the vectors are dependent, False otherwise.
    """
    rank = np.linalg.matrix_rank(matrix)
    vector_num = matrix.shape[1]  # col num = vector num

    return bool(rank < vector_num)

def is_basis(basis_matrix) -> bool:
    """
    Checks if a given matrix can form a basis (i.e., if the vectors (columns) in it are independent).

    Args:
        basis_matrix (np.ndarray): The input matrix to be checked.

    Returns:
        bool: True if the matrix can form a basis, False otherwise.
    """
    if not is_square_matrix(basis_matrix):
        return False
    return not is_dependent(basis_matrix)