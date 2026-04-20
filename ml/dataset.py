import itertools
from analyzers.layered_analysis import analyze_layered_cipher


def generate_dataset(cipher_funcs, cipher_specs):
    data = []
    labels = []

    names = list(cipher_specs.keys())

    for combo in itertools.combinations(names, 2):
        funcs = [cipher_funcs[n] for n in combo]
        specs = [cipher_specs[n] for n in combo]

        result = analyze_layered_cipher(
            name="_".join(combo),
            cipher_funcs=funcs,
            cipher_specs=specs
        )

        score = result["score"]

        features = []
        for spec in specs:
            features.extend([
                spec.key_size,
                spec.block_size,
                spec.num_rounds,
                int(spec.has_sbox),
                int(spec.has_permutation),
                len(spec.operations),
            ])

        data.append(features)
        labels.append(score)

    return data, labels