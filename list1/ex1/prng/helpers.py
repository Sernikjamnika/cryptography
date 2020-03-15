def extended_euclid(a, b):
    if a == 0:
        return (b, a, 1)
    else:
        divisor, x, y = extended_euclid(b % a, a)
        return (divisor, y - (b // a) * x, x)


def modular_inverse(value, modulus):
    divisor, inversed_value, _ = extended_euclid(value, modulus)
    if divisor == 1:
        return inversed_value % modulus
    raise Exception("Inverse does not exist")
