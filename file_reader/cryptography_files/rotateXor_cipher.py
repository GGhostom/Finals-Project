KEY_TYPE = "int"
HAS_SBOX = False
HAS_PERMUTATION = True


def encryption(x, key):
    r = key % 8
    return ((x << r) | (x >> (8 - r))) & 0xFF


def decryption(x, key):
    r = key % 8
    return ((x >> r) | (x << (8 - r))) & 0xFF & 0xFF