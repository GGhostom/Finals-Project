def compute_final_score(m):
    return (
        0.25 * m.entropy +
        0.25 * m.avalanche_score +
        0.20 * m.ind_score +
        0.15 * m.complexity_score +
        0.15 * m.structure_score
    )