SBOX = {
    0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
    0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
    0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
    0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
}

INV_SBOX = {v: k for k, v in SBOX.items()}


def substitute(x):
    left = (x >> 4) & 0xF
    right = x & 0xF
    return (SBOX[left] << 4) | SBOX[right]


def inverse_substitute(x):
    left = (x >> 4) & 0xF
    right = x & 0xF
    return (INV_SBOX[left] << 4) | INV_SBOX[right]


def permute(x):
    perm = [1, 5, 2, 0, 3, 7, 4, 6]
    result = 0

    for i in range(8):
        bit = (x >> i) & 1
        result |= bit << perm[i]

    return result


def inverse_permute(x):
    perm = [3, 0, 2, 4, 6, 1, 7, 5]
    result = 0

    for i in range(8):
        bit = (x >> i) & 1
        result |= bit << perm[i]

    return result


def spn_encrypt(x, key=0b10101010):
    state = x

    for _ in range(3):
        state ^= key
        state = substitute(state)
        state = permute(state)

    return state


def spn_decrypt(x, key=0b10101010):
    state = x

    for _ in range(3):
        state = inverse_permute(state)
        state = inverse_substitute(state)
        state ^= key

    return state