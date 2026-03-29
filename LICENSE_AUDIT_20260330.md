# License Audit

Date: 2026-03-30
Scope: packaging review for `FOSforGithubRepo`
Note: this is an engineering risk check, not formal legal advice.

## Summary

Based on the currently packaged source and the direct dependencies inspected from the local environment:

- the overall license picture looks **manageable**
- the dominant licenses are **MIT**, **Apache-2.0**, **BSD**, and **ISC**
- I did **not** find an obvious hard blocker for publishing the packaged repo
- the one dependency that deserves explicit attention is `jszip`, because it is published as:
  - `MIT OR GPL-3.0-or-later`

That is not automatically a problem, because an `OR` expression means one valid path is available under MIT terms.

## Main Components

### OpenClaw

Source:

- [package.json](C:/Users/Fred/Desktop/F_OS/openclaw/package.json)
- [LICENSE](C:/Users/Fred/Desktop/F_OS/openclaw/LICENSE)

Observed license:

- `MIT`

Practical meaning:

- your local overlay on top of OpenClaw is not obviously in conflict with an MIT-licensed upstream
- if you redistribute modified OpenClaw files, keep the upstream license notice intact

### FredOS

Current local FredOS package metadata does not yet declare a final published project license in `pyproject.toml`.

Practical meaning:

- this is your own code, so the publication decision is yours
- before public release, you should choose and add a root license for the GitHub package

Recommended options remain:

- `Apache-2.0`
- or `MIT`

## Direct OpenClaw Dependency Snapshot

Direct dependencies inspected from the local `node_modules` metadata include:

### Clearly permissive / low concern

- `@agentclientprotocol/sdk` — `Apache-2.0`
- `@anthropic-ai/vertex-sdk` — `MIT`
- `@aws-sdk/client-bedrock` — `Apache-2.0`
- `@clack/prompts` — `MIT`
- `@homebridge/ciao` — `MIT`
- `@line/bot-sdk` — `Apache-2.0`
- `@lydell/node-pty` — `MIT`
- `@mariozechner/pi-agent-core` — `MIT`
- `@mariozechner/pi-ai` — `MIT`
- `@mariozechner/pi-coding-agent` — `MIT`
- `@mariozechner/pi-tui` — `MIT`
- `@modelcontextprotocol/sdk` — `MIT`
- `@mozilla/readability` — `Apache-2.0`
- `@sinclair/typebox` — `MIT`
- `ajv` — `MIT`
- `chalk` — `MIT`
- `chokidar` — `MIT`
- `cli-highlight` — `ISC`
- `commander` — `MIT`
- `croner` — `MIT`
- `dotenv` — `BSD-2-Clause`
- `express` — `MIT`
- `file-type` — `MIT`
- `gaxios` — `Apache-2.0`
- `hono` — `MIT`
- `ipaddr.js` — `MIT`
- `jiti` — `MIT`
- `json5` — `MIT`
- `linkedom` — `ISC`
- `long` — `Apache-2.0`
- `markdown-it` — `MIT`
- `node-edge-tts` — `MIT`
- `osc-progress` — `MIT`
- `pdfjs-dist` — `Apache-2.0`
- `playwright-core` — `Apache-2.0`
- `qrcode-terminal` — `Apache 2.0`
- `sharp` — `Apache-2.0`
- `sqlite-vec` — `MIT OR Apache`
- `tar` — `BlueOak-1.0.0`
- `tslog` — `MIT`
- `undici` — `MIT`
- `uuid` — `MIT`
- `ws` — `MIT`
- `yaml` — `ISC`
- `zod` — `MIT`

### Needs explicit note

- `jszip` — `MIT OR GPL-3.0-or-later`

Why it matters:

- this is a dual-license package
- dual-license with `OR` is generally less risky than a pure GPL dependency
- the safe publication posture is to treat it as used under the MIT branch and avoid unnecessarily copying its source or vendored code into your own repo

## Direct FredOS Dependency Snapshot

Direct Python dependencies inspected from local package metadata include:

- `sqlalchemy` — `MIT`
- `fastapi` — MIT classifier
- `uvicorn` — BSD classifier
- `pydantic` — MIT classifier
- `pydantic-settings` — MIT classifier
- `httpx` — `BSD-3-Clause`

Two packages did not expose a clean `License` field in the local quick check:

- `alembic`
- `pytest`

This is not automatically a red flag.

It only means:

- the quick metadata path was incomplete
- they should be double-checked before a final public release if you want a cleaner audit log

## Risk Assessment

### No obvious blockers found

I did not find:

- AGPL in the inspected direct dependency set
- a clearly incompatible copyleft requirement in the core packaged path
- a license that obviously prevents a normal open-source publication of your wrapper/package

### Main practical cautions

1. Add your own top-level license before public release.
2. Keep OpenClaw upstream license notices intact.
3. Document clearly that `openclaw-overlay/` is an overlay against upstream OpenClaw, not a clean-room reimplementation.
4. Treat `jszip` as a dependency used under its MIT branch and avoid copying third-party source unnecessarily.
5. If you want a stronger release-grade audit, run a full transitive dependency license scan before public push.

## Recommended License Direction for Your Repo

Given the current dependency mix, both of these are practical:

- `MIT`
- `Apache-2.0`

My engineering recommendation remains:

- prefer `Apache-2.0` if you want a slightly clearer publication posture

Reason:

- permissive
- broadly compatible with the observed direct dependency mix
- clearer legal framing than MIT alone

## Before Public Push

Recommended final checks:

1. run one full transitive license scan for Node dependencies
2. run one full transitive license scan for Python dependencies
3. add your chosen root `LICENSE`
4. keep upstream attribution where required
5. keep secrets and local state out of the repo

