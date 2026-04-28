import random


def generate_key(cipher: "CipherSpec"):
    if cipher.key_type == "int":
        return random.randint(1, 255)

    if cipher.key_type == "tuple":
        return (
            random.randint(1, 255),
            random.randint(0, 255)
        )

    return random.randint(1, 255)