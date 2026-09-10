# Encrypting and Decrypting the Affine Cipher

This repository consists of a Python implementation of the Affine Cipher.

The Affine Cipher is a type of monoalphabetic substitution cipher that encrypts plaintext by substituting one alphabetical character for another. It uses a mathematical function to encrypt the plaintext.

## Table of Contents

- [Original state of the project](#original-state-of-the-project)
- [Current state of the project](#current-state-of-the-project)
    - [Project structure](#project-structure)
    - [encrypt_affine_cypher.py -> src/affine_cipher/encrypt.py](#encrypt_affine_cypherpy---srcaffine_cipherencryptpy)
    - [decrypt_affine_cipher.py -> src/affine_cipher/decrypt.py](#decrypt_affine_cipherpy---srcaffine_cipherdecryptpy)
    - [src/affine_cipher/cli.py](#srcaffine_cipherclipy)
- [Mathematical function to encrypt the plaintext manually](#mathematical-function-to-encrypt-the-plaintext-manually)
    - [Affine Cipher encryption example](#affine-cipher-encryption-example)
- [Mathematical function to decrypt the ciphertext manually](#mathematical-function-to-decrypt-the-ciphertext-manually)
- [Finding the modular multiplicative inverse of an integer](#finding-the-modular-multiplicative-inverse-of-an-integer)
    - [Affine Cipher decryption example](#affine-cipher-decryption-example)
- [Setup](#setup)
- [Using a script to encrypt plaintext](#using-a-script-to-encrypt-plaintext)
- [Using a script to decrypt ciphertext](#using-a-script-to-decrypt-ciphertext)
- [Cipher correctness](#cipher-correctness)
- [Testing](#testing)
- [Code quality machinery](#code-quality-machinery)
    - [Linting + formatting](#linting--formatting)
    - [Security](#security)
    - [Pre-commit hooks](#pre-commit-hooks)
    - [CI/CD](#cicd)
- [Footnotes](#footnotes)



## Original state of the project

Originally, the structure of the project was the following:

```
affine-cipher
├──decrypt_affine_cipher.py
└──encrypt_affine_cypher.py
```

The original scripts were:

```shell
python encrypt_affine_cypher.py
python decrypt_affine_cipher.py
```

No workflows, no linting, no testing, no dependencies installed except colorama and no dependency file (`colorama` isn't pinned anywhere). There was even a filename inconsistency.

`encrypt_affine_cypher.py` encrypted with a hardcoded (`a=3, b=10`) entered via `input()`. Only uppercase letters were transformed, everything else (including lowercase) passed through unchanged. There was no check that `a` and 26 were `coprime`.

`decrypt_affine_cipher.py` contained the real math, but the script only ever called `affine_brute_force`. There was no path to decrypt with a known key.

To view the original project, please visit [commit a2b3ddb](https://github.com/interglobalmedia/affine_cipher/tree/a2b3ddbb941839c6808b984149eef48425d45a19) on GitHub.

## Current state of the project

### Project structure

If you run tree -a -I 'htmlcov|Claude outputs|.coverage|test-notes.md|notes.md|output.txt|git-commit-messages.md|.pytest_cache|.ruff_cache|.mypy_cache|.DS_Store|.git|.venv|__pycache__|coverage.xml|dist' from the command line, filtering out the noise this diagram excludes, it results in the following:

```
.
├── .github
│   └── workflows
│       └── ci.yml
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── README.md
├── pyproject.toml
├── src
│   └── affine_cipher
│       ├── __init__.py
│       ├── cli.py
│       ├── decrypt.py
│       └── encrypt.py
├── tests
│   ├── test_cli.py
│   ├── test_decrypt.py
│   ├── test_encrypt.py
│   └── test_roundtrip.py
└── uv.lock

6 directories, 15 files
```
### encrypt_affine_cypher.py -> src/affine_cipher/encrypt.py

```
# encrypt_affine_cypher.py

import string
from colorama import init, Fore

# Initialize Colorama
init()
def affine_encryption(plaintext, a, b):
   # Define the uppercase alphabet.
   alphabet = string.ascii_uppercase
   # Get the length of the alphabet
   m = len(alphabet)
   # Initialize an empty string to store the ciphertext.
   ciphertext = ''
   # Iterate through each character in the plaintext.
   for char in plaintext:
       # Check if the character is in the alphabet.
       if char in alphabet:
           # If it's an alphabet letter, encrypt it.
           # Find the index of the character in the alphabet.
           p = alphabet.index(char)
           # Apply the encryption formula: (a * p + b) mod m.
           c = (a * p + b) % m
           # Append the encrypted character to the ciphertext.
           ciphertext += alphabet[c]
       else:
           # If the character is not in the alphabet, keep it unchanged.
           ciphertext += char
   # Return the encrypted ciphertext.
   return ciphertext
    
# Define the plaintext and key components
plaintext = input(f'{Fore.GREEN}[?] Enter text to encrypt: ')
a = 3
b = 10
# Call the affine_crypt function with the specified parameters
encrypted_text = affine_encryption(plaintext, a, b)
# Print the original plaintext, the key components, and the encrypted text
print(f'{Fore.MAGENTA}[+] Plaintext: {plaintext}')
print(f'{Fore.GREEN}[+] Encrypted Text: {encrypted_text} ')
```

```
# src/affine_cipher/encrypt.py

import string

from colorama import Fore, init


def affine_encryption(plaintext: str, a: int, b: int) -> str:
    # Define the uppercase alphabet.
    alphabet = string.ascii_uppercase
    # Get the length of the alphabet
    m = len(alphabet)
    # Initialize an empty string to store the ciphertext.
    ciphertext = ""
    # Iterate through each character in the plaintext.
    for char in plaintext:
        # Check if the character is in the alphabet.
        if char in alphabet:
            # If it's an alphabet letter, encrypt it.
            # Find the index of the character in the alphabet.
            p = alphabet.index(char)
            # Apply the encryption formula: (a * p + b) mod m.
            c = (a * p + b) % m
            # Append the encrypted character to the ciphertext.
            ciphertext += alphabet[c]
        else:
            # If the character is not in the alphabet, keep it unchanged.
            ciphertext += char
    # Return the encrypted ciphertext.
    return ciphertext


def run_encrypt() -> None:

    # Initialize Colorama
    init()

    # Define the plaintext and key components
    plaintext = input(f"{Fore.GREEN}[?] Enter text to encrypt: ")
    a = 3
    b = 10
    # Call the affine_crypt function with the specified parameters
    encrypted_text = affine_encryption(plaintext, a, b)
    # Print the original plaintext, the key components, and the encrypted text
    print(f"{Fore.MAGENTA}[+] Plaintext: {plaintext}")
    print(f"{Fore.GREEN}[+] Encrypted Text: {encrypted_text} ")
```

### decrypt_affine_cipher.py -> src/affine_cipher/decrypt.py

```
# decrypt_affine_cipher.py

import string
from colorama import init, Fore

# Initialize colorama
init()

# Function to get the Euclidean Algorithm
def extended_gcd(a, b):
    """
    extended Euclidean Algorithm to find the greatest common divisor and coefficients x, y such that ax + by = gcd(a, b)
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)
# function to get the modular inverse
def modular_inverse(a, m):
    """
    Compute the modular multiplicative inverse of a modulo m.
    Raises an exception if the modular inverse does not exist.
    """
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist!')
    else:
        return x % m
# Function to decrypt our message
def affine_decrypt(ciphertext, a, b):
    """
    Decrypt a message with the Affine Cipher using the given key components a and b.
    """
    alphabet = string.ascii_uppercase
    m = len(alphabet)
    plaintext = ''
    # Compute the multiplicative inverse of a
    a_inv = modular_inverse(a, m)
    # Iterate through each character in the ciphertext
    for char in ciphertext:
        # Check if the character is in the alphabet
        if char in alphabet:
            # If it's an alphabet letter, decrypt it
            # Find the index of the character in the alphabet
            c = alphabet.index(char)
            # Apply the decryption formula: a_inv * (c - b) mod m
            p = (a_inv * (c - b)) % m
            # Append the decrypted character to the plaintext
            plaintext += alphabet[p]
        else:
            # If the character is not in the alphabet, keep it unchanged
            plaintext += char
    # Return the decrypted plaintext
    return plaintext
# Function to perform brute-force attack
def affine_brute_force(ciphertext):
    """
    Brute-force attack to find possible keys for an Affine Cipher and print potential decryptions for manual inspection.
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
                print(f'Key a={a}, b={b}: {decrypted_text}')
ciphertext = input(f'{Fore.GREEN}[?] Enter message to decrypt: ')
# Perform a brute-force attack to find a potential decrypted message.
affine_brute_force(ciphertext)
```

```
# src/affine_cipher/decrypt.py

import string

from colorama import Fore, init


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
    plaintext = ""
    # Compute the multiplicative inverse of a
    a_inv = modular_inverse(a, m)
    # Iterate through each character in the ciphertext
    for char in ciphertext:
        # Check if the character is in the alphabet
        if char in alphabet:
            # If it's an alphabet letter, decrypt it
            # Find the index of the character in the alphabet
            c = alphabet.index(char)
            # Apply the decryption formula: a_inv * (c - b) mod m
            p = (a_inv * (c - b)) % m
            # Append the decrypted character to the plaintext
            plaintext += alphabet[p]
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


def run_decrypt() -> None:
    # Initialize colorama
    init()

    ciphertext = input(f"{Fore.GREEN}[?] Enter message to decrypt: ")
    # Perform a brute-force attack to find a potential decrypted message.
    affine_brute_force(ciphertext)
```

### src/affine_cipher/cli.py

```
import argparse

from affine_cipher.decrypt import run_decrypt
from affine_cipher.encrypt import run_encrypt


def main() -> None:

    parser = argparse.ArgumentParser(prog="affine-cipher")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("encrypt")
    subparsers.add_parser("decrypt")

    args = parser.parse_args()

    if args.command == "encrypt":
        run_encrypt()
    elif args.command == "decrypt":
        run_decrypt()
```

## Mathematical function to encrypt the plaintext manually

The mathematical function used to encrypt the plaintext:

```
c = (a * p + b) % m
```

Where `c` is the numerical position of the resulting ciphertext character, `a` must be a `coprime`[^1] of `m` (which represents the size of the alphabet). `b` can be any integer. `p` represents the numerical position based on a zero index of the character being encrypted in the alphabet.

### Affine Cipher encryption example

Let's say `a = 3`, and `b = 10`. `a` has a valid value, because it is a `coprime` of 26. Valid values for a are: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, and 25. And let's say the `plaintext` I want to encrypt is `"HELLO"`.

```
# calculation for H (p = 7):

c = (3 * 7 + 10) % 26

c = 31 % 26 

c = 5 -> F

# calculation for E (p = 4):

c = (3 * 4 + 10) % 26

c = (12 + 10) % 26

c = 22 mod 26

c = 22 -> W

# calculation for L (p = 11):

c = (3 * 11 + 10) % 26

c = 43 mod 26 

c = 17 -> R

# calculation for L (p = 11):

c = (3 * 11 + 10) % 26

c = 43 mod 26

c =  17 -> R

# calculation for O (p = 14):

c = (3 * 14 + 10) % 26

c = 52 mod 26

c = 0 -> A
```

## Mathematical function to decrypt the ciphertext manually

Manually decrypting the ciphertext into plaintext is more complicated than encrypting the plaintext into ciphertext.

The mathematical function used to manually decrypt the the ciphertext:

```
p = a⁻¹ * (c - b) mod 26
```

## Finding the modular multiplicative inverse of an integer

What is `a⁻¹` and how do I calculate it?

In modular arithmetic, `a⁻¹` means the modular multiplicative inverse of an integer.

Basically, I am looking for a whole number that, when multiplied by a, leaves a remainder of 1 when divided by 26.

The mathematical function for calculating the modular inverse is:

(a * x)(mod 26) = 1

Where x is the modular inverse of a.

### Affine Cipher decryption example

Let's say `a = 3`, and `b = 10`. `a` has a valid value, because it is a `coprime` of 26. And let's say the ciphertext I want to decrypt is "FWRRA".

To calculate the modular inverse of a:

```
(3 * x) (mod 26) = 1
(3 * 9) mod 26 = 1
27 mod 26 = 1
```

To decrypt the ciphertext character F (c = 5):

```
p = a⁻¹ * (c - b) mod 26

p = 9 * (5 - 10) mod 26

p = 9 * (-5) mod 26

p = -45 mod 26 = 7 (-45 + 26 + 26 = 7)

7 = H
```

To decrypt the ciphertext character W (c = 22):

```
p = a⁻¹ * (c - b) mod 26

p = 9 * (22 - 10) mod 26

p = 9 * (12) mod 26 = 108 mod 26

p = 108 mod 26 = 4 (108 -104)

4 = E
```

To decrypt the ciphertext R (c = 17):

```
p = a⁻¹ * (c - b) mod 26

p = 9 * (17 - 10) mod 26

p = 9 * (7) mod 26 = 63 mod 26

p = 63 mod 26 = 2 -> 63 - 52 (26 * 2) = 11

11 = L
```

To decrypt the ciphertext R (c = 17):

```
p = a⁻¹ * (c - b) mod 26

p = 9 * (17 - 10) mod 26

p = 9 * (7) mod 26 = 63 mod 26

p = 63 mod 26 = 2 -> 63 - 52 (26 * 2) = 11

11 = L
```

To decrypt ciphertext A (c = 0):

```
p = a⁻¹ * (c - b) mod 26

p = 9 * (0 - 10) mod 26

p = 9 * (-10) mod 26

p = -90 mod 26 = (-90 + 26 + 26 + 26 + 26 = 14)

14 = O
```

## Setup

```shell
git clone https://github.com/interglobalmedia/affine_cipher.git
cd affine_cipher
uv sync
```

## Using a script to encrypt plaintext

You don't have to encrypt plaintext manually. This project provides a script that will do it for you:

```shell
uv run affine-cipher encrypt # then press return
```

This returns:

```shell
[?] Enter text to encrypt: HELLO # then press return
[+] Plaintext: HELLO
[+] Encrypted Text: FWRRA
```

## Using a script to decrypt ciphertext

You don't have to decrypt plaintext manually. This project provides a script that will do it for you:

```shell
uv run affine-cipher decrypt # then press return
[?] Enter message to decrypt: FWRRA
# which results in the output:
Key a=1, b=0: FWRRA
Key a=1, b=1: EVQQZ
Key a=1, b=2: DUPPY
Key a=1, b=3: CTOOX
Key a=1, b=4: BSNNW
Key a=1, b=5: ARMMV
Key a=1, b=6: ZQLLU
Key a=1, b=7: YPKKT
Key a=1, b=8: XOJJS
Key a=1, b=9: WNIIR
Key a=1, b=10: VMHHQ
Key a=1, b=11: ULGGP
Key a=1, b=12: TKFFO
Key a=1, b=13: SJEEN
Key a=1, b=14: RIDDM
Key a=1, b=15: QHCCL
Key a=1, b=16: PGBBK
Key a=1, b=17: OFAAJ
Key a=1, b=18: NEZZI
Key a=1, b=19: MDYYH
Key a=1, b=20: LCXXG
Key a=1, b=21: KBWWF
Key a=1, b=22: JAVVE
Key a=1, b=23: IZUUD
Key a=1, b=24: HYTTC
Key a=1, b=25: GXSSB
Key a=3, b=0: TQXXA
Key a=3, b=1: KHOOR
Key a=3, b=2: BYFFI
Key a=3, b=3: SPWWZ
Key a=3, b=4: JGNNQ
Key a=3, b=5: AXEEH
Key a=3, b=6: ROVVY
Key a=3, b=7: IFMMP
Key a=3, b=8: ZWDDG
Key a=3, b=9: QNUUX
Key a=3, b=10: HELLO # the only correct output
Key a=3, b=11: YVCCF
Key a=3, b=12: PMTTW
Key a=3, b=13: GDKKN
Key a=3, b=14: XUBBE
Key a=3, b=15: OLSSV
Key a=3, b=16: FCJJM
Key a=3, b=17: WTAAD
Key a=3, b=18: NKRRU
Key a=3, b=19: EBIIL
Key a=3, b=20: VSZZC
Key a=3, b=21: MJQQT
Key a=3, b=22: DAHHK
Key a=3, b=23: URYYB
Key a=3, b=24: LIPPS
Key a=3, b=25: CZGGJ
Key a=5, b=0: BUTTA
Key a=5, b=1: GZYYF
Key a=5, b=2: LEDDK
Key a=5, b=3: QJIIP
Key a=5, b=4: VONNU
Key a=5, b=5: ATSSZ
Key a=5, b=6: FYXXE
Key a=5, b=7: KDCCJ
Key a=5, b=8: PIHHO
Key a=5, b=9: UNMMT
Key a=5, b=10: ZSRRY
Key a=5, b=11: EXWWD
Key a=5, b=12: JCBBI
Key a=5, b=13: OHGGN
Key a=5, b=14: TMLLS
Key a=5, b=15: YRQQX
Key a=5, b=16: DWVVC
Key a=5, b=17: IBAAH
Key a=5, b=18: NGFFM
Key a=5, b=19: SLKKR
Key a=5, b=20: XQPPW
Key a=5, b=21: CVUUB
Key a=5, b=22: HAZZG
Key a=5, b=23: MFEEL
Key a=5, b=24: RKJJQ
Key a=5, b=25: WPOOV
Key a=7, b=0: XSVVA
Key a=7, b=1: IDGGL
Key a=7, b=2: TORRW
Key a=7, b=3: EZCCH
Key a=7, b=4: PKNNS
Key a=7, b=5: AVYYD
Key a=7, b=6: LGJJO
Key a=7, b=7: WRUUZ
Key a=7, b=8: HCFFK
Key a=7, b=9: SNQQV
Key a=7, b=10: DYBBG
Key a=7, b=11: OJMMR
Key a=7, b=12: ZUXXC
Key a=7, b=13: KFIIN
Key a=7, b=14: VQTTY
Key a=7, b=15: GBEEJ
Key a=7, b=16: RMPPU
Key a=7, b=17: CXAAF
Key a=7, b=18: NILLQ
Key a=7, b=19: YTWWB
Key a=7, b=20: JEHHM
Key a=7, b=21: UPSSX
Key a=7, b=22: FADDI
Key a=7, b=23: QLOOT
Key a=7, b=24: BWZZE
Key a=7, b=25: MHKKP
Key a=9, b=0: POZZA
Key a=9, b=1: MLWWX
Key a=9, b=2: JITTU
Key a=9, b=3: GFQQR
Key a=9, b=4: DCNNO
Key a=9, b=5: AZKKL
Key a=9, b=6: XWHHI
Key a=9, b=7: UTEEF
Key a=9, b=8: RQBBC
Key a=9, b=9: ONYYZ
Key a=9, b=10: LKVVW
Key a=9, b=11: IHSST
Key a=9, b=12: FEPPQ
Key a=9, b=13: CBMMN
Key a=9, b=14: ZYJJK
Key a=9, b=15: WVGGH
Key a=9, b=16: TSDDE
Key a=9, b=17: QPAAB
Key a=9, b=18: NMXXY
Key a=9, b=19: KJUUV
Key a=9, b=20: HGRRS
Key a=9, b=21: EDOOP
Key a=9, b=22: BALLM
Key a=9, b=23: YXIIJ
Key a=9, b=24: VUFFG
Key a=9, b=25: SRCCD
Key a=11, b=0: RCLLA
Key a=11, b=1: YJSSH
Key a=11, b=2: FQZZO
Key a=11, b=3: MXGGV
Key a=11, b=4: TENNC
Key a=11, b=5: ALUUJ
Key a=11, b=6: HSBBQ
Key a=11, b=7: OZIIX
Key a=11, b=8: VGPPE
Key a=11, b=9: CNWWL
Key a=11, b=10: JUDDS
Key a=11, b=11: QBKKZ
Key a=11, b=12: XIRRG
Key a=11, b=13: EPYYN
Key a=11, b=14: LWFFU
Key a=11, b=15: SDMMB
Key a=11, b=16: ZKTTI
Key a=11, b=17: GRAAP
Key a=11, b=18: NYHHW
Key a=11, b=19: UFOOD
Key a=11, b=20: BMVVK
Key a=11, b=21: ITCCR
Key a=11, b=22: PAJJY
Key a=11, b=23: WHQQF
Key a=11, b=24: DOXXM
Key a=11, b=25: KVEET
Key a=15, b=0: JYPPA
Key a=15, b=1: CRIIT
Key a=15, b=2: VKBBM
Key a=15, b=3: ODUUF
Key a=15, b=4: HWNNY
Key a=15, b=5: APGGR
Key a=15, b=6: TIZZK
Key a=15, b=7: MBSSD
Key a=15, b=8: FULLW
Key a=15, b=9: YNEEP
Key a=15, b=10: RGXXI
Key a=15, b=11: KZQQB
Key a=15, b=12: DSJJU
Key a=15, b=13: WLCCN
Key a=15, b=14: PEVVG
Key a=15, b=15: IXOOZ
Key a=15, b=16: BQHHS
Key a=15, b=17: UJAAL
Key a=15, b=18: NCTTE
Key a=15, b=19: GVMMX
Key a=15, b=20: ZOFFQ
Key a=15, b=21: SHYYJ
Key a=15, b=22: LARRC
Key a=15, b=23: ETKKV
Key a=15, b=24: XMDDO
Key a=15, b=25: QFWWH
Key a=17, b=0: LMBBA
Key a=17, b=1: OPEED
Key a=17, b=2: RSHHG
Key a=17, b=3: UVKKJ
Key a=17, b=4: XYNNM
Key a=17, b=5: ABQQP
Key a=17, b=6: DETTS
Key a=17, b=7: GHWWV
Key a=17, b=8: JKZZY
Key a=17, b=9: MNCCB
Key a=17, b=10: PQFFE
Key a=17, b=11: STIIH
Key a=17, b=12: VWLLK
Key a=17, b=13: YZOON
Key a=17, b=14: BCRRQ
Key a=17, b=15: EFUUT
Key a=17, b=16: HIXXW
Key a=17, b=17: KLAAZ
Key a=17, b=18: NODDC
Key a=17, b=19: QRGGF
Key a=17, b=20: TUJJI
Key a=17, b=21: WXMML
Key a=17, b=22: ZAPPO
Key a=17, b=23: CDSSR
Key a=17, b=24: FGVVU
Key a=17, b=25: IJYYX
Key a=19, b=0: DIFFA
Key a=19, b=1: SXUUP
Key a=19, b=2: HMJJE
Key a=19, b=3: WBYYT
Key a=19, b=4: LQNNI
Key a=19, b=5: AFCCX
Key a=19, b=6: PURRM
Key a=19, b=7: EJGGB
Key a=19, b=8: TYVVQ
Key a=19, b=9: INKKF
Key a=19, b=10: XCZZU
Key a=19, b=11: MROOJ
Key a=19, b=12: BGDDY
Key a=19, b=13: QVSSN
Key a=19, b=14: FKHHC
Key a=19, b=15: UZWWR
Key a=19, b=16: JOLLG
Key a=19, b=17: YDAAV
Key a=19, b=18: NSPPK
Key a=19, b=19: CHEEZ
Key a=19, b=20: RWTTO
Key a=19, b=21: GLIID
Key a=19, b=22: VAXXS
Key a=19, b=23: KPMMH
Key a=19, b=24: ZEBBW
Key a=19, b=25: OTQQL
Key a=21, b=0: ZGHHA
Key a=21, b=1: UBCCV
Key a=21, b=2: PWXXQ
Key a=21, b=3: KRSSL
Key a=21, b=4: FMNNG
Key a=21, b=5: AHIIB
Key a=21, b=6: VCDDW
Key a=21, b=7: QXYYR
Key a=21, b=8: LSTTM
Key a=21, b=9: GNOOH
Key a=21, b=10: BIJJC
Key a=21, b=11: WDEEX
Key a=21, b=12: RYZZS
Key a=21, b=13: MTUUN
Key a=21, b=14: HOPPI
Key a=21, b=15: CJKKD
Key a=21, b=16: XEFFY
Key a=21, b=17: SZAAT
Key a=21, b=18: NUVVO
Key a=21, b=19: IPQQJ
Key a=21, b=20: DKLLE
Key a=21, b=21: YFGGZ
Key a=21, b=22: TABBU
Key a=21, b=23: OVWWP
Key a=21, b=24: JQRRK
Key a=21, b=25: ELMMF
Key a=23, b=0: HKDDA
Key a=23, b=1: QTMMJ
Key a=23, b=2: ZCVVS
Key a=23, b=3: ILEEB
Key a=23, b=4: RUNNK
Key a=23, b=5: ADWWT
Key a=23, b=6: JMFFC
Key a=23, b=7: SVOOL
Key a=23, b=8: BEXXU
Key a=23, b=9: KNGGD
Key a=23, b=10: TWPPM
Key a=23, b=11: CFYYV
Key a=23, b=12: LOHHE
Key a=23, b=13: UXQQN
Key a=23, b=14: DGZZW
Key a=23, b=15: MPIIF
Key a=23, b=16: VYRRO
Key a=23, b=17: EHAAX
Key a=23, b=18: NQJJG
Key a=23, b=19: WZSSP
Key a=23, b=20: FIBBY
Key a=23, b=21: ORKKH
Key a=23, b=22: XATTQ
Key a=23, b=23: GJCCZ
Key a=23, b=24: PSLLI
Key a=23, b=25: YBUUR
Key a=25, b=0: VEJJA
Key a=25, b=1: WFKKB
Key a=25, b=2: XGLLC
Key a=25, b=3: YHMMD
Key a=25, b=4: ZINNE
Key a=25, b=5: AJOOF
Key a=25, b=6: BKPPG
Key a=25, b=7: CLQQH
Key a=25, b=8: DMRRI
Key a=25, b=9: ENSSJ
Key a=25, b=10: FOTTK
Key a=25, b=11: GPUUL
Key a=25, b=12: HQVVM
Key a=25, b=13: IRWWN
Key a=25, b=14: JSXXO
Key a=25, b=15: KTYYP
Key a=25, b=16: LUZZQ
Key a=25, b=17: MVAAR
Key a=25, b=18: NWBBS
Key a=25, b=19: OXCCT
Key a=25, b=20: PYDDU
Key a=25, b=21: QZEEV
Key a=25, b=22: RAFFW
Key a=25, b=23: SBGGX
Key a=25, b=24: TCHHY
Key a=25, b=25: UDIIZ
```

## Cipher correctness

The core definition of cipher correctness is that it's a mathematical property stating that for any valid key (k) and message (m), running decryption on the ciphertext with that same key yields the original message. It also guarantees that the encryption transformation is fully invertible when using the proper matching key.

However, cipher correctness does not mean cipher security. Correctness ensures functionality and reliability (e.g., the message can be read later). Security ensures that unauthorized people cannot read the message even if they intercept it. An algorithm can be completely correct (it encrypts and decrypts fine) but insecure (easy for hackers to break, like the Caesar or Affine Cipher).

That said, this project contains limitations:

1. `run_decrypt()` in `decrypt.py` only runs `affine_brute_force`.
1. There is no coprime validation.
1. There is no real known-key decrypt path via CLI, deciding on lowercase/non-alphabetic handling, real key args instead of hardcoded.
1. I can't pick my own key without editing source code.

## Testing

| Tool | Purpose | Configured in |
| --- | --- | --- |
|pytest | test runner/framework | pyproject.toml/<div>[tool.pytest.ini_options]</div> |
| pytest-cov | the coverage plugin measuring branch and statement coverage | pyproject.toml/<div>[tool.coverage.run]</div><div>[tool.coverage.report]</div> |

**Testing commands:**

```shell
# pytest:
pytest --cov=affine_cipher --cov-report=term-missing
# pytest-cov:
pytest --cov=affine_cipher --cov-report=term-missing --cov-report=html
```

## Code quality machinery

### Linting + formatting

| Tool | Purpose | Configured in |
| --- | --- | --- |
| ruff | lint + format | pyproject.toml/<div>[tool.ruff]</div><div>target-version = "py314"</div><div>line-length = 88</div><div>[tool.ruff.lint]</div><div>select = ["E", "F", "I", "UP", "B"]</div> |
| mypy | checks/verifies standard type hints in Python code | pyproject.toml/<div>[tool.mypy]</div><div>python_version = "3.14"</div><div>disallow_untyped_defs = true</div> |

### Security

| Tool | Purpose | Configured in |
| --- | --- | --- |
| bandit | security-focused static analysis tool | .pre-commit-config.yaml/<div>- id: bandit</div><div>&nbsp;&nbsp;args: ["-r", "src"]</div><div>&nbsp;&nbsp;pass_filenames: false</div> |
| pip-audit | scans Python environments and dependency trees for packages with known security vulnerabilities | .pre-commit-config.yaml/<div>- id: pip-audit</div><div>&nbsp;&nbsp;name: pip-audit</div><div>&nbsp;&nbsp;entry: uv run pip-audit</div><div>&nbsp;&nbsp;language: system</div><div>&nbsp;&nbsp;pass_filenames: false</div><div>&nbsp;&nbsp;files: ^(pyproject\.toml\|uv\.lock)$</div>

### Pre-commit hooks

| Hook | Purpose | Configured in |
| --- | --- | --- |
| ruff-check | primary command used to run the Ruff Linter on Python projects | .pre-commit-config.yaml/<div>- id: ruff-check</div><div>&nbsp;&nbsp;args: [--fix]</div> |
| ruff-format | automatically formats Python code | .pre-commit-config.yaml/<div>- id: ruff-format</div> |
| mypy | checks/verifies standard type hints in Python code | .pre-commit-config.yaml/<div>- id: mypy</div><div>&nbsp;&nbsp;additional_dependencies: [types-colorama]</div> |
| pytest | runs Python tests against the Python code | .pre-commit-config.yaml/<div>- id: pytest</div><div>&nbsp;&nbsp;name: pytest</div><div>&nbsp;&nbsp;entry: uv run pytest</div><div>&nbsp;&nbsp;language: system</div><div>&nbsp;&nbsp;pass_filenames: false</div><div>&nbsp;&nbsp;always_run: true</div> |
| bandit | security-focused static analysis tool | .pre-commit-config.yaml/<div>- id: bandit</div><div>&nbsp;&nbsp;args: ["-r", "src"]</div><div>&nbsp;&nbsp;pass_filenames: false</div> |
| pip-audit | scans Python environments and dependency trees for packages with known security vulnerabilities | .pre-commit-config.yaml/<div>- id: pip-audit</div><div>&nbsp;&nbsp;name: pip-audit</div><div>&nbsp;&nbsp;entry: uv run pip-audit</div><div>&nbsp;&nbsp;language: system</div><div>&nbsp;&nbsp;pass_filenames: false</div><div>&nbsp;&nbsp;files: ^(pyproject\.toml\|uv\.lock)$</div> |

### CI/CD

GitHub Actions runs on every push and pull request to `main `(`.github/workflows/ci.yml`), via two jobs:

- `lint-and-test`: runs the checks from the tables above against every commit. `ruff check` and `ruff format --check` (lint & format), `mypy .` (type checking), `pytest` with coverage reporting (`--cov=affine_cipher --cov-report=term-missing --cov-report=xml`), `bandit -r src` (security static analysis), and `pip-audit` (dependency vulnerability scanning). Environment setup uses `astral-sh/setup-uv` + `uv sync --all-extras --dev --frozen` for a reproducible install.
- `build `: runs `uv build` to produce a wheel, as a preview of the (currently deferred) Publish to PyPI work.

`permissions: contents: read` scopes the workflow's token down to read-only, and a `concurrency` group cancels stale runs when new commits land on the same branch.

## Footnotes

[^1]: Being a `coprime` of an integer means having no positive integer factors in common, aside from 1.



