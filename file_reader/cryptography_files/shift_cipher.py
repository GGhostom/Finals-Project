KEY_TYPE = "int"
HAS_SBOX = False
HAS_PERMUTATION = False


def encryption(x, key):
    return (x + key) % 256


def decryption(x, key):
    return (x - key) % 256