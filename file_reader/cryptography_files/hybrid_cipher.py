def encryption(x, key):
    x = x ^ (key & 0xFF)
    x = ((x << 1) | (x >> 7)) & 0xFF
    x = (x + (key >> 1)) % 256
    return x


def decryption(x, key):
    x = (x - (key >> 1)) % 256
    x = ((x >> 1) | (x << 7)) & 0xFF
    x = x ^ (key & 0xFF)
    return x