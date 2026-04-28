KEY_TYPE = "tuple"
HAS_SBOX = False
HAS_PERMUTATION = False


def encryption(x, key):
    a, b = key
    return (a * x + b) % 256


def decryption(x, key):
    a, b = key
    a_inv = pow(a, -1, 256)
    return (a_inv * (x - b)) % 256