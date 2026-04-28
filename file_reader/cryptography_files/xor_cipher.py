KEY_TYPE = "int"
HAS_SBOX = False
HAS_PERMUTATION = False


def encryption(x, key):
    return (x ^ key) & 0xFF


def decryption(x, key):
    return (x ^ key) & 0xFF