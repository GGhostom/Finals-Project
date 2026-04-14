def brute_force_time(key_size):
    ops = 2 ** key_size
    seconds = ops / 1e9
    return seconds


def complexity_score(seconds):
    if seconds < 1e6:
        return 10
    elif seconds < 1e12:
        return 50
    else:
        return 90