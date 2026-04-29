def encryption(x, key):
    b = format(x, "08b")
    return int(b[::-1], 2)


def decryption(x, key):
    return encryption(x, key)