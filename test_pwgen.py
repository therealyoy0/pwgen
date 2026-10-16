#!/usr/bin/env python3
"""Unit tests for pwgen."""
from __future__ import annotations

import contextlib
import io
import string
import unittest
from unittest import mock

import pwgen


class TestAlphabet(unittest.TestCase):
    def test_alphabet_default_letters_and_digits(self) -> None:
        alphabet = pwgen.build_alphabet(digits=True, symbols=False)
        for ch in string.ascii_letters + string.digits:
            self.assertIn(ch, alphabet)
        for ch in pwgen.SYMBOLS:
            self.assertNotIn(ch, alphabet)

    def test_alphabet_no_digits(self) -> None:
        alphabet = pwgen.build_alphabet(digits=False, symbols=False)
        for ch in string.digits:
            self.assertNotIn(ch, alphabet)
        for ch in string.ascii_letters:
            self.assertIn(ch, alphabet)

    def test_alphabet_with_symbols(self) -> None:
        alphabet = pwgen.build_alphabet(digits=True, symbols=True)
        for ch in pwgen.SYMBOLS:
            self.assertIn(ch, alphabet)
        for ch in string.ascii_letters:
            self.assertIn(ch, alphabet)

    def test_alphabet_no_digits_with_symbols(self) -> None:
        alphabet = pwgen.build_alphabet(digits=False, symbols=True)
        for ch in string.digits:
            self.assertNotIn(ch, alphabet)
        for ch in string.ascii_letters + pwgen.SYMBOLS:
            self.assertIn(ch, alphabet)


class TestGeneration(unittest.TestCase):
    def test_generate_length(self) -> None:
        alphabet = pwgen.build_alphabet(digits=True, symbols=False)
        for length in (1, 8, 16, 64, 1024):
            self.assertEqual(len(pwgen.generate_password(length, alphabet)), length)

    def test_generate_charset(self) -> None:
        alphabet = pwgen.build_alphabet(digits=True, symbols=True)
        password = pwgen.generate_password(64, alphabet)
        for ch in password:
            self.assertIn(ch, alphabet)

    def test_generate_empty_alphabet_raises(self) -> None:
        with self.assertRaises(ValueError):
            pwgen.generate_password(8, "")

    def test_generate_uses_secrets(self) -> None:
        with mock.patch("secrets.choice", return_value="x") as choice:
            password = pwgen.generate_password(5, "abc")
        self.assertEqual(password, "xxxxx")
        self.assertEqual(choice.call_count, 5)


class TestCLI(unittest.TestCase):
    def test_parse_defaults(self) -> None:
        args = pwgen.parse_args([])
        self.assertEqual(args.length, 16)
        self.assertFalse(args.no_digits)
        self.assertFalse(args.symbols)

    def test_parse_length_and_flags(self) -> None:
        args = pwgen.parse_args(["-l", "24", "--symbols", "--no-digits"])
        self.assertEqual(args.length, 24)
        self.assertTrue(args.no_digits)
        self.assertTrue(args.symbols)

    def test_parse_length_too_small(self) -> None:
        with self.assertRaises(SystemExit) as ctx:
            pwgen.parse_args(["-l", "0"])
        self.assertEqual(ctx.exception.code, 2)

    def test_parse_length_too_large(self) -> None:
        with self.assertRaises(SystemExit) as ctx:
            pwgen.parse_args(["-l", "1025"])
        self.assertEqual(ctx.exception.code, 2)

    def test_parse_length_non_int(self) -> None:
        with self.assertRaises(SystemExit) as ctx:
            pwgen.parse_args(["-l", "abc"])
        self.assertEqual(ctx.exception.code, 2)

    def test_main_prints_password(self) -> None:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = pwgen.main([])
        self.assertEqual(code, 0)
        lines = buf.getvalue().splitlines()
        self.assertEqual(len(lines), 1)
        password = lines[0]
        self.assertEqual(len(password), 16)
        alphabet = pwgen.build_alphabet(digits=True, symbols=False)
        for ch in password:
            self.assertIn(ch, alphabet)

    def test_main_respects_length(self) -> None:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = pwgen.main(["-l", "8"])
        self.assertEqual(code, 0)
        self.assertEqual(len(buf.getvalue().strip()), 8)


if __name__ == "__main__":
    unittest.main()
