# FredOS + OpenClaw Repo Package

This folder is a GitHub-ready package for the current FredOS + OpenClaw architecture.

It is intentionally **not** a full dump of the local machine state.

Instead, it contains:

- the FredOS backend source
- an OpenClaw overlay for the files changed locally
- sanitized OpenClaw state templates
- architecture and validation docs
- install guidance for humans and AI assistants

## Who This Is For

This package is for people who want to reproduce the current FredOS + OpenClaw architecture on another machine without inheriting private runtime state from the original development environment.

It is especially useful for:

- local-first agent system builders
- contributors who want to inspect or extend the architecture
- AI coding agents that need a clean installation path

## Why This Repo Is Packaged This Way

The local working environment contains machine-specific and secret-bearing state that should not be pushed to GitHub, including:

- OAuth/auth profiles
- API keys and gateway tokens
- Discord tokens
- local databases with real task/project data
- runtime logs
- local `.openclaw` state
- large bundled dependencies and build outputs

So the GitHub package is split into:

### 1. `fredos/`

The FredOS backend source tree, sanitized for sharing.

Included:

- app code
- Alembic migrations
- docs
- tests
- `.env.example`

Excluded:

- `.env`
- `fredos.db`
- local logs
- `fredos_data/`
- downloaded Python tarballs and other local blobs

### 2. `openclaw-overlay/`

This is **not** a full OpenClaw fork.

It contains only the local files that were added or changed relative to upstream OpenClaw and are required for this architecture:

- FredOS plugin files
- agent/runtime compatibility changes
- tool/profile changes
- subagent-related adjustments

Recommended installation model:

1. clone upstream OpenClaw separately
2. copy this overlay on top of the checked-out upstream tree
3. install/build OpenClaw locally

This keeps the repo easier to maintain than publishing a full long-lived OpenClaw fork with machine-local state mixed in.

### 3. `openclaw-state-template/`

Sanitized workspace/bootstrap templates for:

- `coder-pm`
- `coding-agent`
- `memory-agent`
- shared local `TOOLS.md`

These are templates, not a live state dump.

### 4. `docs/`

Architecture, validation, and policy documents.

## What Is Already Validated

This architecture has already been validated in two important ways:

### A. Real coding-project execution

Validated capabilities include:

- FredOS context retrieval
- FredOS task update
- project grounding against real repo files
- bounded ML smoke training run
- project-local walkthrough updates

### B. Phase 1 subagent orchestration

Validated capabilities include:

- router-led bounded orchestration
- dual dispatch with `coding-agent` and `memory-agent`
- project assignment policy in practice
- router-layer FredOS writeback

## Repo Layout

- `fredos/`
- `openclaw-overlay/`
- `openclaw-state-template/`
- `docs/`
- `README_FOR_AI.md`

## What Should Not Be Committed

Do not commit:

- real `.env` files
- local `.openclaw` state
- `fredos.db`
- `fredos_data/`
- OAuth profile files
- auth tokens
- gateway tokens
- Discord tokens
- runtime logs
- `node_modules/`
- `dist/` and `dist-runtime/`

## Installation Model

This package assumes:

1. FredOS is run from the included `fredos/` folder
2. OpenClaw is installed from upstream plus the local overlay
3. OpenClaw local state is created fresh from the provided templates
4. secrets are added manually on the new machine

For step-by-step machine bootstrap, use:

- `README_FOR_AI.md`

## Key Design Principle

OpenClaw is the runtime shell.  
FredOS is the canonical memory and task layer.  
Real project repos remain execution truth.

## Before Publishing

Use these companion documents:

- [`REPO_PUBLISH_GUIDE_20260330.md`](C:/Users/Fred/Desktop/F_OS/FOSforGithubRepo/REPO_PUBLISH_GUIDE_20260330.md)
- [`PUBLISH_CHECKLIST_20260330.md`](C:/Users/Fred/Desktop/F_OS/FOSforGithubRepo/PUBLISH_CHECKLIST_20260330.md)
