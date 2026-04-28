def shift_encrypt(x, key=3):
    return (x + key) % 256


def shift_decrypt(x, key=3):
    return (x - key) % 256