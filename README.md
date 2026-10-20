# Fellah AI

Crop disease diagnosis and irrigation guidance for smallholder farmers, in Darija and Amazigh.
A farmer photographs a sick plant, gets a diagnosis and treatment advice (text and audio), and receives daily irrigation recommendations.

**Approach:** React PWA wrapped with Capacitor for Android, a FastAPI backend, an FAO-56 irrigation engine, and on-device diagnosis through a native TFLite plugin.

## Repository layout

```
apps/
  farmer-app/        React PWA + Capacitor (@rihabetm)
  dashboard/         Cooperative dashboard (@itsya-ssine)
packages/
  ui/                Shared components and theme
  api-client/        Client generated from docs/api.yaml
  i18n/              Darija, Amazigh, French strings and audio IDs
plugins/
  tflite/            Native on-device inference plugin (@rihabetm)
backend/             FastAPI service (@itsya-ssine)
irrigation/          FAO-56 engine (@itsya-ssine)
ml/                  Training, evaluation, export, spikes (@rihabetm)
content/             Knowledge base, glossary, audio manifest (@itsya-ssine)
data/                Data docs only; real data via DVC
infra/               Terraform, Docker, CI config
docs/                Blueprint, pipeline, contracts, decisions, tasks
```

## Getting started

```bash
# JavaScript workspaces
corepack enable && pnpm install

# Backend
cd backend && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && pytest

# Irrigation engine
cd ../irrigation && pip install -r requirements.txt && pytest
```

## Where to start

Read `docs/tasks/phase0-first-tasks.md`. The full plan is in `docs/fellah-ai-dev-pipeline.md`.

## Ownership

| | Owns |
|---|---|
| **@rihabetm** | Diagnosis models, native inference plugin, farmer app |
| **@itsya-ssine** | Data platform, irrigation engine, language content, backend, dashboard |

See `CONTRIBUTING.md` for workflow rules.
