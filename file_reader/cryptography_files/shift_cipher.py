def encryption(x, key):
    return (x + key) % 256


def decryption(x, key):
    return (x - key) % 256