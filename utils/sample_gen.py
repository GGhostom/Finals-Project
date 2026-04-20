from models.sample_set import SampleSet


def generate_samples(cipher_func, n=32, bits=8):
    samples = SampleSet()

    for i in range(n):
        pt = i % (2 ** bits)
        ct = cipher_func(pt)

        pt_bin = format(pt, f"0{bits}b")
        ct_bin = format(ct, f"0{bits}b")

        samples.add(pt_bin, ct_bin)

    return samples