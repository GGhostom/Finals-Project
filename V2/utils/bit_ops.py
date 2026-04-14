def bit_difference(a, b):
    return sum(x != y for x, y in zip(a, b))


def flip_one_bit(bits):
    bits = list(bits)
    bits[0] = '1' if bits[0] == '0' else '0'
    return "".join(bits)


def compare_bits(a, b):
    if len(a) != len(b):
        raise ValueError("Bit strings must be same length")
    same = sum(x == y for x, y in zip(a, b))
    return same / len(a)


def average(lst):
    return sum(lst) / len(lst) if lst else 0