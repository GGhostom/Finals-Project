KEY_TYPE = "int"
HAS_SBOX = True
HAS_PERMUTATION = True


def encryption(x, key):
    return ((x ^ key) * 31) & 0xFF


def decryption(x, key):
    inv = pow(31, -1, 256)
    return (inv * x) ^ key