# README_FOR_AI

This file is the installation and bootstrap guide for an AI assistant or coding agent setting up this project on a new machine.

Follow the steps in order.

## Goal

Recreate a working FredOS + OpenClaw development environment on a new machine without copying over:

- secrets
- OAuth state
- local databases
- runtime logs
- personal machine state

## High-Level Structure

This package contains:

- `fredos/` — sanitized FredOS backend source
- `openclaw-overlay/` — local modifications that should be applied on top of upstream OpenClaw
- `openclaw-state-template/` — sanitized OpenClaw workspace/config templates
- `docs/` — architecture and validation docs

## Step 1: Prerequisites

Install these first:

- Git
- Node.js and `pnpm`
- Python 3.11+
- Git Bash on Windows if OpenClaw build scripts require `bash`
- Ollama if local model serving is desired

## Step 2: Set Up FredOS

Working directory target:

- create a local workspace folder
- copy this repo package into it

Inside `fredos/`:

1. create a virtual environment
2. install dependencies from `requirements.txt`
3. create `.env` from `.env.example`
4. fill in the required API/model settings manually
5. run Alembic migrations
6. start FredOS locally

Suggested commands on Windows PowerShell:

```powershell
cd fredos
python -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
$env:PYTHONPATH = (Get-Location).Path
alembic upgrade head
.\fredos.bat run
```

Important:

- do not copy any old `.env`
- do not copy any old `fredos.db`
- let the database start clean

## Step 3: Clone OpenClaw Upstream

Clone upstream OpenClaw separately on the new machine.

Use the upstream repository and check out the intended compatible commit or release for this package.

This package was prepared against a local OpenClaw based on:

- upstream branch: `main`
- local head used during packaging: `883239a560ecc7e83860439a4adacba5c7b0ec78`

## Step 4: Apply the OpenClaw Overlay

Copy the contents of `openclaw-overlay/` over the matching paths in the OpenClaw clone.

Included overlay areas currently contain:

- `extensions/fredos/`
- selected `src/agents/` files
- selected `src/config/` files
- selected build/runtime support files

If a file already exists in upstream OpenClaw, replace it with the overlay version only after confirming that this package targets the same or a compatible OpenClaw revision.

## Step 5: Install and Build OpenClaw

From the OpenClaw clone:

```powershell
pnpm install
pnpm build
```

If `bash` is not found on Windows, make sure Git Bash is installed and on `PATH`.

## Step 6: Create Fresh OpenClaw State

Do **not** copy a live `.openclaw` directory from another machine.

Instead:

1. create a fresh local state directory
2. copy the contents of `openclaw-state-template/` into that new state directory
3. create a sanitized `openclaw.json` from the template in this package
4. manually fill in machine-specific values

Recommended local state directory:

```text
<repo-root>\\.openclaw
```

## Step 7: Fill in OpenClaw Secrets Manually

The packaged config template intentionally omits live values for:

- OAuth profiles
- provider auth
- Discord token
- gateway token
- any machine-specific paths

These must be added manually on the target machine.

## Step 8: Start OpenClaw

Set the state dir:

```powershell
$env:OPENCLAW_STATE_DIR = "C:\\path\\to\\your\\repo\\.openclaw"
```

Then run from the OpenClaw clone:

```powershell
pnpm openclaw gateway run --allow-unconfigured
```

Useful checks:

```powershell
pnpm openclaw agents list
pnpm openclaw status --json
```

## Step 9: Verify FredOS Integration

Confirm:

- FredOS is running on the expected local port
- OpenClaw loads the `fredos` plugin
- `coder-pm` can see `fredos_retrieve_context`
- `memory-agent` can see `fredos_list_projects`

## Step 10: Validate the Stack

Run a small bounded validation before using the setup for real project work:

1. generic orchestration validation
2. project-scoped validation
3. one bounded coding-project execution test

## Packaging Rules

When updating this package in the future:

- keep `fredos/` sanitized
- keep `openclaw-overlay/` minimal
- keep `openclaw-state-template/` template-only
- never commit live auth or local DB state

## Source of Truth

For architecture details, read:

- `docs/FREDOS_OPENCLAW_ARCHITECTURE_AND_VALIDATION_20260330.md`

