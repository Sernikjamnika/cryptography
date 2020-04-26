import argparse
import os
import random

import jks
from Crypto.Cipher import AES


MODES = ("oracle", "challenge")
ENCRYPTION_TYPES = {
    "OFB": AES.MODE_OFB,
    "CTR": AES.MODE_CTR,
    "CBC": AES.MODE_CBC,
}


def get_encryption_key(key_store_name, key_store_password, key_id, key_password):
    key_store = jks.KeyStore.load(key_store_name, key_store_password)
    return key_store.secret_keys[key_id]


def encrypt_file(input_path, output_path, cipher):
    cipher_text = bytearray()
    with open(input_path, mode="rb") as input_file:
        text = input_file.read()
        chunks = [
            text[chunk_start : chunk_start + 16]
            for chunk_start in range(0, len(text), 16)
        ]
        for chunk in chunks:
            cipher_text.extend(cipher.encrypt(chunk))
    with open(output_path, mode="wb") as output_file:
        output_file.write(cipher_text)


def decrypt_file(input_path, output_path, cipher):
    cipher_text = bytearray()
    with open(input_path, mode="rb") as input_file:
        text = input_file.read()
        chunks = [
            text[chunk_start : chunk_start + 16]
            for chunk_start in range(0, len(text), 16)
        ]
        for chunk in chunks:
            cipher_text.extend(cipher.decrypt(chunk))
    with open(output_path, mode="w") as output_file:
        output_file.write(str(cipher_text, encoding="utf-8"))


def main(args):
    encryption_key = get_encryption_key(
        args.keystore_path, args.keystore_pass, args.key_id, args.key_pass
    )
    encryption_key.decrypt(args.key_pass)
    if args.mode == "oracle":
        for input_file in args.input_files:
            encrypt_file(
                input_file,
                "encrypted_" + input_file,
                AES.new(
                    encryption_key._key,
                    ENCRYPTION_TYPES[args.encryption_type],
                    bytes(args.iv, encoding="utf-8"),
                ),
            )
    else:
        input_file = random.choice(args.input_files[:2])
        encrypt_file(
            input_file,
            "encrypted_message.txt",
            AES.new(
                encryption_key._key,
                ENCRYPTION_TYPES[args.encryption_type],
                bytes(args.iv, encoding="utf-8"),
            ),
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--keystore_path", required=True, help="Path to keystore")
    parser.add_argument("--keystore_pass", required=True, help="Password to keystore")
    parser.add_argument("--key-id", required=True, help="Key identifier")
    parser.add_argument("--key-pass", required=True, help="Password to key")
    parser.add_argument(
        "--iv", required=True, help="Path to initial vector for encryption"
    )
    parser.add_argument("--mode", required=True, choices=MODES, help="Program mode")
    parser.add_argument(
        "--encryption-type",
        required=True,
        choices=ENCRYPTION_TYPES.keys(),
        help="Program mode",
    )
    parser.add_argument(
        "--input-files", required=True, help="Paths to input files", nargs="+"
    )
    args = parser.parse_args()
    main(args)
