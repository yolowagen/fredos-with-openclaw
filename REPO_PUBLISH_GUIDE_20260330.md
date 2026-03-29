# Repo Publish Guide

Date: 2026-03-30

## Purpose

This note summarizes three publication decisions:

1. recommended GitHub repo naming
2. recommended license direction
3. recommended release posture for the first public push

## Recommended Repo Naming

Good names for this package should communicate that this is:

- FredOS-centered
- OpenClaw-integrated
- a packaged architecture/runtime kit

Recommended options:

1. `fredos-openclaw`
2. `fredos-openclaw-runtime`
3. `fos-runtime-kit`

Recommended default:

- `fredos-openclaw`

Why:

- shortest and clearest
- accurately describes the architecture split
- easy to understand for new readers
- leaves room for subdirectories such as `fredos/` and `openclaw-overlay/`

## License Recommendation

This package does not yet include a final license file.

That is safer than publishing the wrong one too early.

Recommended options:

### Option A: MIT

Best when:

- you want the least friction for reuse and experimentation
- you are comfortable with broad reuse

Pros:

- simple
- common
- contributor-friendly

Tradeoff:

- very permissive

### Option B: Apache-2.0

Best when:

- you want permissive reuse
- you also want clearer patent language

Pros:

- still open and contributor-friendly
- more explicit legal framing than MIT

Tradeoff:

- slightly heavier than MIT

### Option C: Wait before adding a license

Best when:

- you want to publish the code privately first
- you are not yet ready to authorize reuse

Pros:

- avoids accidental over-permission

Tradeoff:

- public GitHub visibility without a license can confuse contributors

## Practical Recommendation

If your goal is to let others inspect, learn from, and build on the architecture:

- choose `Apache-2.0`

If your goal is to minimize friction and optimize for fast community adoption:

- choose `MIT`

If you are still unsure:

- keep the repo unpublished or private until you decide

## First Public Push Recommendation

For the first public version:

- publish the sanitized package only
- do not include a live `.openclaw` state
- do not include a prefilled database
- do not include machine-local logs
- clearly document the upstream OpenClaw dependency and overlay model

## Suggested Release Posture

Version label suggestion:

- `v0.1.0`

Meaning:

- architecture is real
- local validation exists
- APIs and worker contracts are still evolving

## Suggested Repo Description

Suggested GitHub description:

`FredOS + OpenClaw local-first agent runtime package with canonical task/memory governance and bounded subagent orchestration.`

