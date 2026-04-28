import random


def generate_uniform_dataset(n=1000):
    return [0 for _ in range(n)]


def generate_random_dataset(n=1000):
    return [random.randint(0, 255) for _ in range(n)]


# def generate_cpa_dataset(encrypt_func, n=1000):
#     # Builds dataset:
#     # label 0 → uniform plaintext
#     # label 1 → random plaintext
#     data = []
#     labels = []
#     uniform = generate_uniform_dataset(n)
#     random_data = generate_random_dataset(n)
#     for pt in uniform:
#         ct = encrypt_func(pt)
#         data.append(ct)
#         labels.append(0)
#     for pt in random_data:
#         ct = encrypt_func(pt)
#         data.append(ct)
#         labels.append(1)
#     return data, labels