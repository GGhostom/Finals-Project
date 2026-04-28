KEY_TYPE = "int"
HAS_SBOX = False
HAS_PERMUTATION = True


def encryption(x, key):
    shifted = ((x << (key % 8)) | (x >> (8 - (key % 8)))) & 0xFF
    return shifted ^ key


def decryption(x, key):
    unxor = x ^ key
    r = key % 8
    return ((unxor >> r) | (unxor << (8 - r))) & 0xFF