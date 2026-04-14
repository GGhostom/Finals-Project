from utils.bit_ops import *


def compute_avalanche(samples, encrypt_func):
    total_change = 0
    count = 0

    for pt, ct in samples.pairs:
        flipped = flip_one_bit(pt)
        new_ct = encrypt_func(flipped)

        diff = bit_difference(ct, new_ct)
        total_change += diff
        count += 1

    return total_change / count if count else 0


def compute_entropy(ciphertexts):
    from collections import Counter
    import math

    data = "".join(ciphertexts)
    freq = Counter(data)

    total = len(data)
    entropy = 0

    for f in freq.values():
        p = f / total
        entropy -= p * math.log2(p)

    return entropy


def compute_correlation(samples):
    correlations = []

    for pt, ct in samples.pairs:
        correlations.append(compare_bits(pt, ct))

    return average(correlations)