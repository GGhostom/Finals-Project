# multiplicative_cipher.py

MOD = 256
KEY = 5  # must be coprime with 256 (odd numbers usually ok)


def modinv(a, m):
    for i in range(m):
        if (a * i) % m == 1:
            return i
    return 1


def encryption(x):
    return (x * KEY) % MOD


def decryption(x):
    return (x * modinv(KEY, MOD)) % MOD