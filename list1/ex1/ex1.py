import argparse

from prng.lcg import lcg, get_lcg_arguments


if __name__ == "__main__":
    seed = 1242
    generator = lcg(seed)
    random_values = [seed] + [next(generator) for _ in range(5)]

    print("Generated random values")
    print(random_values)
    predicted_modulus, predicted_mutliplier, predicted_increment = get_lcg_arguments(
        random_values
    )

    print("Predicted LCG arguments")
    print(
        f"Modulus: {predicted_modulus} | Multiplier: {predicted_mutliplier} | Increment: {predicted_increment}"
    )

    print("Next value of LCG")
    lcg_next_value = next(generator)
    print(lcg_next_value)
    print("Predicted next value")
    predicted_next_value = (random_values[-1] * predicted_mutliplier + predicted_increment) % predicted_modulus
    print(predicted_next_value)
    print(f"Is this LCG generated? {lcg_next_value == predicted_next_value}")
