def bitshuffle_encrypt(x):
    # reverse bits
    result = 0
    for i in range(8):
        bit = (x >> i) & 1
        result |= bit << (7 - i)

    return result


def bitshuffle_decrypt(x):
    # same as encrypt (self-inverse)
    result = 0
    for i in range(8):
        bit = (x >> i) & 1
        result |= bit << (7 - i)

    return result