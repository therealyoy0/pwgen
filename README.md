# pwgen

Generate one cryptographically random password to stdout (Python stdlib only).

## Requirements

Python 3.10+ (stdlib only — no third-party packages). Full local: run `python pwgen.py`; no install/package.

## Usage

```bash
python pwgen.py
python pwgen.py -l 32
python pwgen.py -n 3
python pwgen.py -l 24 --symbols
python pwgen.py -l 20 --no-digits
python pwgen.py -l 20 --no-digits --symbols
```

| Option | Default | Effect |
|---|---|---|
| `-l` / `--length` | `16` | Exact length (`1`–`1024`) |
| `-n` / `--count` | `1` | How many passwords (`1`–`1000`, one per line) |
| Letters (a–z, A–Z) | always on | Cannot be disabled |
| Digits `0-9` | on | Disable with `--no-digits` |
| Symbols | off | Enable with `--symbols` |

Symbol set: `!@#$%^&*()-_=+[]{}|;:,.<>?`  
With `--symbols`, quote the password if you paste it into a shell.

## Security

Uses the `secrets` module (OS CSPRNG), never `random`.

## Tests

```bash
python -m unittest -v
```
