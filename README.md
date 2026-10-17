# pwgen

Generate cryptographically random password(s) to stdout (Python stdlib only).

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
python pwgen.py --exclude-ambiguous
python pwgen.py -l 24 --exclude-ambiguous --symbols
python pwgen.py -n 5 -l 20 --exclude-ambiguous --symbols
```

| Option | Default | Description |
|---|---|---|
| `-l` / `--length` | `16` | Password length (`1`–`1024`) |
| `-n` / `--count` | `1` | How many passwords to print (`1`–`1000`, one per line) |
| `--no-digits` | off | Exclude digits `0-9` from the alphabet |
| `--symbols` | off | Include symbols `!@#$%^&*()-_=+[]{}|;:,.<>?` |
| `--exclude-ambiguous` | off | Exclude ambiguous characters `0`, `O`, `l`, `1`, `I` |
| Letters (a–z, A–Z) | always on | Cannot be disabled |

Digits are included by default; use `--no-digits` to turn them off.

With `--symbols`, quote the password if you paste it into a shell.

## Security

- Uses the `secrets` module (OS CSPRNG), never `random`.
- `--exclude-ambiguous` removes look-alike characters (`0`/`O`, `l`/`1`/`I`) to reduce transcription errors; it also shrinks the alphabet slightly.
- Local secrets: `.env` is gitignored. Copy `.env.example` if you need env vars for local tooling — **pwgen itself does not load `.env`**. Never commit real credentials.

## Tests

```bash
python -m unittest -v
```
