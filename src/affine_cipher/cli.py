import argparse

from affine_cipher.decrypt import run_decrypt
from affine_cipher.encrypt import run_encrypt


def main() -> None:

    parser = argparse.ArgumentParser(prog="affine-cipher")
    subparsers = parser.add_subparsers(dest="command", required=True)
    encrypt_parser = subparsers.add_parser("encrypt")
    decrypt_parser = subparsers.add_parser("decrypt")

    for p in [encrypt_parser]:
        p.add_argument("-a", type=int, required=True)
        p.add_argument("-b", type=int, required=True)

    for p in [decrypt_parser]:
        p.add_argument("-a", type=int, required=False)
        p.add_argument("-b", type=int, required=False)
        p.add_argument("--brute-force", action="store_true")

    args = parser.parse_args()

    try:
        if args.command == "encrypt":
            run_encrypt(args.a, args.b)
        elif args.command == "decrypt":
            if (args.a is None) != (args.b is None):
                parser.error("-a and -b must be given together")
            if (args.a is not None) and (args.b is not None) and (args.brute_force):
                parser.error(
                    "-a and -b and --brute-force cannot all be selected together. Choose either -a and -b or --brute-force."  # noqa: E501
                )
            run_decrypt(args.a, args.b, args.brute_force)
    except ValueError as e:
        parser.error(str(e))
