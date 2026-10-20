# Phase 0: first tasks

Goal: validate demand, fix scope, run the inference spike, start collecting data.
Full details: `docs/fellah-ai-dev-pipeline.md`.

## Shared
- [ ] Turn on branch protection for `main` (PR required, 1 review, CI must pass)
- [ ] Set the inference spike thresholds (`ml/spikes/inference_benchmark/README.md`)
- [ ] Confirm the agronomist partner and the pilot cooperative; draft the priority disease list
- [ ] Fill in `docs/success-metrics.md` targets

## @rihabetm
| Step | Task | Where |
|---|---|---|
| A0.1 | Write the photo collection protocol | `docs/photo-protocol.md` |
| A0.2 | Benchmark MobileNetV3, EfficientNet-Lite, MobileViT on a public dataset | `ml/` |
| **A0.3** | **Inference spike: ONNX Runtime Web vs TF.js vs native TFLite on 3-4 low-end Android phones, then write the decision** | `ml/spikes/inference_benchmark/`, `docs/decisions/0002-inference-path.md` |
| A0.4 | WebView compatibility test (camera, audio, RTL, Tifinagh) on oldest target phones | `docs/` |

Branch: `feat/a0-3-inference-spike`

## @itsya-ssine
| Step | Task | Where |
|---|---|---|
| **B0.1** | **WhatsApp-to-dataset ingestion pipeline** | `data/whatsapp_ingestion/` |
| B0.2 | Irrigation prototype notebook for one crop using Open-Meteo | `irrigation/notebooks/` |
| B0.3 | Database schema draft and consent fields | `backend/` and `docs/` |
| B0.4 | Assess data sources: Open-Meteo, NASA POWER, SoilGrids | `docs/` |
| B0.5 | Hello-world PWA on staging | `apps/farmer-app/` |

Branch: `feat/b0-1-whatsapp-ingestion`

## Exit criteria
Scope fixed, agronomist partner engaged, spike decision made, first photos collected, irrigation prototype producing plausible numbers.
