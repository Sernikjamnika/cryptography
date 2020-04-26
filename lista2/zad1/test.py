from .main import encrypt_file, decrypt_file, ENCRYPTION_TYPES, get_encryption_key
from Crypto.Cipher import AES



def test_encrypt():
    input_file = "m.txt"
    encryption_type = "CBC"
    encryption_key = get_encryption_key(
        "aes-keystore.jck", "mystorepass", "jceksaes", "mykeypass"
    )
    iv = "2137832583667307"
    encrypt_file(
        input_file,
        "encrypted_" + input_file,
        AES.new(
            encryption_key._key,
            ENCRYPTION_TYPES[encryption_type],
            bytes(iv, encoding="utf-8"),
        ),
    )
    decrypt_file(
        "encrypted_" + input_file,
        "decrypted_" + input_file,
        AES.new(
            encryption_key._key,
            ENCRYPTION_TYPES[encryption_type],
            bytes(iv, encoding="utf-8"),
        ),
    )
    with open("m.txt") as file_1:
        with open("decrypted_m.txt") as file_2:
            assert file_1.readlines() == file_2.readlines()