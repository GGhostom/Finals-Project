# shift_cipher.py

def encryption(x, key=3):
    return (x + key) % 256


def decryption(x, key=3):
    return (x - key) % 256