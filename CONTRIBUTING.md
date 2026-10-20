# Contributing

## Workflow
1. Pick or create an issue from the task template; reference the pipeline step (for example A0.3).
2. Branch from `main`: `feat/a0-3-inference-spike`, `fix/b2-5-daily-job`, `docs/api-contract`.
3. Keep pull requests small. The other engineer reviews every PR. No direct pushes to `main`.
4. Squash merge with a Conventional Commit title.

## Commit messages (Conventional Commits)
`type(scope): summary` in the imperative, 72 characters or fewer.

Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `perf`, `ci`.
Scopes: `app`, `dashboard`, `ui`, `api`, `i18n`, `plugin`, `backend`, `irrigation`, `ml`, `content`, `data`, `infra`, `docs`.

Examples:
- `feat(irrigation): add Hargreaves ET0 fallback`
- `docs(ml): record inference spike results`

## Contracts first
Change `docs/api.yaml` or `docs/model-contract.md` in a PR **before** the code that depends on them, and tag the other engineer.

## Never commit
Real farmer data, photos, phone numbers, API keys, `.env` files, model binaries, or audio files.
