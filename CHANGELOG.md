# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/)-style grouping where useful.

## [Unreleased]

### Changed

- docs: refresh README with full CLI options table and security notes

## [0.1.0] - 2026-10-17

### Added

- CLI: generate cryptographically random passwords via `secrets` (stdlib only)
  - `-l` / `--length` (default `16`, range `1`–`1024`)
  - `--no-digits`, `--symbols`
  - letters always included
- `-n` / `--count` to print N passwords (default `1`, range `1`–`1000`, one per line)
- `--exclude-ambiguous` to drop look-alike characters `0`, `O`, `l`, `1`, `I` from the alphabet
- `.gitignore` for Python caches, venvs, IDE/OS junk, and PocketTeam artifacts
- `.env` ignored; `.env.example` provided for local tooling (pwgen does not load it)
- Unit tests for alphabet, CLI, count, and exclude-ambiguous
- README usage and options documentation

### Fixed

- `generate_password`: reject out-of-range `length` (must be between `1` and `1024`)
