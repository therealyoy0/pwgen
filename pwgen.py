#!/usr/bin/env python3
"""Generate a cryptographically random password (stdlib only)."""
from __future__ import annotations

import argparse
import secrets
import string
import sys

LETTERS = string.ascii_letters
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?"
DEFAULT_LENGTH = 16
MIN_LENGTH = 1
MAX_LENGTH = 1024


def build_alphabet(*, digits: bool, symbols: bool) -> str:
    alphabet = LETTERS
    if digits:
        alphabet += DIGITS
    if symbols:
        alphabet += SYMBOLS
    return alphabet


def generate_password(length: int, alphabet: str) -> str:
    if not alphabet:
        raise ValueError("alphabet must not be empty")
    return "".join(secrets.choice(alphabet) for _ in range(length))


def _length_type(value: str) -> int:
    try:
        length = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid int value: {value!r}") from exc
    if not MIN_LENGTH <= length <= MAX_LENGTH:
        raise argparse.ArgumentTypeError(
            f"length must be between {MIN_LENGTH} and {MAX_LENGTH}"
        )
    return length


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a random password.")
    parser.add_argument(
        "-l",
        "--length",
        type=_length_type,
        default=DEFAULT_LENGTH,
        help=f"Password length (default: {DEFAULT_LENGTH}, min: {MIN_LENGTH}, max: {MAX_LENGTH})",
    )
    parser.add_argument(
        "--no-digits",
        action="store_true",
        help="Exclude digits 0-9 (digits included by default)",
    )
    parser.add_argument(
        "--symbols",
        action="store_true",
        help="Include symbols (off by default)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    alphabet = build_alphabet(digits=not args.no_digits, symbols=args.symbols)
    try:
        password = generate_password(args.length, alphabet)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2
    print(password)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
