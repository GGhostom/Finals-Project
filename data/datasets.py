import random


def uniform(n):
    return [0 for _ in range(n)]


def random_bytes(n):
    return [random.randint(0, 255) for _ in range(n)]


def patterned(n):
    return [i % 256 for i in range(n)]


def make_corpus(n=5000):
    return {
        "uniform": uniform(n),
        "random": random_bytes(n),
        "pattern": patterned(n),
    }