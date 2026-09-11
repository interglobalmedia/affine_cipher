import string

from colorama import Fore, init

from affine_cipher.case import restore_char_case
from affine_cipher.key_validation import validate_affine_key


def affine_encryption(plaintext: str, a: int, b: int) -> str:
    # Define the uppercase alphabet.
    alphabet = string.ascii_uppercase
    # Get the length of the alphabet
    m = len(alphabet)
    validate_affine_key(a, m)
    # Initialize an empty string to store the ciphertext.
    ciphertext = ""
    # Iterate through each character in the plaintext.
    for char in plaintext:
        # Check if the character is in the alphabet.
        if char.upper() in alphabet:
            # If it's an alphabet letter, encrypt it.
            # Find the index of the character in the alphabet.
            p = alphabet.index(char.upper())
            # Apply the encryption formula: (a * p + b) mod m.
            c = (a * p + b) % m
            # Append the encrypted character to the ciphertext.
            transformed = alphabet[c]
            ciphertext += restore_char_case(char, transformed)
        else:
            # If the character is not in the alphabet, keep it unchanged.
            ciphertext += char
    # Return the encrypted ciphertext.
    return ciphertext


def run_encrypt(a: int, b: int) -> None:

    # Initialize Colorama
    init()

    # Define the plaintext and key components
    plaintext = input(f"{Fore.GREEN}[?] Enter text to encrypt: ")

    # Call the affine_crypt function with the specified parameters
    encrypted_text = affine_encryption(plaintext, a, b)
    # Print the original plaintext, the key components, and the encrypted text
    print(f"{Fore.MAGENTA}[+] Plaintext: {plaintext}")
    print(f"{Fore.GREEN}[+] Encrypted Text: {encrypted_text} ")
