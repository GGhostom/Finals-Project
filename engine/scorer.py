def compute_final_score(metrics):
    return (
        0.2 * metrics.key_score +
        0.2 * metrics.structure_score +
        0.2 * metrics.avalanche_score +
        0.2 * metrics.entropy +
        0.2 * metrics.complexity_score
    )