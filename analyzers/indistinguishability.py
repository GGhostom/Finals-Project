from ml.cpa_tester import train_classifier


def compute_indistinguishability(encrypt_func):
    acc = train_classifier(encrypt_func)

    # convert accuracy → advantage
    advantage = abs(acc - 0.5) * 2  # scale to [0,1]

    # invert (higher = better)
    score = 1 - advantage

    return score