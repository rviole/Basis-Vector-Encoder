import numpy as np
from typing import List
from tools import Vector, map_string, is_square_matrix, is_basis, validate_input
import json

with open("symbol_mapping.json", "r") as f:
    symbol_mapping = json.load(f)


raw_message: str = "Hello DImon, i am batman"


def encrypt(
    raw_message: str, symbol_mapping: dict, basis=np.array([[1, 0], [0, 1]])
) -> List[Vector]:
    if not isinstance(basis, np.ndarray):
        basis = np.array(basis)
    if not is_basis(basis):
        raise ValueError("The basis is not a basis matrix. Probably dependent vectors.")
    basis_components = basis.shape[0]

    # Transform the message to lower case and remove leading and trailing whitespaces
    preprocessed_message = raw_message.lower().strip()

    # Map each character to the corresponding mapping value
    mapped_message = map_string(preprocessed_message, symbol_mapping=symbol_mapping)
    # Pad each symbol to allign shape with basis vectors

    # for example
    # basis_components = 2
    # mapped_message = [1, 2, 3]
    # padded_message = [[1, 0], [2, 0], [3, 0]]
    padded_message = [
        [c] + [symbol_mapping.get("PAD", 0)] * (basis_components - 1)
        for c in mapped_message
    ]

    vectorized_message = [Vector(p) for p in padded_message]

    transformed_message = [
        Vector(np.dot(basis, vector)) for vector in vectorized_message
    ]

    return transformed_message


def decrypt(
    encrypted_message: List[Vector], basis_representation, symbol_mapping: dict
) -> str:
    if not is_basis(basis_representation):
        raise ValueError("The basis is not a basis matrix. Probably dependent vectors.")

    try:
        inverse_trans_matrix = np.linalg.inv(basis_representation)
    except np.linalg.LinAlgError:
        raise ValueError("The transformation matrix is not invertible.")

    reverse_symbol_mapping = {v: k for k, v in symbol_mapping.items()}
    std_vectorized_message = [
        np.dot(inverse_trans_matrix, vector) for vector in encrypted_message
    ]

    decrypted_message = "".join(
        [
            reverse_symbol_mapping.get(vector[0], "UNK")
            for vector in std_vectorized_message
        ]
    )

    return decrypted_message


# Transformation matrix from Jenifer to Mike
jenifer_to_mike_transformation = np.array([[1, 1], [1, -1]])

ecnrypted_message = encrypt(
    raw_message=raw_message,
    basis=jenifer_to_mike_transformation,
    symbol_mapping=symbol_mapping,
)
decrypted_message = decrypt(
    encrypted_message=ecnrypted_message,
    basis_representation=jenifer_to_mike_transformation,
    symbol_mapping=symbol_mapping,
)

print("Encrypted message:", ecnrypted_message[:3], "...")
print("Decrypted message:", decrypted_message)
