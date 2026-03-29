# Publish Checklist

Date: 2026-03-30
Scope: GitHub publication readiness for `FOSforGithubRepo`

## Completed in This Packaging Pass

- [x] Created a GitHub-ready package under `FOSforGithubRepo`
- [x] Split the package into:
  - `fredos/`
  - `openclaw-overlay/`
  - `openclaw-state-template/`
  - `docs/`
- [x] Excluded live `.openclaw` runtime state
- [x] Excluded `fredos.db`
- [x] Excluded `fredos_data/`
- [x] Excluded `.env`
- [x] Excluded obvious gateway/auth/Discord tokens from packaged files
- [x] Added `.gitignore`
- [x] Added human-facing `README.md`
- [x] Added `README_FOR_AI.md`
- [x] Added state/bootstrap templates
- [x] Added OpenClaw overlay apply/init scripts
- [x] Added architecture and validation docs
- [x] Removed Python bytecode caches from packaged `fredos/`

## Manual Checks Before Push

- [ ] Decide final repo name
- [ ] Decide final license
- [ ] Decide whether the initial push is public or private
- [ ] Confirm the upstream OpenClaw version/commit you want to document as the official base
- [ ] Re-read `README.md` as a first-time visitor
- [ ] Re-read `README_FOR_AI.md` as a fresh-machine installer

## Security Checks Before Push

- [ ] Run one more secret scan across the final repo folder
- [ ] Confirm no real `.env` values remain
- [ ] Confirm no real OAuth profile data remains
- [ ] Confirm no Discord token remains
- [ ] Confirm no gateway token remains
- [ ] Confirm no local DB files remain

## Documentation Checks Before Push

- [ ] Confirm architecture docs still match the current code
- [ ] Confirm the project assignment policy file is included
- [ ] Confirm the worker schema file is included
- [ ] Confirm the subagent execution record is included
- [ ] Confirm README references valid local paths inside the packaged repo

## Optional Cleanup Before Push

- [ ] Add a final license file once the license decision is made
- [ ] Add a root `CHANGELOG.md`
- [ ] Add a short `CONTRIBUTING.md`
- [ ] Add a small diagram later if you want a more visual repo landing page

## Recommended Push Order

1. create the new GitHub repository
2. copy or initialize git inside `FOSforGithubRepo`
3. review `git status`
4. run a final secret scan
5. make the first commit
6. push to GitHub
7. test the install guide on a clean clone or second machine

## Current Recommendation

This package is ready for a **careful first push**, provided the remaining manual checks above are completed.
