def extract_features(spec):
    return [
        spec.key_size,
        spec.block_size,
        spec.num_rounds,
        int(spec.has_sbox),
        int(spec.has_permutation),
        len(spec.operations),
    ]