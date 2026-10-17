#!/usr/bin/env python3
"""Generate cryptographically random passwords (stdlib only)."""
from __future__ import annotations

import argparse
import secrets
import string
import sys

LETTERS = string.ascii_letters
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?"
AMBIGUOUS = "0Ol1I"
DEFAULT_LENGTH, DEFAULT_COUNT = 16, 1
MIN_LENGTH, MAX_LENGTH = 1, 1024
MIN_COUNT, MAX_COUNT = 1, 1000


def build_alphabet(*, digits: bool, symbols: bool, exclude_ambiguous: bool = False) -> str:
    alphabet = LETTERS
    if digits:
        alphabet += DIGITS
    if symbols:
        alphabet += SYMBOLS
    if exclude_ambiguous:
        alphabet = "".join(ch for ch in alphabet if ch not in AMBIGUOUS)
    return alphabet


def generate_password(length: int, alphabet: str) -> str:
    if not alphabet:
        raise ValueError("alphabet must not be empty")
    if not MIN_LENGTH <= length <= MAX_LENGTH:
        raise ValueError(f"length must be between {MIN_LENGTH} and {MAX_LENGTH}")
    return "".join(secrets.choice(alphabet) for _ in range(length))


def _bounded_int(name: str, lo: int, hi: int):
    def convert(value: str) -> int:
        try:
            n = int(value)
        except ValueError as exc:
            raise argparse.ArgumentTypeError(f"invalid int value: {value!r}") from exc
        if not lo <= n <= hi:
            raise argparse.ArgumentTypeError(f"{name} must be between {lo} and {hi}")
        return n

    return convert


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate random password(s).")
    p.add_argument(
        "-l", "--length", type=_bounded_int("length", MIN_LENGTH, MAX_LENGTH),
        default=DEFAULT_LENGTH, help=f"length (default {DEFAULT_LENGTH})",
    )
    p.add_argument(
        "-n", "--count", type=_bounded_int("count", MIN_COUNT, MAX_COUNT),
        default=DEFAULT_COUNT, help=f"how many (default {DEFAULT_COUNT})",
    )
    p.add_argument("--no-digits", action="store_true", help="exclude digits")
    p.add_argument("--symbols", action="store_true", help="include symbols")
    p.add_argument(
        "--exclude-ambiguous",
        action="store_true",
        help="exclude ambiguous characters 0, O, l, 1, I",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    alphabet = build_alphabet(
        digits=not args.no_digits,
        symbols=args.symbols,
        exclude_ambiguous=args.exclude_ambiguous,
    )
    try:
        for _ in range(args.count):
            print(generate_password(args.length, alphabet))
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
