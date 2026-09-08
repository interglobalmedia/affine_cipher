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
