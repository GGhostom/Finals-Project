from models.metrics import Metrics
from analyzers import statistical, structural, complexity
from engine import scorer, classifier
from utils.sample_generator import generate_samples


def compose_functions(cipher_funcs):
    def composed(x):
        for func in cipher_funcs:
            x = func(x)
        return x

    return composed


def analyze_layered_cipher(name, cipher_funcs, cipher_specs):
    composed_func = compose_functions(cipher_funcs)

    samples = generate_samples(composed_func)

    metrics = Metrics()

    # statistical
    metrics.avalanche_score = statistical.compute_avalanche(samples, composed_func)
    metrics.entropy = statistical.compute_entropy([ct for _, ct in samples.pairs])

    # combined key size
    total_key_size = sum(spec.key_size for spec in cipher_specs)
    metrics.key_score = structural.key_score(total_key_size)

    # structural diversity
    unique_ops = set()
    for spec in cipher_specs:
        unique_ops.update(spec.operations)

    metrics.structure_score = len(unique_ops) * 10

    # complexity
    time = complexity.brute_force_time(total_key_size)
    metrics.complexity_score = complexity.complexity_score(time)

    final_score = scorer.compute_final_score(metrics)
    classification = classifier.classify(final_score)

    return {
        "name": name,
        "metrics": metrics,
        "score": final_score,
        "classification": classification
    }