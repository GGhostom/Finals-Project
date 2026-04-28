from utils.bit_ops import *


def compute_avalanche(samples, encrypt_func):
    total_changed = 0
    total_bits = 0

    for pt_bits, ct_bits in samples.pairs:
        pt_int = int(pt_bits, 2)

        for i in range(len(pt_bits)):
            flipped = pt_int ^ (1 << i)
            new_ct = encrypt_func(flipped)

            original = int(ct_bits, 2)
            new_ct_bits = format(new_ct, "08b")

            diff = sum(
                1 for a, b in zip(ct_bits, new_ct_bits) if a != b
            )

            total_changed += diff
            total_bits += len(ct_bits)

    if total_bits == 0:
        return 0

    return total_changed / total_bits


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


# def compute_correlation(samples):
#     correlations = []
#
#     for pt, ct in samples.pairs:
#         correlations.append(compare_bits(pt, ct))
#
#     return average(correlations)