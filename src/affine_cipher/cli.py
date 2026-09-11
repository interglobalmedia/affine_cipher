import argparse

from affine_cipher.decrypt import run_decrypt
from affine_cipher.encrypt import run_encrypt


def main() -> None:

    parser = argparse.ArgumentParser(prog="affine-cipher")
    subparsers = parser.add_subparsers(dest="command", required=True)
    encrypt_parser = subparsers.add_parser("encrypt")
    subparsers.add_parser("decrypt")

    for p in [encrypt_parser]:
        p.add_argument("-a", type=int, required=True)
        p.add_argument("-b", type=int, required=True)

    args = parser.parse_args()

    if args.command == "encrypt":
        run_encrypt(args.a, args.b)
    elif args.command == "decrypt":
        run_decrypt()
