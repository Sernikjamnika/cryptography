import typing
import math

from .helpers import modular_inverse


def lcg(seed: int) -> int:
    """
    Generates pseudo - random numbers as Linear Congruent Generator.
    """
    multiplier = 672257307069504227
    increment = 7382843889490247368
    modulus = 9223371036854775783
    while True:
        seed = (seed * multiplier + increment) % modulus
        yield seed


def get_increment(modulus: int, multiplier: int, generated_sequence: (int, int)) -> int:
    """
    Gets increment of LCG from given sequence, modulus and multiplier of LCG

    Utilizes fact that 
    increment  = sequence[1] - sequence[0] * multiplier (mod modulus)
    """
    first_value, second_value = generated_sequence[:2]
    return (second_value - first_value * multiplier) % modulus


def get_multiplier(modulus: int, generated_sequence: (int, int)) -> int:
    """
    Gets multiplier of LCG from given sequence and modulus of LCG.

    Utilizes fact that 
    sequence[2] - sequence[1] = multiplier * (sequence[1] - sequence[0]) (mod modulus)
    multiplier = (sequence[2] - sequence[1]) * (sequence[1] - sequence[0])^(-1) (mod modulus)
    """
    first_value, second_value, third_value = generated_sequence[:3]
    return (
        (third_value - second_value)
        * modular_inverse(second_value - first_value, modulus)
        % modulus
    )


def get_modulus(generated_sequence: typing.Tuple[int]) -> int:
    """
    Gets modulus of LCG from given sequence.

    Utilizes number theory fact that given few random multiples of n,
    there is a large probability that their gcd is equal to n. And fact
    that if and only if X = 0 (mod modulus) then X = k * modulus.

    So that transforms sequence into sequence of differences such that
    difference[0] = sequence[1] - sequence[0]
    and 
    difference[1] = sequence[2] - sequence[1] = 
    = multiplier * (sequence[1] - sequence[0]) (mod modulus)

    Then transforms differences to make them equivalent to 0 mod modulus.
    difference[2] * differnece[0] - difference[1]^2 = 
    = (multiplier * differnece[0])^2 - (multiplier * differnece[0])^2 = 0 (mod modulus)
    """
    differences = [
        value_next - value_now
        for value_now, value_next in zip(generated_sequence, generated_sequence[1:])
    ]
    modulus_multiplied_differences = [
        third * first - second ** 2
        for first, second, third in zip(differences, differences[1:], differences[2:])
    ]

    modulus = math.gcd(*modulus_multiplied_differences[:2])
    for difference in modulus_multiplied_differences[2:]:
        modulus = math.gcd(modulus, difference)
    return abs(modulus)


def get_lcg_arguments(generated_sequence: typing.Tuple[int]) -> (int, int, int):
    modulus = get_modulus(generated_sequence)
    multiplier = get_multiplier(modulus, generated_sequence[:3])
    increment = get_increment(modulus, multiplier, generated_sequence[:2])
    return modulus, multiplier, increment
