import itertools


def best_sequence_bruteforce(env, max_layers):
    best_score = float("-inf")
    best_seq = None
    n = len(env.ciphers)
    for L in range(1, max_layers + 1):
        for seq in itertools.permutations(range(n), L):
            score = env.evaluate_sequence(list(seq))
            if score > best_score:
                best_score = score
                best_seq = list(seq)

    return best_score, best_seq