# hybrid_cipher.py

def encryption(x):
    x = x ^ 0x3A
    x = (x << 1 | x >> 7) & 0xFF
    return x


def decryption(x):
    x = (x >> 1 | x << 7) & 0xFF
    x = x ^ 0x3A
    return x