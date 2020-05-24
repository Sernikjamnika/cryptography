import random

from sympy import mod_inverse

from .utils import generate_coprime


def generate_private_key(sequence_length, sequence_variance, q_variance):
    def superincreasing_sequence(length, q_variance):
        sequence_sum = 0
        for _ in range(length):
            element = sequence_sum + random.randint(1, q_variance)
            yield element
            sequence_sum += element

    sequence = list(superincreasing_sequence(sequence_length, sequence_variance))
    q = sum(sequence) + random.randint(1, q_variance)
    r = generate_coprime(q)
    return sequence, q, r


def generate_public_key(sequence, q, r):
    return [(w * r) % q for w in sequence]


def generate_keys(sequence_length, sequence_variance, q_variance):
    private_key = generate_private_key(sequence_length, sequence_variance, q_variance)
    public_key = generate_public_key(*private_key)
    return private_key, public_key


def encrypt(message, public_key):
    binary_message = "".join(format(ord(m), "b") for m in message)
    if len(binary_message) > len(public_key):
        print("Public key too short")
    else:
        return sum(
            [
                int(bin_message_element) * public_key_element
                for bin_message_element, public_key_element in zip(
                    binary_message, public_key
                )
            ]
        )


def decrypt(message, sequence, q, r):
    max_sequence_value = (message * mod_inverse(r, q)) % q
    indices = []
    while max_sequence_value > 0:
        index = 0
        while sequence[index] <= max_sequence_value:
            index += 1
        indices.append(index - 1)
        max_sequence_value -= sequence[index - 1]

    binary_message = ""
    for index in range(indices[0] + 1):
        if index in indices:
            binary_message += "1"
        else:
            binary_message += "0"
    return "".join(chr(int("".join(r), 2)) for r in zip(*[iter(binary_message)] * 7))
