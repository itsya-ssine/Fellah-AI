# Fellah AI: Crop Disease and Irrigation Guidance for Smallholder Farmers

> A mobile app that lets a farmer photograph a sick plant, get a diagnosis and treatment advice in **Darija or Amazigh**, and receive **irrigation timing** based on weather and soil data. Sold to cooperatives by subscription, with commissions from input suppliers.

*(Working name: "Fellah AI". Change it freely.)*

---

## 1. Executive Summary

Smallholder farmers in North Africa lose a large share of their harvest to diseases, pests and poor water management. Drought is making each of these losses worse. Agronomic advice exists, but it rarely reaches farmers: extension officers are stretched thin, most advice is in French or Modern Standard Arabic, and many farmers (especially Amazigh-speaking ones in the Atlas, Souss and Rif) are left out entirely.

**Fellah AI** puts an agronomist in the farmer's pocket:

1. **Diagnose**: take a photo of a leaf, fruit or plant; get the likely disease or pest with a confidence level.
2. **Treat**: get step-by-step advice (cultural, biological, then chemical as a last resort) in Darija or Amazigh, in text and voice.
3. **Irrigate**: get a daily "water now / wait / reduce" recommendation per plot, based on local weather, crop stage and soil.
4. **Follow the region**: a regional dashboard shows weather and water-need indicators built from public data.

---

## 2. Problem Statement

| Issue | Detail |
|---|---|
| Crop losses | Diseases, pests and weeds cause significant yield losses every season (commonly cited global figures are 20-40%; local figures should be checked against public sources). |
| Late or wrong diagnosis | Farmers identify problems late, or confuse fungal, bacterial and nutrient problems, leading to wasted or harmful pesticide use. |
| Water mismanagement | Irrigation by habit or tradition rather than by crop need wastes scarce water and money (pumping, diesel, electricity). |
| Climate pressure | Drought, heat waves and irregular rainfall are increasing across Morocco and North Africa. |
| Language gap | Most digital agri-tools are in French, English or standard Arabic; Darija and Amazigh (Tashelhit, Tamazight, Tarifit) are almost absent. |
| Advice gap | Few extension agents per farmer; many farmers have no access to agronomists. |
| Connectivity | Rural areas often have weak or intermittent mobile data. |

---

## 3. Target Users and Customers

**End users (farmers)**
- Smallholders (0.5-10 ha), growing e.g. olives, citrus, tomatoes, potatoes, wheat/barley, argan, dates, vegetables, almonds, saffron.
- Low to medium digital literacy; Android smartphones (entry level); some low-literate users, so voice and icon-based UI are essential.

**Paying customers**
- Agricultural cooperatives and unions of cooperatives (primary).
- Later: agro-processors and exporters (traceability and quality), banks/insurers (risk data), NGOs and development programs, input suppliers (lead generation).

**Public data and reference sources**
- Datasets and publications: PlantVillage, PlantDoc, PlantNet-300K, iNaturalist, FAO-56, FAO AGROVOC, and published research from INRA Maroc and universities.
- Regulatory lists: the public ONSSA approved pesticide list.
- Weather, soil and satellite: Open-Meteo, NASA POWER, ERA5, SoilGrids, Sentinel-2.

**Funders**
- Funders: ADA (Agence pour le Developpement Agricole), international development agencies, impact investors.

---

## 4. Core Features

### 4.1 MVP (must have)

1. **Photo diagnosis**
   - Camera capture with guidance ("get closer", "show the underside of the leaf", "avoid shadows").
   - Crop selection (or auto-detection), then disease/pest/nutrient-deficiency prediction with top-3 results and confidence.
   - "Not sure" fallback that asks the user to retake the photo instead of guessing.
2. **Treatment advice**
   - Structured advice: what it is, how it spreads, what to do now, how to prevent it.
   - Ordered by priority: cultural practices, biological controls, then approved chemical options (only products registered in Morocco, with dose, pre-harvest interval and safety).
   - Delivered in Darija (Arabic script) and Amazigh (Tifinagh and Latin), as text **and audio**.
3. **Irrigation advisor**
   - Farmer creates a plot (location pin, crop, planting date, irrigation method: drip, furrow, sprinkler, flood); soil comes from public soil data.
   - Daily recommendation: *irrigate today / wait / how many minutes or liters*.
   - 7-day outlook and alerts for heat waves, frost, and rain.
4. **Offline-first behavior**
   - On-device model for diagnosis; cached advice; sync when connected.
5. **Voice-first, icon-first UI**
   - Large buttons, audio prompts, minimal text.

### 4.2 Phase 2

- Plot history and crop diary (treatments, irrigation, costs, yield).
- Satellite vegetation index (NDVI) per plot to spot stress early.
- Regional dashboard (see 4.3).
- WhatsApp bot and SMS/USSD fallback for feature phones and weak data.
- Marketplace links to certified input suppliers (commission source).

### 4.3 Regional Dashboard (web)

- Maps of weather, ET0 and irrigation need built from public data.
- Heat wave, frost and heavy-rain alerts from public forecasts.
- Water-need reports.
- Subscription and invoicing.
- Exportable reports for donors and certification (GlobalG.A.P., organic).

### 4.4 Phase 3

- Yield prediction and harvest planning.
- Expansion to Algeria, Tunisia, Mauritania, Egypt and other dialects.

---

## 5. Solution Architecture

```
 ┌───────────────┐      ┌────────────────────────┐      ┌─────────────────────┐
 │ Mobile app    │◄────►│ Backend API (cloud)    │◄────►│ Data & ML platform  │
 │ (Android first│      │ Auth, plots, advice,   │      │ Training pipeline,  │
 │  + on-device  │      │ sync, notifications    │      │ model registry,     │
 │  AI model)    │      └──────────┬─────────────┘      │ dataset curation    │
 └──────┬────────┘                 │                    └─────────────────────┘
        │ SMS / WhatsApp / USSD     │
        ▼                           ▼
 ┌───────────────┐      ┌────────────────────────┐      ┌─────────────────────┐
 │ Messaging     │      │ Irrigation engine      │◄─────│ External data:      │
 │ gateway       │      │ (FAO-56 water balance) │      │ weather, satellite, │
 └───────────────┘      └────────────────────────┘      │ soil data           │
                                                        └─────────────────────┘
 ┌──────────────────────────────┐
 │ Regional web dashboard       │
 └──────────────────────────────┘
```

### 5.1 Design Principles

- **Offline-first**: the core diagnosis must work with no connection.
- **Low-end device friendly**: runs on 2-3 GB RAM Android phones; app size kept small.
- **Low bandwidth**: compressed images, delta sync, queue uploads.
- **Voice and local language**: Darija and Amazigh are first-class, not translations bolted on.
- **Abstain when unsure**: uncertain cases return "not sure, retake the photo"; the system never presents guesses as facts.
- **Privacy by design**: user and plot data is minimized and never used for training.

---

## 6. Technical Requirements

### 6.1 AI: Plant Disease Diagnosis

**Task**: image classification (and optionally detection/segmentation) of diseases, pests and deficiencies for target crops.

**Model options**
- Start with transfer learning on a pretrained backbone: MobileNetV3, EfficientNet-Lite, or a small Vision Transformer (e.g. MobileViT).
- Export to **TensorFlow Lite** or **ONNX Runtime Mobile** with INT8 quantization for on-device inference (target: under 25 MB model, under 500 ms per image on a mid-range phone).
- A larger cloud model can re-check images when connected and when the on-device confidence is low.
- Add a **crop classifier** and an **out-of-distribution detector** (so photos of hands, soil or non-plants are rejected instead of misdiagnosed).

**Data**
- Public datasets: PlantVillage, PlantDoc, PlantNet-300K, iNaturalist, Cassava and other Kaggle/Zenodo agricultural datasets. Note that PlantVillage images are lab-style (plain background) and models trained only on it generalize poorly to real fields.
- **Public data only**: no farmer- or expert-supplied photos or labels. Close the domain gap with in-the-wild public sets (for example PlantDoc), strong augmentation (light, blur, background, compression), cross-dataset evaluation, out-of-distribution rejection and a published model card.
- Clean the public data: deduplicate (including augmented copies), map class names across datasets, and flag label noise automatically.
- Scope for MVP: the crops and conditions that public datasets cover well; record per-class sample counts, image style and license in `data/public_datasets/registry.csv`.

**Evaluation**
- Split by **source plant and dataset**, not by random image, to avoid leakage; hold out whole datasets (for example train on PlantVillage, test on PlantDoc).
- Metrics: per-class precision/recall, top-3 accuracy, calibration (confidence reliability), abstain rate, and robustness to blur, lighting and compression.

**MLOps**
- Versioned datasets (DVC or similar), experiment tracking (MLflow or Weights & Biases), model registry, retraining when new public datasets are added, over-the-air model updates, and monitoring of confidence drift across releases.

### 6.2 AI: Language (Darija and Amazigh)

This is the most distinctive and hardest part. Both are low-resource languages.

| Component | Approach |
|---|---|
| Advice content | Advice templates in French/Arabic written from cited public sources (FAO, EPPO, ONSSA lists, research publications), translated and adapted by native speakers. **Prefer curated templates over free-form generation** for safety. |
| Darija | Arabic script and Latin ("Arabizi") input support; use existing Darija resources (e.g. community datasets, DODa-style corpora) to improve understanding. |
| Amazigh | Three main varieties: Tashelhit (Souss, High/Anti-Atlas), Central Atlas Tamazight, Tarifit (Rif). Support **Tifinagh** (IRCAM standard) and Latin script. Start with one variety (e.g. Tashelhit), then add others. |
| Text-to-speech | Record professional voice talent in each language to build audio for the advice library (practical for MVP); evaluate neural TTS (fine-tuned VITS or similar) once enough recorded speech exists. |
| Speech-to-text | Optional in MVP; fine-tune a model such as Whisper on public speech corpora where the license allows, for Darija and Tashelhit questions. |
| Terminology | Build a glossary of crop, disease, pest and chemical terms seeded from public vocabularies such as FAO AGROVOC; agricultural vocabulary often differs by region. |
| LLM assistant (Phase 2) | Retrieval-augmented generation grounded in a vetted knowledge base, restricted to approved content, with citations and refusal when unsure. Never allow the LLM to invent chemical doses. |

### 6.3 Irrigation Engine

**Method**: soil water balance based on FAO-56.

1. Compute reference evapotranspiration (**ET0**) from weather: temperature, humidity, wind, solar radiation (Penman-Monteith; use Hargreaves as a fallback when data is limited).
2. Multiply by the crop coefficient (**Kc**) for the crop and growth stage to get crop water demand (ETc).
3. Track soil water: add rainfall and irrigation, subtract ETc and drainage.
4. Trigger irrigation advice when depletion reaches the allowable threshold for the crop and soil (field capacity, wilting point, root depth).
5. Convert the need to practical units: minutes of drip, number of furrow turns, liters per tree.

**Inputs**
- Weather forecast and history: Open-Meteo, NASA POWER, ERA5 reanalysis, national meteorological service (DGM) data where accessible.
- Soil: SoilGrids (texture, water-holding capacity).
- Satellite: Sentinel-2 NDVI/NDWI via Copernicus or Google Earth Engine for crop stress and growth stage.

**Roadmap for accuracy**: start rule-based (FAO-56), then evaluate optional ML correction layers using public reference data.

### 6.4 Mobile App

- **Platform**: Android first (dominant in the target market); iOS later.
- **Framework**: Flutter or React Native (single codebase); native modules for camera and TFLite.
- **Local storage**: SQLite/Room/Isar for plots, advice library, queued uploads.
- **Offline sync**: background sync, conflict handling, resumable image upload.
- **Accessibility**: audio-first flows, large touch targets, pictograms, high contrast for sunlight, right-to-left layout and Tifinagh font support.
- **Size/performance**: aim for an APK under 50 MB, run on Android 8+ with 2 GB RAM.
- **Notifications**: push (FCM) plus SMS/WhatsApp fallback for important alerts (frost, heat wave, irrigation).

### 6.5 Backend and Cloud

| Layer | Suggested choice |
|---|---|
| API | Python (FastAPI) or Node.js (NestJS), REST + optional GraphQL |
| Database | PostgreSQL with PostGIS (plots, geodata), Redis (cache/queues) |
| Object storage | S3-compatible (images, audio, models) |
| Task queue | Celery or similar for weather ingestion, daily irrigation calculation, notifications |
| Auth | Phone-number OTP login (many users do not use email) |
| ML serving | Cloud inference service (e.g. TorchServe/Triton/FastAPI) for the heavy model and re-checks |
| Messaging | WhatsApp Business API, SMS gateway (Moroccan operators), USSD later |
| Hosting | Cloud region close to users (EU/Africa), containerized (Docker + Kubernetes or managed services); consider Moroccan data hosting options for compliance |
| Observability | Logging, metrics, error tracking (Sentry, Prometheus/Grafana) |
| CI/CD | GitHub Actions or GitLab CI; automated tests and model validation gates |

### 6.6 Regional Web Dashboard

- React/Next.js (or similar) with a maps library (Leaflet/MapLibre).
- Data comes from public weather and soil sources and the irrigation engine.
- Billing and subscription management (local payment methods plus invoicing; bank transfer is common for cooperatives).

### 6.7 Security, Privacy and Compliance

- Compliance with Moroccan **Law 09-08** on personal data protection (CNDP declaration/authorization); align with GDPR if serving EU-linked exporters.
- User photos are never used for model training; allow deletion of user data.
- Plot locations are sensitive: encrypt at rest and in transit.
- Pesticide advice must respect **ONSSA-approved product lists** and label directions; include safety warnings (protective equipment, pre-harvest intervals, bee protection).
- Terms of service clarifying that the app provides decision support, not a guarantee.

### 6.8 Hardware / Infrastructure Budget Items

- GPU compute for training (cloud GPUs; a single modern GPU is enough for MVP).
- Test phones: 8-10 low/mid-range Android devices.

---

## 7. Business Model

### 7.1 Revenue Streams

1. **Cooperative subscription (core)**
   - Per-member per-month or per-hectare per-season pricing, billed to the cooperative.
   - Tiers: *Basic* (diagnosis + advice), *Plus* (irrigation + alerts + dashboard), *Premium* (satellite, reports, traceability).
2. **Input supplier commissions**
   - Referral fees when a farmer buys a recommended, approved product through the app or a partner dealer.
   - **Safeguard**: recommendation logic must remain independent. Show non-chemical options first, rank by agronomic fit (not by commission), and label sponsored links clearly. Losing farmer trust would end the business.
3. **Data and reports (carefully)**
   - Reports built from public weather and water-need data for ministries, researchers, insurers and agro-industry.
4. **Grants and programs**
   - Climate adaptation, water-efficiency and digital agriculture grants.
5. **Future**: exporter/traceability modules.

### 7.2 Unit Economics to Estimate

- Cost per active user per month (cloud, SMS), estimated from load tests.
- Cooperative sales cycle length (often long; plan for grant funding).
- Public benchmark results (model card, irrigation backtests) are the evidence for the product's quality.

### 7.3 Go-to-Market

- Start in one region and 2-3 crops chosen from public dataset coverage (e.g. Souss-Massa for citrus/vegetables and Tashelhit; Atlas/Haouz for olives and almonds; Saiss or Gharb for cereals and vegetables).

---

## 8. Step-by-Step Plan

### Phase 0: Scope and Public Data (Months 0-2)

1. Compile the public dataset registry: PlantVillage, PlantDoc, PlantNet-300K, iNaturalist and others, with license, crops, classes and image style.
2. Choose **one region, 2-3 crops, 1 Amazigh variety** and define the priority disease list from public dataset coverage.
3. Write the evaluation protocol: public train and held-out sets, cross-dataset tests, leakage rules.
4. Prototype the irrigation engine in a notebook and check it against FAO-56 worked examples.

### Phase 1: Data and Knowledge Foundation (Months 2-6)

5. Build the **knowledge base**: disease sheets, treatment guidance, approved product list, irrigation parameters (Kc, root depth, thresholds) for each crop, every entry citing a public source.
6. Build the **public dataset pipeline**: ingestion, taxonomy mapping, deduplication, label-noise flagging, robustness test sets.
7. Assemble the **glossary and translations**; hire native-speaker translators and voice talent; record the first audio library.
8. Set up the cloud foundation, repositories, CI/CD and data versioning.

### Phase 2: MVP Build (Months 4-9)

9. Train the first diagnosis models with transfer learning; evaluate on the held-out public test set; iterate on weak classes.
10. Build the **irrigation engine** (FAO-56) and test it against FAO-56 worked examples and published reference data.
11. Build the **mobile app**: onboarding with phone OTP, plot creation, camera diagnosis, advice screens with audio, irrigation card, notifications, offline mode.
12. Build the backend API and a minimal regional dashboard.
13. Internal testing, accessibility checks, performance tests on low-end phones.

### Phase 3: Public-Data Evaluation and Hardening (Months 9-14)

14. Publish a model card and benchmark report: datasets, licenses, domain gap, per-class results, limits.
15. Run robustness and calibration evaluation on perturbed public sets.
16. Backtest and run sensitivity analysis on the irrigation engine with public reference data.
17. Fix UX and device issues; refine language and audio.

### Phase 4: Launch and Scale (Months 14-24)

18. Publish the benchmark results; finalize pricing and contracts.
19. Roll out to more regions; add crops (from newly added public data) and the other Amazigh varieties.
20. Add WhatsApp/SMS/USSD channels, supplier marketplace and satellite NDVI.
21. Raise funding or secure grants; build a small team for support and partnerships.
22. Plan expansion to Algeria, Tunisia and other markets with dialect adaptation.

---

## 9. Team and Roles

| Role | Responsibility |
|---|---|
| Product lead / founder | Vision, partnerships, fundraising |
| ML engineer (x1-2) | Vision models, on-device optimization, MLOps |
| NLP/speech engineer (part-time or contract) | Darija/Amazigh text and speech pipeline |
| Mobile developer (x1-2) | Android/Flutter app |
| Backend/data engineer (x1) | APIs, irrigation engine, data pipelines |
| UX designer | Voice-first, icon-first UI |
| Native-speaker linguists and voice talent | Translation, terminology, audio recording |
| Business development | Cooperative and supplier relationships |

---

## 10. Indicative Budget (Rough Order of Magnitude)

Costs vary widely; validate with real quotes.

| Item | Estimate (first 12-18 months) |
|---|---|
| Team (core 5-8 people, partly part-time) | Largest share of budget |
| Public dataset storage and curation | Low |
| Cloud and GPU compute | Low to moderate for MVP |
| Voice recording and translation | Low to moderate |
| Test devices | Low |
| Legal, data protection, insurance | Low |

Funding sources to explore: ADA, Innov Invest / Moroccan innovation programs, development agencies, climate and water grants, agritech accelerators, university partnerships.

---

## 11. Key Performance Indicators

**Product**
- Diagnosis top-1 and top-3 accuracy on held-out public test sets (including in-the-wild data); calibration error; share of "not sure" results.
- Time from photo to advice; offline success rate on test devices.

**Adoption**
- Monthly active users and retention.

**Technical quality (the evidence that sells the product)**
- Robustness: accuracy drop on perturbed public test sets.
- Irrigation engine agreement with FAO-56 worked examples and cross-checked ET0 across weather sources.

**Business**
- Number of paying cooperatives, revenue per member, churn, cost per active user, commission revenue share.

---

## 12. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Models fail on real field photos (domain gap from public data) | In-the-wild public sets, augmentation, cross-dataset evaluation, out-of-distribution detection, "not sure, retake the photo" flow, published model card |
| Wrong advice harms crops or health | Curated, source-cited advice; public approved-product list only; no generated doses; clear safety warnings; liability terms; automated validation blocks unsourced entries |
| Low-resource language quality | Native-speaker review; start with one Amazigh variety; recorded audio before synthetic TTS |
| Poor connectivity | Offline-first design; SMS/WhatsApp fallback |
| Low digital literacy | Voice/icon UI, accessibility guidelines |
| Slow cooperative sales | Grant funding; publish public benchmark results |
| Conflict of interest with input suppliers | Independent recommendation logic; transparent sponsored labeling |
| Irrigation inaccuracy | Validate against FAO-56 worked examples; cross-check weather sources; conservative recommendations at first |
| Data privacy issues | Minimization, no training on user data, deletion, CNDP compliance |
| Dependence on external data APIs | Cache data, use multiple weather sources, fallback methods |
| Seasonality (data and revenue) | Multi-crop portfolio; multi-region; subscription per season |

---

## 13. Ethics and Social Impact

- **Inclusion**: support Amazigh and Darija speakers and low-literacy users on equal footing.
- **User data**: minimized, never used to train models, deletable on request.
- **Sustainable practices**: prioritize integrated pest management and reduce overuse of pesticides and water.
- **Transparency**: show confidence levels and limitations honestly.
- **Dataset bias**: document gaps in crop, region and image-source coverage of the public datasets.

---

## 14. Tech Stack Summary

| Area | Suggested tools |
|---|---|
| Mobile | Flutter or React Native, TensorFlow Lite / ONNX Runtime Mobile, SQLite |
| ML | PyTorch or TensorFlow, timm, Albumentations, MLflow, DVC |
| Speech/NLP | Whisper fine-tuning, VITS or similar TTS, recorded audio library |
| Backend | FastAPI or NestJS, PostgreSQL + PostGIS, Redis, Celery, Docker |
| Geo / climate data | Open-Meteo, NASA POWER, ERA5, SoilGrids, Sentinel-2 / Google Earth Engine |
| Messaging | WhatsApp Business API, SMS gateway, FCM |
| Web dashboard | React/Next.js, MapLibre/Leaflet |
| DevOps | GitHub Actions, Terraform, Kubernetes or managed services, Sentry, Grafana |

---

## 15. Immediate Next Actions (First 30 Days)

1. Choose region, crops, and Amazigh variety from public dataset coverage.
2. Build the public dataset registry and ingestion pipeline.
3. Draft the priority disease list and the irrigation parameter table from public sources, with citations.
4. Write the evaluation protocol (public train and held-out sets, cross-dataset tests).
5. Prototype the irrigation engine in a notebook using Open-Meteo data for one crop.
6. Prepare a 10-slide pitch and a grant application (ADA, innovation programs, climate/water funds).

---

*This document is a planning blueprint. Statistics, costs, regulations and program names should be verified with current official sources before use in funding applications or contracts.*
