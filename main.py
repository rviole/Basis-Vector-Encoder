import numpy as np
from typing import List
from tools import Vector, map_string, is_basis, validate_input
import json

with open("symbol_mapping.json", "r") as f:
    symbol_mapping = json.load(f)


raw_message: str = "Hey, Mike! How are you doing?"


def encrypt(
    raw_message: str, symbol_mapping: dict, basis=np.array([[1, 0], [0, 1]])
) -> List[Vector]:
    """
    Encrypts a raw message using a specified basis matrix and symbol mapping.

    Args:
        raw_message (str): The message to be encrypted.
        symbol_mapping (dict): A dictionary mapping symbols to their corresponding vector representations.
        basis (np.ndarray): A basis matrix used for the transformation. Defaults to the 2D identity matrix.

    Returns:
        List[Vector]: A list of transformed vectors representing the encrypted message.
    """
    validate_input(raw_message, symbol_mapping, basis)
    
    if not isinstance(basis, np.ndarray):
        basis = np.array(basis)
    if not is_basis(basis):
        raise ValueError("The basis is not a basis matrix. Probably dependent vectors.")
    basis_components = basis.shape[0]

    # Remove leading and trailing whitespaces from the message
    preprocessed_message = raw_message.strip()

    # Map each character to the corresponding mapping value
    mapped_message = map_string(preprocessed_message, symbol_mapping=symbol_mapping)

    # Pad each symbol to allign shape with basis vectors for linear transformation
    # for example
    # basis_components = 2
    # mapped_message = [1, 2, 3]
    # padded_message = [[1, 0], [2, 0], [3, 0]]
    padded_message = [
        [c] + [symbol_mapping.get("PAD", 0)] * (basis_components - 1)
        for c in mapped_message
    ]

    # Transform the each padded symbol to a vector (ndarray)
    vectorized_message = [Vector(p) for p in padded_message]

    # Transform the message using the basis matrix
    transformed_message = [
        Vector(np.dot(basis, vector)) for vector in vectorized_message
    ]

    return transformed_message


def decrypt(
    encrypted_message: List[Vector], basis, symbol_mapping: dict
) -> str:
    """
    Decrypts an encrypted message using a specified basis matrix and symbol mapping.

    Args:
        encrypted_message (List[Vector]): The encrypted message represented as a list of vectors.
        basis (np.ndarray): The basis matrix used for the inverse transformation.
        symbol_mapping (dict): A dictionary mapping symbols to their corresponding vector representations.

    Returns:
        str: The decrypted message as a string.
    """
    validate_input(encrypted_message, basis, symbol_mapping)
    
    if not is_basis(basis):
        raise ValueError("The basis is not a basis matrix. Probably dependent vectors.")

    try:
        inverse_trans_matrix = np.linalg.inv(basis)
    except np.linalg.LinAlgError:
        raise ValueError("The transformation matrix is not invertible.")

    
    # Use this to map the vectors back to symbols
    reverse_symbol_mapping = {v: k for k, v in symbol_mapping.items()} 
    
    
    # After inverse transformation we get the standard basis vectors (padded and in std basis)
    std_vectorized_message = [
        np.dot(inverse_trans_matrix, vector) for vector in encrypted_message
    ] 

    # Extract the first element of each vector and map it to a symbol (other elements are padding)
    decrypted_message = "".join(
        [
            reverse_symbol_mapping.get(vector[0], "UNK")
            for vector in std_vectorized_message
        ]
    ) 

    return decrypted_message


# Transformation matrix from Jenifer basis to Mike basis
# Basically, how Mike sees Jenifer's basis / Jenifer-to-Mike "language translation"
jenifer_to_mike_transformation = np.array([[1, 1], [1, -1]])

ecnrypted_message = encrypt(
    raw_message=raw_message,
    basis=jenifer_to_mike_transformation,
    symbol_mapping=symbol_mapping,
)
decrypted_message = decrypt(
    encrypted_message=ecnrypted_message,
    basis=jenifer_to_mike_transformation,
    symbol_mapping=symbol_mapping,
)

print("Encrypted message:", ecnrypted_message[:3], "...")
print("Decrypted message:", decrypted_message)
