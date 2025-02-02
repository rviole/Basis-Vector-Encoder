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


def is_square(matrix) -> bool:
    matrix = np.array(matrix)
    return matrix.shape[0] == matrix.shape[1]


def message_to_vectors(
    message: str,
    basis: np.ndarray = None,
    mapping: dict = SYMBOL_MAPPING,
    padding_symbol=PADDING_SYMBOL,
):
    if not isinstance(basis, np.ndarray):
        basis = np.array(basis)
        print(basis)
    if not is_square(basis):
        raise ValueError("Basis matrix must be square matrix")

    dimensions = basis.shape[0]

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

    # now lets transform vectors to basis
    vectors_in_basis = [basis @ v for v in vectors]

    return vectors_in_basis


def vectors_to_message(vectors: List[Vector], mapping=SYMBOL_MAPPING) -> str:
    def decode_vector_to_symbol(vector: Vector, mapping=mapping):
        reverse_mapping = {v: k for k, v in mapping.items()}
        decoded_symbol = reverse_mapping.get(vector[0])
        return decoded_symbol

    decoded_symbols = [decode_vector_to_symbol(vector) for vector in vectors]
    return "".join(decoded_symbols)


# Example #1
# Basis vectors of Jennifer
# Jenifer_bc = np.array([[1, 0], [0, 1]])

# Basis vectors of John in Jennifer's basis
# John_bc = np.array([[1, 1], [1, -1]])

# John's basis vectors represent a transformation to Jennifer's basis vectors
# Any vector in John's basis can be represented in Jennifer's basis using the transformation matrix [[1, 1], [1, -1]]
# it acts like a language translator between John and Jennifer's basis vectors (coordinate system)

# Example #2 - Practice

str_message = (
    "Hello Mike. This is my secret message. I hope you can decrypt it. Good luck!"
)
jenifer_basis_in_jennifer_basis = np.array([[1, 0], [0, 1]])
jenifer_basis_message = message_to_vectors(
    str_message, basis=jenifer_basis_in_jennifer_basis
)

transformation_jenifer_to_mike_basis = np.array([[1, 1], [1, -1]])

# Now we need to make a composition to:
# 1. Translate the message to vectors in std basis
# 2. Translate the message to vectors in Jennifer's basis
# 3. Translate the Jennifer's basis vectors to Mike's basis vectors

# Why we use composition of jenifers basis and transformation matrix?
# Because the vectorized message is in std basis. TO show that this message originates from Jenifer, we need to translate it to Jenifer's basis
# Then we use transformation matrix to translate it to Mike's basis
# So overall it is a composition of two transformations
# And to decrypt the message, we need to do the inverse of the composition
jenifer_message_in_mike_basis = [
    transformation_jenifer_to_mike_basis @ m for m in jenifer_basis_message
]

# Now we need to decrypt the message using the inverse of the composite transformation matrix


# Now we finished with translating the message from Jennifer's basis to Mike's basis
# Now the Mike will decrypt the message using the inverse of the composite transformation matrix (just like inverse language translator)
# in other words, he will do reverse enginnering to get the original message, by using the ivnerse of the transformation matrix.


# inverse composition
transformation_mike_to_jenifer_basis = np.linalg.inv(
    transformation_jenifer_to_mike_basis
)

# decrpyted message in Jennifer's basis (basically using reverse engineering)
jenifer_message_in_jennifer_basis = [
    transformation_mike_to_jenifer_basis @ m for m in jenifer_message_in_mike_basis
]


decrypte_message = vectors_to_message(jenifer_message_in_jennifer_basis)

print("Jennifer's original message: ", str_message)
print(
    "Jennifer's vectorized message in her basis: ",
    f"{jenifer_basis_in_jennifer_basis[:5]}...\n",
)

print(
    "Jennifer's vectorized message in Mike's basis: ",
    f"{jenifer_message_in_mike_basis[:5]}...\n",
)

print(
    "Mike's vectorized message in Jennifer's basis: ",
    f"{jenifer_message_in_jennifer_basis[:5]}...\n",
)


print("Decrypted message: ", decrypte_message)

# hERE IS the workflow
# 1. first we have a string message
# 2. we convert the message to vectorized message in standard basis
# 3. we convert the vectorized message to Jennifer's basis
# 4. we convert the vectorized message in Jennifer's basis to Mike's basis
# 5. Mike will decrypt the message by converting the message from Mike's basis to Jennifer's basis
# 6. Mike will convert the message from Jennifer's basis to standard basis
# 7. Mike will convert the message from standard basis to string message

# Why there is a standart basis intermediate step?
# Because the message is vectorized using integer mapping, which is a standard basis representation. So we need to convert it to Jennifer's basis to show that this message is from Jennifer

# How Mike will decrypt the message?
# There is a transformation matrix that represents Jeniifer's basis vectors in Mike's basis vectors. Mike will use the inverse of this transformation matrix to decrypt the message.
# So, if the transformation matrix translates between Jenifer's perspective to Mike's perspective, the inverse of this transformation matrix will translate between Mike's perspective to Jenifer's perspective
