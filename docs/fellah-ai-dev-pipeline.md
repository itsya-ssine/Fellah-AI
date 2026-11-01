# Fellah AI: Development Pipeline for a Two-Person AI and Data Engineering Team

**Approach: web app (React PWA) wrapped as an Android app with Capacitor.**

Based on `docs/project-blueprint.md`. The work is split between **@rihabetm** and **@itsya-ssine**, step by step, following the phases of the project blueprint (Months 0-24).

---

## 0. How the Work Is Split

Both team members are AI and data engineers, so the split follows **system ownership**. Each owns a full vertical slice and reviews the other's work.

| | **@rihabetm: Vision and Farmer App** | **@itsya-ssine: Data, Irrigation, Language, Backend and Dashboard** |
|---|---|---|
| **Owns** | Diagnosis models, on-device inference (native plugin), vision MLOps, the farmer web app and its Capacitor packaging | Public data platform, irrigation engine, Darija/Amazigh content and audio pipeline, backend API, regional dashboard, shared API client |
| **Main deliverable** | An app that diagnoses plant photos offline in under 500 ms on a mid-range phone, evaluated on public in-the-wild data | A backend that serves advice, irrigation recommendations and sync |
| **Primary stack** | PyTorch, timm, Albumentations, TFLite, ONNX, MLflow, DVC, React, TypeScript, Vite, Capacitor, Kotlin (small plugin) | FastAPI, PostgreSQL + PostGIS, Redis, Celery, Open-Meteo, SoilGrids, Whisper/TTS, Docker, Next.js/React |
| **Backup for** | Backend API and CI/CD | Model training and evaluation, web app screens |

**Shared responsibilities**: architecture decisions, CI/CD, code review, the shared UI package, public dataset quality, final integration.

**Roles the team cannot cover and must contract**: native-speaker translators and voice talent, UX designer, business development. Labels come from public datasets and advice comes from cited public sources, so no agronomist, field team or farmer partner is required (see `docs/decisions/0003-public-datasets-only.md`).

### Working Rules

1. One monorepo (pnpm workspaces or Turborepo):
   ```
   /apps/farmer-app        React PWA + Capacitor (android/, ios/)
   /apps/dashboard         Regional dashboard (Next.js or React)
   /packages/ui            Shared components, theme, RTL and Tifinagh fonts
   /packages/api-client    Typed client generated from the OpenAPI spec
   /packages/i18n          Darija, Amazigh, French strings and audio IDs
   /plugins/tflite         Native Capacitor plugin for on-device inference
   /backend                FastAPI service
   /irrigation             FAO-56 engine (Python package)
   /ml                     Training, evaluation, export
   /content                Knowledge base, glossary, audio manifest
   /infra                  Terraform, Docker, CI
   /docs
   ```
2. Every feature goes through a pull request reviewed by the other engineer.
3. Weekly 1-hour sync plus a 15-minute async daily update.
4. Interfaces are **contracts first** (OpenAPI spec, model I/O spec, database schema) so both can work in parallel.
5. Every model and dataset is versioned. Nothing reaches the app without passing the validation gate.

---

## Phase 0: Discovery and Validation (Months 0-2)

Goal: fix the scope from public data, run the inference spike, and set up the public dataset registry.

### Shared steps

| # | Step | Output |
|---|---|---|
| 0.1 | Set technical constraints from public statistics and target-device assumptions: phone models, Android versions, connectivity, voice use. | Technical constraints summary |
| 0.2 | Choose **one region, 2-3 crops, one Amazigh variety**, and the priority disease list, based on class coverage in the public datasets. | Scope document |
| 0.3 | Compile the **public dataset registry** (PlantVillage, PlantDoc, PlantNet-300K, iNaturalist and others): license, crops, classes, image style, intended role. | `data/public_datasets/registry.csv` |
| 0.4 | Define success metrics: top-1/top-3 accuracy, "uncertain" rate, latency, offline success rate. | `docs/success-metrics.md` |

### @rihabetm

| # | Step | Output |
|---|---|---|
| A0.1 | Write the **evaluation protocol**: public train and held-out sets, cross-dataset tests, leakage rules, robustness tests. | `docs/evaluation-protocol.md` |
| A0.2 | Benchmark 3-4 backbones (MobileNetV3, EfficientNet-Lite, MobileViT) on a public dataset for size, accuracy and latency. | Benchmark notebook and table |
| A0.3 | **Inference spike (week 1-2, go/no-go)**: run the same quantized model three ways on 3-4 low and mid-range Android phones (Android 8+, 2-3 GB RAM): (1) ONNX Runtime Web (WASM, SIMD), (2) TensorFlow.js, (3) native TFLite called from a minimal Capacitor plugin. Measure latency, peak memory, battery drain, and app startup time. | Spike report and decision |
| A0.4 | Test the **WebView** on the oldest target phones: rendering, camera capture, audio playback, Tifinagh font, RTL layout. | WebView compatibility report |

**Go/no-go rule for the spike** (thresholds set by both engineers before running it):
- Web inference acceptable if it is under about 1.5 s per image and stays well within memory limits on a 2 GB phone without crashes.
- Otherwise, use the **native TFLite plugin** (target under 500 ms).
- If even the WebView itself is unreliable on target phones, escalate the decision to Flutter before building more.

### @itsya-ssine

| # | Step | Output |
|---|---|---|
| B0.1 | Build the **public dataset ingestion pipeline**: download with checksums and normalize into one schema (image, crop, label, source dataset, license, split). | Ingestion script, dataset v0 |
| B0.2 | Prototype the **irrigation engine in a notebook** for one crop using Open-Meteo (ET0, Kc, simple water balance). | `irrigation/prototype.ipynb` |
| B0.3 | Draft the **database schema** (users, plots, diagnoses, advice, irrigation logs). | ERD and SQL draft |
| B0.4 | Test data sources: Open-Meteo, NASA POWER, SoilGrids (coverage, resolution, rate limits, failure modes). | Data source assessment |
| B0.5 | Set up the **monorepo skeleton** and a hello-world PWA deployed on staging, so the web pipeline exists from week 2. | Working monorepo |

**Phase 0 exit criteria**: scope fixed, spike decision made, public dataset registry and ingestion working, irrigation prototype producing plausible numbers.

---

## Phase 1: Data and Knowledge Foundation (Months 2-6)

Goal: build the assets that matter most: the curated public dataset, the source-cited knowledge base, the infrastructure, and the app shell.

### Shared steps

| # | Step | Output |
|---|---|---|
| 1.1 | Set up GitHub Actions: lint, type-check, unit tests, web build, Android build (Gradle) with signed debug APKs as artifacts. | Working CI |
| 1.2 | Set up cloud foundation with Terraform: storage bucket, database, container registry, staging environment. | `infra/` |
| 1.3 | Agree on the **API contract** (OpenAPI) and the **model I/O contract** (input size, normalization, class list, confidence format). Generate the TypeScript client from the OpenAPI spec. | `docs/api.yaml`, `packages/api-client`, `docs/model-contract.md` |
| 1.4 | Agree on the **design system** with the UX designer: large touch targets, pictograms, high contrast for sunlight, RTL, Tifinagh font. Build it once in `packages/ui`. | Shared UI package |

### @rihabetm: Vision data and app shell

| # | Step | Output |
|---|---|---|
| A1.1 | Set up **DVC** for datasets and **MLflow** for experiments. | Reproducible tracking |
| A1.2 | Build **dataset curation tooling**: taxonomy map across datasets, duplicate detection, and automated label-noise flagging (for example confident learning). | `ml/src/datasets/` |
| A1.3 | Build **robustness test sets** from the public held-out data: blur, lighting, background and JPEG perturbations that mimic phone cameras. | Robustness test sets |
| A1.4 | Build **data-quality checks**: blur, duplicates, exposure, minimum resolution. Also run a light blur/exposure check on the device before upload. | `ml/quality_checks.py` |
| A1.5 | Create **leakage-safe splits**: deduplicate (including augmented copies), keep images of the same source plant together where metadata allows, never split randomly by image, and hold out whole datasets (for example train on PlantVillage, test on PlantDoc). Freeze the held-out **public test set**. | Split script and frozen test set |
| A1.6 | Assemble the **training data** from public sets (PlantVillage, PlantDoc, PlantNet-300K, iNaturalist); document the domain gap between lab-style and in-the-wild images. | Training dataset and notes |
| A1.7 | Build the **app shell**: React Router, state management, i18n (Darija, Amazigh, French), RTL, Tifinagh font, phone-OTP login screens, PWA manifest and service worker (Workbox). | App shell v0 |
| A1.8 | Set up **Capacitor**: Android project, app signing, Camera, Filesystem, Network, Preferences and Push Notifications plugins, and the SQLite plugin for local data. | Android build running on test phones |

### @itsya-ssine: Knowledge base, language and data platform

| # | Step | Output |
|---|---|---|
| B1.1 | Build the **knowledge base schema** and content pipeline: disease sheets, treatments (cultural, then biological, then approved chemical), irrigation parameters (Kc per stage, root depth, depletion threshold). Every entry cites a public source (FAO, EPPO, ONSSA public lists, research publications). | Structured JSON/YAML in `/content` |
| B1.2 | Build **validation tooling**: every advice entry needs at least one public source (title, URL, retrieval date), and chemicals are checked against the public ONSSA approved list (dose, pre-harvest interval, safety copied from label data). Unsourced entries cannot be published. | `content/validate.py` |
| B1.3 | Build the **glossary** (crop, disease, pest, product terms) in French, Arabic, Darija and the chosen Amazigh variety, seeded from public vocabularies (for example FAO AGROVOC) and reviewed by translators. | Versioned glossary |
| B1.4 | Build the **translation and audio pipeline**: advice template, translation review, recording, audio file, with IDs linking text and audio. Encode audio as small compressed files (for example Opus) for weak connections. | Audio library v1 |
| B1.5 | Build the **data ingestion layer**: scheduled Celery jobs pulling weather forecasts and history into PostgreSQL/PostGIS, with fallback between sources. | Weather service |
| B1.6 | Build the **soil data fetcher** (SoilGrids lookup by coordinates). | Soil service |
| B1.7 | Set up data-protection basics: user data is never used for training, retention limits, and deletion (Law 09-08). | Retention policy and delete endpoint |
| B1.8 | Build the **backend skeleton** (FastAPI) serving the OpenAPI contract with mock data so @rihabetm can build screens against it from day one. | API mock on staging |

**Phase 1 exit criteria**: every priority class covered by registered public data with a documented license and domain gap, a frozen public test set, a source-cited knowledge base for the priority crops, audio library for priority advice, daily weather and soil ingestion, and an installable Android build of the app shell.

---

## Phase 2: MVP Build (Months 4-9)

Goal: working app, models, irrigation engine and backend. Many steps run in parallel.

### @rihabetm: Diagnosis model, inference plugin and farmer web app

| # | Step | Output |
|---|---|---|
| A2.1 | **Baseline model**: transfer learning (MobileNetV3 or EfficientNet-Lite), pretrained on lab-style public data, fine-tuned on in-the-wild public data with strong augmentation (lighting, blur, background, rotation). | Model v0.1, MLflow run |
| A2.2 | **Evaluate honestly** on the frozen public held-out test set and the robustness sets: per-class precision/recall, top-1/top-3, confusion matrix for look-alikes, calibration curve. | Evaluation report |
| A2.3 | **Fix weak classes**: add more public data, class weighting, hard-example mining, automated label-error review. Repeat until targets are met. | Model v0.2+ |
| A2.4 | Build the **crop classifier** and **out-of-distribution detector** (reject hands, soil, non-plants, blurry photos). Tune thresholds for the "not sure, retake the photo" fallback. | Gatekeeper models |
| A2.5 | **Calibrate confidence** (temperature scaling). | Calibrated model |
| A2.6 | **Compress and export**: INT8 quantization to TFLite (and ONNX if the web path is kept). Verify accuracy loss against the float model. Targets: under 25 MB, under 500 ms on a mid-range phone. | Mobile model artifact |
| A2.7 | Build the **native TFLite Capacitor plugin** (Kotlin): `classify(imagePath)` returns top-3 classes, confidences and OOD score; loads models from app storage so they can be updated without a Play Store release; hardware acceleration (NNAPI/GPU delegate) with CPU fallback. Provide a **web fallback** (ONNX Runtime Web) for the PWA in a browser. | `plugins/tflite` with unit and device tests |
| A2.8 | Build the **farmer app screens**: onboarding, plot creation (map pin, crop, planting date, irrigation method), camera with capture guidance, diagnosis result (top-3 plus confidence), advice screen with audio, irrigation card. Use the native camera plugin rather than the browser camera for focus and resolution control. | App beta |
| A2.9 | Build the **offline layer**: SQLite (Capacitor plugin) for plots, advice and queued uploads; service worker caches the app shell and audio; resumable image upload with compression; sync with conflict handling. | Offline mode |
| A2.10 | Implement **audio-first UI** with the designer: large buttons, pictograms, audio playback controls, handling of audio autoplay limits (audio starts from an explicit tap), RTL, Tifinagh. | UI complete |
| A2.11 | Build **over-the-air updates**: model download with checksum and rollback, and web-layer updates (a live-update service or self-hosted) for non-native changes. Keep native plugin changes tied to Play Store releases. | Update system |
| A2.12 | Build the **cloud re-check endpoint** with the larger model for low-confidence cases (FastAPI/Triton). | Cloud inference service |
| A2.13 | Set up the **model validation gate in CI**: a new model cannot be released unless it beats the current one on the frozen public test set and meets size and latency limits on a reference device. | Automated gate |

### @itsya-ssine: Irrigation, backend and dashboard

| # | Step | Output |
|---|---|---|
| B2.1 | Turn the notebook into the production **irrigation engine** (FAO-56): ET0 (Penman-Monteith, Hargreaves fallback), Kc by growth stage, soil water balance, depletion threshold, rain and irrigation inputs. | `irrigation/` package with unit tests |
| B2.2 | Convert water need into **practical units**: minutes of drip, furrow turns, liters per tree. | Recommendation formatter |
| B2.3 | **Validate the engine** against FAO-56 worked examples and published reference values, and cross-check ET0 between Open-Meteo, NASA POWER and ERA5; test edge cases (heat wave, heavy rain, missing weather). Start conservative. | Validation report |
| B2.4 | Build **backend API v1** (FastAPI): OTP auth, users, plots, diagnoses, advice, irrigation, sync, notifications. Replace the mocks from B1.8 endpoint by endpoint. | API v1 on staging |
| B2.5 | Build the **daily batch job**: per plot, fetch weather, update water balance, generate "irrigate / wait / reduce" advice, queue notifications. | Scheduled pipeline |
| B2.6 | Build the **advice delivery endpoint**: text and audio URLs in the requested language and script, from the validated knowledge base only. | Advice service |
| B2.7 | Build **notifications**: FCM push through Capacitor, plus SMS/WhatsApp fallback for frost, heat wave and irrigation alerts. | Notification service |
| B2.8 | Build the **abstain flow**: low-confidence or out-of-distribution results return "not sure, retake the photo" with capture tips. No human review. | Abstain workflow |
| B2.9 | Build the **regional dashboard** (React/Next.js + MapLibre) on top of `packages/ui` and `packages/api-client`: weather, ET0 and irrigation-need maps from public data. | Dashboard v0 |
| B2.10 | Add **observability**: structured logs, Sentry (web and Android), Prometheus/Grafana, alerts on failed daily jobs and weather API failures. | Monitoring |
| B2.11 | Implement **heat wave, frost and heavy-rain alert logic** from public forecast data. | Alert rules |
| B2.12 | Support **sync and caching headers** on the API for low bandwidth: delta sync, compressed responses, idempotent uploads. | Sync API |

### Shared in Phase 2

| # | Step | Output |
|---|---|---|
| 2.1 | Integrate the app with the backend (auth, sync, advice, irrigation card, notifications). @rihabetm owns the client, @itsya-ssine owns the server. | End-to-end flow |
| 2.2 | **End-to-end tests**: photo to diagnosis to advice in Darija/Amazigh with audio, on real low-end phones, online and offline (Playwright for web, Appium or manual device runs for the Android build). | Test suite |
| 2.3 | **Performance budget**: app size (target under 50 MB APK/AAB including model), startup time, memory, and battery on the oldest target phone. | Performance report |
| 2.4 | **Accessibility checks** with the designer: contrast, touch target size, RTL, Tifinagh rendering, audio-first flows, using automated tools and guidelines. | UX fixes |
| 2.5 | **Security review**: encryption in transit and at rest, plot location protection, secure token storage (not plain web storage), deletion flows, pesticide safety warnings. | Checklist completed |
| 2.6 | Prepare **Play Store release**: signing keys, privacy policy, data safety form, closed testing track. | Internal/closed test release |

**Phase 2 exit criteria**: the Android app installs on Android 8+ with 2 GB RAM, diagnosis works offline, irrigation advice arrives daily, advice is in Darija and one Amazigh variety with audio, and models meet the agreed bar on the frozen public test set.

---

## Phase 3: Public-Data Evaluation and Hardening (Months 9-14)

Goal: prove model and engine quality on public benchmarks and on-device tests, and harden the system for release.

### Shared steps

| # | Step | Output |
|---|---|---|
| 3.1 | Production deployment: release process, rollback plan, backups, staged rollout on the Play Store. | Live production system |
| 3.2 | Publish a **model card and benchmark report**: datasets used, licenses, domain gap, per-class results, known limits. | `docs/model-card.md` |
| 3.3 | Weekly review: crashes (Sentry), failed jobs, API errors. | Weekly ops review |

### @rihabetm

| # | Step | Output |
|---|---|---|
| A3.1 | Run the **robustness and calibration evaluation** on the perturbed public sets (blur, lighting, background, compression) and report the degradation per class. | Robustness report |
| A3.2 | Track **model quality across releases** on the frozen public test sets: confidence drift, abstain rate, per-class regressions. | Monitoring dashboard |
| A3.3 | **Retrain** when new public datasets or dataset versions are added (check licenses first), pass the validation gate, ship through the OTA model update. | Model v1.x |
| A3.4 | Fix real-device issues: WebView quirks, memory, battery, camera behavior on specific brands. | App patches |

### @itsya-ssine

| # | Step | Output |
|---|---|---|
| B3.1 | **Backtest the engine** on public reference data: FAO-56 worked examples and historical ERA5 and NASA POWER weather for past seasons (no negative storage, plausible seasonal totals). | Backtest report |
| B3.2 | **Recalibrate** Kc, thresholds and soil parameters against published FAO-56 values and the sensitivity analysis. | Engine v1.1 |
| B3.3 | **Sensitivity analysis** of the engine (soil, Kc, weather source). Reproducible notebook. | `docs/irrigation-sensitivity.ipynb` |
| B3.4 | Estimate **unit economics** from load tests: cloud and SMS cost per active user per month. | Cost report |
| B3.5 | Improve language: automated checks for text/audio ID parity, script and RTL rendering; expand the audio library. | Content v2 |

**Phase 3 exit criteria**: published model card and benchmark report, improved models and engine, estimated cost per active user.

---

## Phase 4: Launch and Scale (Months 14-24)

### @rihabetm

| # | Step | Output |
|---|---|---|
| A4.1 | Extend to **new crops and conditions** using the standard pipeline (add public data, map taxonomy, train, validate, ship). Document it as a playbook. | Crop onboarding playbook |
| A4.2 | Add **severity estimation** or segmentation for the highest-value diseases (optional). | Model extension |
| A4.3 | Build the **iOS version** from the same codebase (Capacitor iOS project plus a Core ML or TFLite version of the inference plugin). | iOS app |
| A4.4 | Add **NDVI stress detection** per plot (Sentinel-2) as an early-warning signal (with @itsya-ssine). | NDVI pipeline |

### @itsya-ssine

| # | Step | Output |
|---|---|---|
| B4.1 | Add the **WhatsApp bot and SMS/USSD** channels for weak connectivity and feature phones. | Messaging channels |
| B4.2 | Full **regional dashboard**: weather and water-need heatmaps, water-need reports, subscription and invoicing, exports for donors and certification. | Dashboard v1 |
| B4.3 | Add other **Amazigh varieties** (Central Atlas, Tarifit); fine-tune **speech-to-text** (Whisper) on public speech corpora where the license allows; evaluate neural TTS (VITS) when enough recordings exist. | Language expansion |
| B4.4 | Build the **RAG assistant**: retrieval from the vetted knowledge base only, citations, refusal when unsure, **no generated chemical doses**. | Assistant v1 |
| B4.5 | Evaluate optional **ML correction layers** on top of FAO-56 using public reference datasets; keep rule-based FAO-56 as the default. | Engine v2 |
| B4.6 | Add the **supplier marketplace** links with independent ranking (non-chemical first, agronomic fit, sponsored items labeled). | Marketplace module |
| B4.7 | Prepare **multi-region and multi-country** configuration (dialects, regional weather sources, tenant isolation). | Scalable config |

### Shared steps

| # | Step | Output |
|---|---|---|
| 4.1 | Scale infrastructure (autoscaling, cost monitoring, disaster recovery). | Production hardening |
| 4.2 | Contribute technical sections to publications and grant applications. | Benchmark paper and grant material |
| 4.3 | Hire or contract additional engineers; use the playbooks and docs already written. | Onboarded hires |

---

## Timeline at a Glance

| Months | @rihabetm | @itsya-ssine |
|---|---|---|
| 0-2 | Evaluation protocol, backbone benchmarks, **inference spike**, WebView tests | Public dataset registry and ingestion, irrigation prototype, schema, data sources, monorepo skeleton |
| 2-6 | DVC/MLflow, dataset curation tooling, robustness sets, leakage-safe splits, public training data, app shell, Capacitor setup | Knowledge base, source validation, glossary, audio pipeline, weather/soil ingestion, data protection, API mock |
| 4-9 | Model training, OOD, calibration, quantization, native TFLite plugin, app screens, offline sync, OTA updates | FAO-56 engine, backend API, daily jobs, notifications, abstain flow, dashboard v0, monitoring |
| 9-14 | Robustness evaluation, release monitoring, retraining, WebView/device fixes | Engine backtest and recalibration, sensitivity analysis, unit economics, content v2 |
| 14-24 | New crops, NDVI, iOS | WhatsApp/SMS/USSD channels, full dashboard, Amazigh varieties, STT/TTS, RAG, marketplace |

---

## Interfaces and Handoffs

| Interface | Owner | Consumer | Contract |
|---|---|---|---|
| Mobile model artifact (TFLite, ONNX) | @rihabetm | App (@rihabetm), model metadata endpoint (@itsya-ssine) | Model I/O spec, class list, version, checksum, thresholds |
| Native plugin API (`classify`) | @rihabetm | Web app code (@rihabetm) | TypeScript definitions in `plugins/tflite` |
| API client | @itsya-ssine (spec), generated | App (@rihabetm), dashboard (@itsya-ssine) | OpenAPI to TypeScript client |
| Diagnosis result | @rihabetm (client), @itsya-ssine (server) | Both | OpenAPI schema |
| Advice content and audio | @itsya-ssine | App (@rihabetm) | Content IDs, language, script, audio URL |
| Irrigation recommendation | @itsya-ssine | App (@rihabetm) | JSON: action, amount, unit, reason, confidence, date |
| Public dataset (normalized) | @itsya-ssine | @rihabetm (training) | Dataset schema plus source dataset and license fields |
| Shared UI package | Both | App and dashboard | `packages/ui` with a visual test per component |

---

## Definition of Done for Any Feature

1. Code reviewed by the other engineer and merged through CI.
2. Unit and integration tests pass; TypeScript has no type errors.
3. For models: passes the validation gate on the frozen public test set.
4. For advice content: every entry cites a public source and chemicals match the public ONSSA approved list.
5. Tested on a real low-end Android phone through the Capacitor build, including offline.
6. Works in RTL and with the Tifinagh font where text is shown.
7. Documented in `/docs`.

---

## Technical Risks Specific to the Web + Capacitor Approach

| Risk | What to do |
|---|---|
| Web inference too slow or memory-hungry on 2 GB phones | Decide at the Phase 0 spike; use the native TFLite plugin as the default path |
| Outdated Android WebView on cheap phones | Test oldest targets early; show an in-app prompt to update WebView; set a minimum supported version |
| Browser storage cleared by the system | Use SQLite through a Capacitor plugin for all important data; keep only UI preferences in web storage |
| Weak background sync and notifications in a web layer | Use native push (FCM) through Capacitor; sync on app open and when connectivity returns; keep SMS/WhatsApp fallback for critical alerts |
| Audio autoplay restrictions | Start audio only from an explicit tap; preload and cache audio files |
| Two small native codebases to maintain (plugin on Android, later iOS) | Keep the plugin tiny and well tested; keep all business logic in TypeScript |
| Play Store policy on updating app code remotely | Use OTA only for web assets and model files; native changes always go through store releases |
| App size growth (model plus audio plus web assets) | Set a size budget in CI; download audio and larger models on demand |
| Too much scope for two people | Hold the MVP to 2-3 crops and one Amazigh variety; use recorded audio, curated templates and rule-based irrigation first |
| Models fail on real field photos (domain gap from public data) | Train on in-the-wild public sets, augment for phone-camera conditions, evaluate cross-dataset, abstain via OOD, keep the frozen public test set untouched, state limits in the model card |
| Noisy public labels | Deduplicate, map taxonomies, flag label noise automatically, drop or down-weight suspect samples |
| No human review of advice | Mandatory source citations, chemical data copied only from the public ONSSA list, no generated doses, automated validation blocks unsourced entries |
| Single point of failure on each slice | Document everything, cross-review, and make each engineer able to deploy the other's component |

---

## First 30 Days (Technical Checklist)

- [ ] Agree on the split in this document; set up the monorepo, CI and cloud account.
- [ ] A: run the **inference spike** (ONNX Runtime Web vs. TF.js vs. native TFLite) on 3-4 low-end Android phones and write the decision.
- [ ] A: test the Android WebView on the oldest target phones (camera, audio, RTL, Tifinagh).
- [ ] A: write the evaluation protocol.
- [ ] B: build the public dataset registry and ingestion pipeline.
- [ ] B: run the irrigation prototype for one crop with Open-Meteo data and check it against FAO-56 worked examples.
- [ ] B: draft the database schema; deploy a hello-world PWA to staging.
- [ ] Both: choose the region and crops, then define the priority disease list from public dataset coverage.
