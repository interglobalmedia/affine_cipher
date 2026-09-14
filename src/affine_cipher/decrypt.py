import string

from colorama import Fore, init

from affine_cipher.case import restore_char_case
from affine_cipher.key_validation import validate_affine_key


# Function to get the Euclidean Algorithm
def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    extended Euclidean Algorithm to find the greatest common divisor and
    coefficients x, y such that ax + by = gcd(a, b)
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)


# function to get the modular inverse
def modular_inverse(a: int, m: int) -> int:
    """
    Compute the modular multiplicative inverse of a modulo m.
    Raises an exception if the modular inverse does not exist.
    """
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Modular inverse does not exist!")
    else:
        return x % m


# Function to decrypt our message
def affine_decrypt(ciphertext: str, a: int, b: int) -> str:
    """
    Decrypt a message with the Affine Cipher using the given key components a and b.
    """
    alphabet = string.ascii_uppercase
    m = len(alphabet)
    validate_affine_key(a, m)
    plaintext = ""
    # Compute the multiplicative inverse of a
    a_inv = modular_inverse(a, m)
    # Iterate through each character in the ciphertext
    for char in ciphertext:
        # Check if the character is in the alphabet
        if char.upper() in alphabet:
            # If it's an alphabet letter, decrypt it
            # Find the index of the character in the alphabet
            c = alphabet.index(char.upper())
            # Apply the decryption formula: a_inv * (c - b) mod m
            p = (a_inv * (c - b)) % m
            transformed = alphabet[p]
            # Append the decrypted character to the plaintext
            plaintext += restore_char_case(char, transformed)
        else:
            # If the character is not in the alphabet, keep it unchanged
            plaintext += char
    # Return the decrypted plaintext
    return plaintext


# Function to perform brute-force attack
def affine_brute_force(ciphertext: str) -> None:
    """
    Brute-force attack to find possible keys for an Affine Cipher and print
    potential decryptions for manual inspection.
    """
    alphabet = string.ascii_uppercase
    m = len(alphabet)
    # Iterate through possible values for a
    for a in range(1, m):
        # Ensure a and m are coprime
        if extended_gcd(a, m)[0] == 1:
            # Iterate through possible values for b
            for b in range(0, m):
                # Decrypt using the current key
                decrypted_text = affine_decrypt(ciphertext, a, b)
                # Print potential decryption for manual inspection
                print(f"Key a={a}, b={b}: {decrypted_text}")


def run_decrypt(a: int | None, b: int | None, brute_force: bool) -> None:
    # Initialize Colorama
    init()

    ciphertext = input(f"{Fore.GREEN}[?] Enter message to decrypt: ")
    if a is not None and b is not None:
        decrypted_text = affine_decrypt(ciphertext, a, b)
        print(f"{Fore.GREEN}[+] Decrypted Text: {decrypted_text} ")
    elif a is None and b is None and not brute_force:
        raise ValueError("Please either supply a key or --brute-force.")
    else:
        # Perform a brute-force attack to find a potential decrypted message.
        affine_brute_force(ciphertext)
