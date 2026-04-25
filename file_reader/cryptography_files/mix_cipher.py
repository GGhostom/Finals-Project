def mix_encrypt(x, key=7):
    x = (x + key) % 256
    x = x ^ (key << 2)
    x = (x * 3) % 256
    return x


def mix_decrypt(x, key=7):
    x = (x * 171) % 256  # inverse of 3 mod 256
    x = x ^ (key << 2)
    x = (x - key) % 256
    return x