import os
import json
from tools import Vector

MESSAGE_PADDING = 50  # default
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
    mapping = json.load(file)

def pad(message|vector):
    pass

def encode(raw_message: str, basis):
    pass


def decode(encoded_message, basis):
    pass
