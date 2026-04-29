# rotate_cipher.py

def encryption(x, r=2):
    return ((x << r) & 0xFF) | (x >> (8 - r))


def decryption(x, r=2):
    return ((x >> r) | (x << (8 - r))) & 0xFF