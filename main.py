import json
import numpy as np
from tools import Vector
from typing import List, Literal


# Load symbol mapping json file
SYMBOL_MAPPING_PATH = "./symbol_mapping.json"
with open(SYMBOL_MAPPING_PATH) as file:
    SYMBOL_MAPPING = json.load(file)


def vectorize_message_std(message: str, symbol_mapping) -> List[Vector]:
    """
    Converts a message to a list of vectors using the standard basis.

    Args:
        message (str): The message to be vectorized.
        symbol_mapping (dict): The mapping from symbols to vectors.

    Returns:
        List[Vector]: The vectorized message.
    """
    message = message.strip().lower()
    symbols = list(message)

    mapped_symbols = [
        symbol_mapping.get(symbol, symbol_mapping[" "]) for symbol in symbols
    ]

    vectors = [Vector(s) for s in mapped_symbols]
    return vectors


def stringify_vectors_std(vectors: List[Vector], symbol_mapping) -> str:
    """
    Converts a list of vectors back to a string using the standard basis.

    Args:
        vectors (List[Vector]): The list of vectors to be converted.
        symbol_mapping (dict): The mapping from vectors to symbols.

    Returns:
        str: The resulting string.
    """
    reversed_mapping = {v: k for k, v in symbol_mapping.items()}
    symbols = [reversed_mapping[vector[0]] for vector in vectors]
    return "".join(symbols)


message: str = "Hello World"
vectorized_out = vectorize_message_std(message, symbol_mapping=SYMBOL_MAPPING)
stringified_out = stringify_vectors_std(vectorized_out, symbol_mapping=SYMBOL_MAPPING)
print(vectorized_out)
print(stringified_out)


def encrypt_message(message:str, symbol_mapping, basis=None, ):
    """ 
    Applies a basis change to a message.

    Args:
        message (str): The message to be transformed.
        basis (np.ndarray): The basis matrix to be applied.
        symbol_mapping (dict): The mapping from symbols to vectors.

    Returns:
        List[Vector]: The transformed message.
    """
    vectors = vectorize_message_std(message, symbol_mapping)

    transformed_vectors = [basis @ v for v in vectors]

    return transformed_vectors

def decrypt_message(vectors, basis, symbol_mapping):
    """ 
    Applies the inverse basis change to a list of vectors.

    Args:
        vectors (List[Vector]): The list of vectors to be transformed.
        basis (np.ndarray): The basis matrix to be applied.
        symbol_mapping (dict): The mapping from vectors to symbols.

    Returns:
        str: The transformed message.
    """
    inverse_basis = np.linalg.inv(basis)
    transformed_vectors = [inverse_basis @ v for v in vectors]
    return stringify_vectors_std(transformed_vectors, symbol_mapping)



# add square matrix validation  