def encryption(x, key):
    r = key % 8
    return ((x << r) & 0xFF) | (x >> (8 - r))


def decryption(x, key):
    r = key % 8
    return ((x >> r) | (x << (8 - r))) & 0xFF