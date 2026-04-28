import math
from collections import Counter


def compute_entropy(ciphertexts):
    if not ciphertexts:
        return 0

    freq = Counter(ciphertexts)
    total = len(ciphertexts)

    entropy = 0.0
    for count in freq.values():
        p = count / total
        entropy -= p * math.log2(p)

    return entropy / math.log2(256)


def compute_avalanche(samples, encrypt_func, key):
    total_bits = 0
    changed_bits = 0

    for pt_bits, ct_bits in samples.pairs:
        pt = int(pt_bits, 2)

        for i in range(8):
            flipped = pt ^ (1 << i)
            new_ct = encrypt_func(flipped, key)
            new_bits = format(new_ct, "08b")

            for a, b in zip(ct_bits, new_bits):
                if a != b:
                    changed_bits += 1
            total_bits += 8

    return changed_bits / total_bits if total_bits else 0