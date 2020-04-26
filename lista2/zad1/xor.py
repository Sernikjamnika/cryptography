import argparse


def main(args):
    output = bytes([ord(a) ^ ord(b) for a, b in zip(args.previous_iv, args.current_iv)])
    with open(args.output_path, mode="wb") as output_file:
        output_file.write(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--previous-iv", required=True, help="Previous nitial vector")
    parser.add_argument("--current-iv", required=True, help="New initial vector")
    parser.add_argument("--output-path", required=True, help="Path to output file")
    args = parser.parse_args()
    main(args)
