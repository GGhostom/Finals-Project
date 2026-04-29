# feistel_cipher.py

def round_func(x, key):
    return ((x ^ key) + 3) % 256


def encryption(x, key=13):
    left = (x >> 4) & 0x0F
    right = x & 0x0F

    for _ in range(2):
        new_left = right
        right = left ^ (round_func(right, key) & 0x0F)
        left = new_left

    return ((left << 4) | right)


def decryption(x, key=13):
    left = (x >> 4) & 0x0F
    right = x & 0x0F

    for _ in range(2):
        new_right = left
        left = right ^ (round_func(left, key) & 0x0F)
        right = new_right

    return ((left << 4) | right)