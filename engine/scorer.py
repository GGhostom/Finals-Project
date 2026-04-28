def compute_final_score(metrics):
    ind = getattr(metrics, "ind_score", 0.0)

    return (
        0.20 * metrics.entropy +
        0.25 * metrics.avalanche_score +
        0.15 * metrics.complexity_score +
        0.10 * metrics.structure_score +
        0.30 * ind
    )