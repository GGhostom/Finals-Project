# xor_cipher.py

def encryption(x, key=42):
    return x ^ key


def decryption(x, key=42):
    return x ^ key