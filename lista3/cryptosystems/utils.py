import math
import random


def generate_coprime(number):
    coprime = random.randint(1, number - 1)
    while math.gcd(coprime, number) != 1:
        coprime = random.randint(1, number - 1)
    return coprime
