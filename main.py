import os
import json
from tools import Vector
from typing import List, Literal

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

# make a padding function
# figure our what each function should return (types)
with open(SYMBOL_MAPPING_PATH) as file:
    SYMBOL_MAPPING = json.load(file)


def decode(encoded_message, basis):
    pass


message = (
    "Hello World, you are douchebad. HOw are you doing. How have you been. Im batman"
)
import numpy as np


def pad_symbol(symbol: str, padding_symbol, dimensions: int) -> List:
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
        padded_symbol = pad_symbol(
            
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
print(enc_msg)
print(dec_msg)
