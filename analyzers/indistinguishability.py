from ml.cpa_tester import train_classifier


def compute_indistinguishability(encrypt_func, cipher_func):
    acc = train_classifier(encrypt_func, cipher_func)

    advantage = abs(acc - 0.5) * 2
    score = 1 - advantage

    return score