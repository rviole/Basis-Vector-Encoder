# Basis-Vector-Encoder

# 🚧🏗️ In Progress...


## 💼📈Portfolio-Project
This project encodes and decodes messages using basis vectors.


This project encodes and decodes messages using basis vectors. In simple terms, think of it as a way of transforming a message into a different 'language'—where each set of basis vectors represents a specific perspective or coordinate system. To decode the message, you need to have the appropriate 'translation'—the corresponding basis vectors from that same 'language.' 

While this project doesn't have much practical use, it serves as a portfolio piece to demonstrate my understanding of basis change, linear transformations, and mathematical concepts.



⚠️ Optimization Disclaimer
- "The code is intentionally not optimized for speed or compactness. The primary goal of this project is to clearly demonstrate the underlying mathema tical concepts and provide a detailed, step-by-step walkthrough of how basis change and linear transformations work. I prioritized readability and intuition over performance, as this project serves as a showcase of my understanding of these topics rather than a high-performance implementation."

🚦Limitations:
Only 1D/2D/3D basis vectors allowed - no zero or higher than 3D.

# Workflow

So, how the code works? Here is a step by step explanation.

1. The goal of a file is to encode a string message in specific coordinate system (described by specific basis matrix). Then we decode the same encoded message, using basis representation of that coordinate system in another coordinate system (Jenifer's basis vectors represented using Mike's basis vectors)

2. To do all of the described operations, first we need to map each symbol to a vector in space. For this, we read `symbol_mapping.json` which is file that mapps each symbol/token to an integer.
It also contains `UNK` (Unkown Token) and `PAD` (Padding Token). Mapping symbols in vectors in such way implicitly makes them in std basis.
```json
{
    "UNK": -1,
    "PAD": 70,
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
    "e": 5,
    ...
    "\\": 65,
    "|": 66,
    "`": 67,
    "~": 68,
    " ": 69

}
```

3. We use `encrypt()` functions  to map each symbol. Then we pad it based on the dimensions of the basis matrix provided (2, 3, ...). Then we vectorize them using `Vector` class and transform using new basis matrix.

4. In `decrypt()` function, we pass the encrypted message along with the same basis represenation of the basis we used to encode the message. Note: We must pass to `decrypt()` function the same basis change representaion matrix as to `encrypt()` function. That transformation matrix says "Jenifer's basis vectors in Mike's perspective/ described by vectors in the Mike's coordinate system".

Additional Notes:

- In this implementation, each symbol in the string corresponds to a single vector.
- Vector() class is a simple overlay  of np.ndarray with just a simple shape manipulation and clarity in names


Rememeber to include
- each symbol is 1 Vector
- we pad Vectors (with PADIDNG SYMBOL = -1) only to allign shapes with basis vectors. 

