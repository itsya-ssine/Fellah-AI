# Phase 0: first tasks

Goal: fix scope from public data, run the inference spike, set up the public dataset registry.
Full details: `docs/fellah-ai-dev-pipeline.md`.

## Shared
- [ ] Turn on branch protection for `main` (PR required, 1 review, CI must pass)
- [ ] Set the inference spike thresholds (`ml/spikes/inference_benchmark/README.md`)
- [ ] Choose region, 2-3 crops and the priority disease list from public dataset class coverage
- [ ] Fill in `docs/success-metrics.md` targets

## @rihabetm
| Step | Task | Where |
|---|---|---|
| A0.1 | Write the evaluation protocol (public train/held-out split, cross-dataset tests) | `docs/evaluation-protocol.md` |
| A0.2 | Benchmark MobileNetV3, EfficientNet-Lite, MobileViT on a public dataset | `ml/` |
| **A0.3** | **Inference spike: ONNX Runtime Web vs TF.js vs native TFLite on 3-4 low-end Android phones, then write the decision** | `ml/spikes/inference_benchmark/`, `docs/decisions/0002-inference-path.md` |
| A0.4 | WebView compatibility test (camera, audio, RTL, Tifinagh) on oldest target phones | `docs/` |

Branch: `feat/a0-3-inference-spike`

## @itsya-ssine
| Step | Task | Where |
|---|---|---|
| **B0.1** | **Public dataset registry and ingestion pipeline** | `data/public_datasets/` |
| B0.2 | Irrigation prototype notebook for one crop using Open-Meteo | `irrigation/notebooks/` |
| B0.3 | Database schema draft | `backend/` and `docs/` |
| B0.4 | Assess data sources: Open-Meteo, NASA POWER, SoilGrids | `docs/` |
| B0.5 | Hello-world PWA on staging | `apps/farmer-app/` |

Branch: `feat/b0-1-public-dataset-ingestion`

## Exit criteria
Scope fixed, spike decision made, public dataset registry and ingestion working, irrigation prototype producing plausible numbers.
