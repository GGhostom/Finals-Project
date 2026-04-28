KEY_TYPE = "int"
HAS_SBOX = False
HAS_PERMUTATION = True


def encryption(x, key):
    # key can control mode (optional variation)
    if key % 2 == 0:
        return ((x << 4) | (x >> 4)) & 0xFF
    return x  # identity fallback (for diversity tests)


def decryption(x, key):
    # same operation is reversible
    if key % 2 == 0:
        return ((x << 4) | (x >> 4)) & 0xFF
    return x