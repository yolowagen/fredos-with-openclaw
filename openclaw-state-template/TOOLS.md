# OpenClaw State Template Notes

This folder contains sanitized template state for a fresh OpenClaw setup.

## Purpose

Use these files to bootstrap a new local `.openclaw` directory without copying:

- secrets
- old sessions
- old auth state
- machine-specific paths

## Canonical State Rule

Create a fresh local state directory on the target machine and copy this template into it.

Then:

1. rename `openclaw.template.json` to `openclaw.json`
2. replace `__STATE_DIR__` with the real local state path
3. fill in auth/provider tokens manually

## Do Not Carry Over

Do not copy over:

- old OAuth profile files
- old gateway tokens
- old Discord tokens
- old device pairing state
- old logs

