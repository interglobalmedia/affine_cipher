from affine_cipher.decrypt import affine_decrypt
from affine_cipher.encrypt import affine_encryption


def test_roundtrip_encrypt_then_decrypt() -> None:

    ciphertext = affine_encryption("COTTAGE", 3, 10)

    assert ciphertext == "QAPPKCW"

    plaintext = affine_decrypt(ciphertext, 3, 10)

    assert plaintext == "COTTAGE"


def test_roundtrip_decrypt_then_encrypt() -> None:

    plaintext = affine_decrypt("QAPPKCW", 3, 10)

    assert plaintext == "COTTAGE"

    ciphertext = affine_encryption(plaintext, 3, 10)

    assert ciphertext == "QAPPKCW"
