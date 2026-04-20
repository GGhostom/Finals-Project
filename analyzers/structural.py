def key_score(key_size):
    if key_size < 40:
        return 10
    elif key_size < 64:
        return 40
    elif key_size < 128:
        return 70
    else:
        return 90


def round_score(num_rounds):
    if num_rounds < 5:
        return 20
    elif num_rounds < 10:
        return 50
    else:
        return 80


def structure_score(spec):
    score = 0

    if spec.has_sbox:
        score += 30
    if spec.has_permutation:
        score += 30
    if "xor" in spec.operations:
        score += 10

    return score