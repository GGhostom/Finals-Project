from utils.bit_ops import *


def compute_avalanche(samples, encrypt_func):
    total_change = 0
    count = 0

    for pt, ct in samples.pairs:
        # convert string → int
        pt_int = int(pt, 2)
        ct_int = int(ct, 2)

        # flip bit in integer form
        flipped_int = pt_int ^ 1  # flip lowest bit

        new_ct_int = encrypt_func(flipped_int)

        # convert back to bit strings
        ct_bits = format(ct_int, "08b")
        new_ct_bits = format(new_ct_int, "08b")

        diff = sum(a != b for a, b in zip(ct_bits, new_ct_bits))

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