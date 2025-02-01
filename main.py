import os
import json
from tools import Vector
from typing import List, Literal
import numpy as np

MESSAGE_PADDING = 50  # default
PADDING_SYMBOL = -1
env_value = os.getenv("MESSAGE_PADDING")
if env_value:
    try:
        MESSAGE_PADDING = int(env_value)
    except Exception as e:
        print(
            f"Invalid value for MESSAGE_PADDING: {env_value}. Using default value: {MESSAGE_PADDING}."
        )
        MESSAGE_PADDING = 50  # default

SYMBOL_MAPPING_PATH = "symbol_mapping.json"

with open(SYMBOL_MAPPING_PATH) as file:
    SYMBOL_MAPPING = json.load(file)


message = (
    "Hello World, you are douchebad. HOw are you doing. How have you been. Im batman"
)


def pad_encoded_symbol(symbol: str, padding_symbol, dimensions: int) -> List:
    return [symbol] + [padding_symbol] * (dimensions - 1)


def message_to_vectors(
    message: str,
    dimensions: Literal[1, 2, 3],
    mapping: dict = SYMBOL_MAPPING,
    padding_symbol=PADDING_SYMBOL,
):
    def encode_symbol_to_vector(
        symbol: str, mapping=mapping, padding_symbol=padding_symbol
    ):
        encoded_symbol = mapping.get(symbol, padding_symbol)

        # pad the encoded symbol to n components (add n-1 because we already have 1 component)
        padded_symbol = pad_encoded_symbol(
            symbol=encoded_symbol, padding_symbol=padding_symbol, dimensions=dimensions
        )

        return Vector(padded_symbol)

    if dimensions not in [1, 2, 3]:
        raise ValueError(f"Dimensions must be either 1, 2 or 3, got {dimensions}")
    sentences = message.lower().strip()
    symbols = list(sentences)
    vectors = [encode_symbol_to_vector(symbol) for symbol in symbols]

    return vectors


def vectors_to_message(vectors: List[Vector], mapping=SYMBOL_MAPPING) -> str:
    def decode_vector_to_symbol(vector: Vector, mapping=mapping):
        reverse_mapping = {v: k for k, v in mapping.items()}
        decoded_symbol = reverse_mapping.get(vector[0])
        return decoded_symbol

    decoded_symbols = [decode_vector_to_symbol(vector) for vector in vectors]
    return "".join(decoded_symbols)


enc_msg = message_to_vectors(message, 2)
dec_msg = vectors_to_message(enc_msg)
# print(enc_msg)
# print(dec_msg)

# Example #1
# Basis vectors of Jennifer
# Jenifer_bc = np.array([[1, 0], [0, 1]])

# Basis vectors of John in Jennifer's basis
# John_bc = np.array([[1, 1], [1, -1]])

# John's basis vectors represent a transformation to Jennifer's basis vectors
# Any vector in John's basis can be represented in Jennifer's basis using the transformation matrix [[1, 1], [1, -1]]
# it acts like a language translator between John and Jennifer's basis vectors (coordinate system)

# Example #2 - Practice

jenifer_str_message = "Hello Mike. This is my secret message. I hope you can decrypt it. Good luck!"
jenifer_vector_message = message_to_vectors(jenifer_str_message, 2)


jennifer_to_mike_transformation = np.array([[1, 1], [1, -1]])

jenifer_message_in_mike_basis = [jennifer_to_mike_transformation @ m for m in jenifer_vector_message]


# Now we finished with translating the message from Jennifer's basis to Mike's basis
# Now the Mike will decrypt the message using the inverse of the transformation matrix (just like inverse language translator)
# in other words, he will do reverse enginnering to get the original message, by using the ivnerse of the transformation matrix.

mike_to_jennifer_transformation = np.linalg.inv(jennifer_to_mike_transformation)
jenifer_message_in_jennifer_basis = [mike_to_jennifer_transformation @ m for m in jenifer_message_in_mike_basis]


print("Jennifer's original message: ", jenifer_str_message)
print("Jennifer's vectorized message in her basis: ", f"{jenifer_vector_message[:5]}...")

print("Jennifer's vectorized message in Mike's basis: ", f"{jenifer_message_in_mike_basis[:5]}...")
print("Mike's vectorized message in Jennifer's basis: ", f"{jenifer_message_in_jennifer_basis[:5]}...")





