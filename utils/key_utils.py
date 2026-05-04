import random


def generate_key(key_size=8):
    return random.randint(0, 2**key_size - 1)

def generate_key_for_cipher(cipher_func):
    # simple default (you can improve later)
    return generate_key(8)