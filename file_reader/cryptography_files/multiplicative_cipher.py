MOD = 256


def modinv(a, m):
    for i in range(m):
        if (a * i) % m == 1:
            return i
    return 1


def encryption(x, key):
    k = (key | 1) % MOD  # ensure odd (invertible)
    return (x * k) % MOD


def decryption(x, key):
    k = (key | 1) % MOD
    inv = modinv(k, MOD)
    return (x * inv) % MOD