KEY_TYPE = "int"
HAS_SBOX = False
HAS_PERMUTATION = True


def encryption(x, key):
    left = (x >> 4) & 0x0F
    right = x & 0x0F

    f = (right ^ key) & 0x0F

    return ((right << 4) | (left ^ f)) & 0xFF


def decryption(x, key):
    right = (x >> 4) & 0x0F
    left = x & 0x0F

    f = (left ^ key) & 0x0F

    return ((left << 4) | (right ^ f)) & 0xFF