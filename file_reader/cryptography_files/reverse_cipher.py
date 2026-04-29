# reverse_cipher.py

def encryption(x):
    b = format(x, "08b")
    return int(b[::-1], 2)


def decryption(x):
    return encryption(x)