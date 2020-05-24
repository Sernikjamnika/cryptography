from cryptosystems.merkel_hellman import decrypt, encrypt, generate_keys


def print_commands():
    print("Commands:")
    print('"exit" for exit')
    print('"gen" for keys generation')
    print('"enc" for encryption')
    print('"dec" for decryption')


def cli():
    private_key, public_key = generate_keys(100, 12, 2)
    print_commands()
    while True:
        command = input("Command is ").strip()
        if command == "gen":
            sequence_length = int(input("Sequence length: "))
            sequence_variance = int(input("Sequence variance: "))
            q_variance = int(input("q variance: "))
            private_key, public_key = generate_keys(
                sequence_length, sequence_variance, q_variance
            )
            print(f"Public key is {public_key}")
        elif command == "enc":
            message = input("Plain text is ")
            print(f"Encrypted message is {encrypt(message, public_key)}")
        elif command == "dec":
            ciphertext = int(input("Ciphertext is "))
            print(f"Decrypted message is {decrypt(ciphertext, *private_key)}")
        elif command == "exit":
            return
        else:
            print("No such command")
            print_commands()


if __name__ == "__main__":
    cli()
