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
4. **Belong to a cooperative**: the cooperative sees aggregated disease alerts and water use across its members and pays for the service.

---

## 2. Problem Statement

| Issue | Detail |
|---|---|
| Crop losses | Diseases, pests and weeds cause significant yield losses every season (commonly cited global figures are 20-40%; local figures should be validated with partner institutes). |
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

**Ecosystem partners**
- Public: Ministry of Agriculture programs (e.g. Generation Green 2020-2030), ONCA (national agricultural advisory office), ORMVAs (regional irrigation offices), ONSSA (food/pesticide safety), INRA Maroc.
- Academic/research: UM6P, IAV Hassan II, ENA Meknes, ICARDA.
- Funders: ADA (Agence pour le Developpement Agricole), international development agencies, impact investors.

---

## 4. Core Features

### 4.1 MVP (must have)

1. **Photo diagnosis**
   - Camera capture with guidance ("get closer", "show the underside of the leaf", "avoid shadows").
   - Crop selection (or auto-detection), then disease/pest/nutrient-deficiency prediction with top-3 results and confidence.
   - "Not sure" fallback that routes to a human expert instead of guessing.
2. **Treatment advice**
   - Structured advice: what it is, how it spreads, what to do now, how to prevent it.
   - Ordered by priority: cultural practices, biological controls, then approved chemical options (only products registered in Morocco, with dose, pre-harvest interval and safety).
   - Delivered in Darija (Arabic script) and Amazigh (Tifinagh and Latin), as text **and audio**.
3. **Irrigation advisor**
   - Farmer creates a plot (location pin, crop, planting date, soil type, irrigation method: drip, furrow, sprinkler, flood).
   - Daily recommendation: *irrigate today / wait / how many minutes or liters*.
   - 7-day outlook and alerts for heat waves, frost, and rain.
4. **Offline-first behavior**
   - On-device model for diagnosis; cached advice; sync when connected.
5. **Voice-first, icon-first UI**
   - Large buttons, audio prompts, minimal text.

### 4.2 Phase 2

- Plot history and crop diary (treatments, irrigation, costs, yield).
- Satellite vegetation index (NDVI) per plot to spot stress early.
- Community Q&A and expert escalation (agronomist reviews uncertain cases).
- Cooperative dashboard (see 4.3).
- WhatsApp bot and SMS/USSD fallback for feature phones and weak data.
- Marketplace links to certified input suppliers (commission source).

### 4.3 Cooperative Dashboard (web)

- Map of members' plots with anonymized disease reports and heatmaps.
- Early outbreak alerts (e.g. 10 reports of the same disease within 10 km in a week).
- Water usage and savings reports.
- Member onboarding, subscription and invoicing.
- Exportable reports for donors, ORMVAs and certification (GlobalG.A.P., organic).

### 4.4 Phase 3

- Low-cost IoT soil moisture sensors (LoRaWAN or cellular) for plots whose owners want precision.
- Yield prediction and harvest planning.
- Insurance and credit scoring partnerships (with farmer consent).
- Expansion to Algeria, Tunisia, Mauritania, Egypt and other dialects.

---

## 5. Solution Architecture

```
 ┌───────────────┐      ┌────────────────────────┐      ┌─────────────────────┐
 │ Mobile app    │◄────►│ Backend API (cloud)    │◄────►│ Data & ML platform  │
 │ (Android first│      │ Auth, plots, advice,   │      │ Training pipeline,  │
 │  + on-device  │      │ sync, notifications    │      │ model registry,     │
 │  AI model)    │      └──────────┬─────────────┘      │ data labeling       │
 └──────┬────────┘                 │                    └─────────────────────┘
        │ SMS / WhatsApp / USSD     │
        ▼                           ▼
 ┌───────────────┐      ┌────────────────────────┐      ┌─────────────────────┐
 │ Messaging     │      │ Irrigation engine      │◄─────│ External data:      │
 │ gateway       │      │ (FAO-56 water balance) │      │ weather, satellite, │
 └───────────────┘      └────────────────────────┘      │ soil, sensors       │
                                                        └─────────────────────┘
 ┌──────────────────────────────┐
 │ Cooperative web dashboard    │
 └──────────────────────────────┘
```

### 5.1 Design Principles

- **Offline-first**: the core diagnosis must work with no connection.
- **Low-end device friendly**: runs on 2-3 GB RAM Android phones; app size kept small.
- **Low bandwidth**: compressed images, delta sync, queue uploads.
- **Voice and local language**: Darija and Amazigh are first-class, not translations bolted on.
- **Human in the loop**: uncertain cases go to experts; the system never presents guesses as facts.
- **Privacy by design**: farmer and plot data belongs to the farmer.

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
- Public datasets for bootstrapping: PlantVillage, PlantDoc, PlantNet-300K, iNaturalist, Cassava and other Kaggle/Zenodo agricultural datasets. Note that PlantVillage images are lab-style (plain background) and models trained only on it generalize poorly to real fields.
- **Local field data is essential**: collect thousands of real photos per priority disease, per crop, in real conditions (different light, backgrounds, growth stages, phone cameras).
- Labeling by plant pathologists (INRA, universities, ONSSA labs); use a double-labeling process and a review of disagreements.
- Data targets for MVP: 5-8 crops, 5-10 conditions per crop, 500-1,000+ field images per class (more for similar-looking diseases).

**Evaluation**
- Split by **farm/field and date**, not by random image, to avoid leakage.
- Metrics: per-class precision/recall, top-3 accuracy, calibration (confidence reliability), and performance on low-end phone photos.
- Field trials with real farmers before launch; compare against an agronomist's diagnosis.

**MLOps**
- Versioned datasets (DVC or similar), experiment tracking (MLflow or Weights & Biases), model registry, automated retraining when enough new labeled data arrives, over-the-air model updates, and monitoring of confidence drift.

### 6.2 AI: Language (Darija and Amazigh)

This is the most distinctive and hardest part. Both are low-resource languages.

| Component | Approach |
|---|---|
| Advice content | Expert-written advice templates in French/Arabic, translated and adapted by native speakers and agronomists. **Prefer curated templates over free-form generation** for safety. |
| Darija | Arabic script and Latin ("Arabizi") input support; use existing Darija resources (e.g. community datasets, DODa-style corpora) to improve understanding. |
| Amazigh | Three main varieties: Tashelhit (Souss, High/Anti-Atlas), Central Atlas Tamazight, Tarifit (Rif). Support **Tifinagh** (IRCAM standard) and Latin script. Start with one variety (e.g. Tashelhit), then add others. |
| Text-to-speech | Record professional voice talent in each language to build audio for the advice library (practical for MVP); evaluate neural TTS (fine-tuned VITS or similar) once enough recorded speech exists. |
| Speech-to-text | Optional in MVP; collect voice data (consent-based, paid contributors) to fine-tune a model such as Whisper for Darija and Tashelhit questions. |
| Terminology | Build a glossary of crop, disease, pest and chemical terms with farmers and agronomists; agricultural vocabulary often differs by region. |
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
- Soil: SoilGrids (texture, water-holding capacity), refined by the farmer's simple input ("sandy / clay / loam") or a 1-question "squeeze test".
- Satellite: Sentinel-2 NDVI/NDWI via Copernicus or Google Earth Engine for crop stress and growth stage.
- Optional: soil moisture sensors for calibration.
- Farmer feedback: "I irrigated" button, "soil felt dry/wet" check, to correct the model.

**Roadmap for accuracy**: start rule-based (FAO-56), then add ML correction layers using sensor and farmer feedback data.

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
| Auth | Phone-number OTP login (farmers often do not use email); role-based access for cooperatives and experts |
| ML serving | Cloud inference service (e.g. TorchServe/Triton/FastAPI) for the heavy model and re-checks |
| Messaging | WhatsApp Business API, SMS gateway (Moroccan operators), USSD later |
| Hosting | Cloud region close to users (EU/Africa), containerized (Docker + Kubernetes or managed services); consider Moroccan data hosting options for compliance |
| Observability | Logging, metrics, error tracking (Sentry, Prometheus/Grafana) |
| CI/CD | GitHub Actions or GitLab CI; automated tests and model validation gates |

### 6.6 Cooperative Web Dashboard

- React/Next.js (or similar) with a maps library (Leaflet/MapLibre).
- Multi-tenant design (each cooperative isolated), role-based access.
- Billing and subscription management (local payment methods plus invoicing; bank transfer is common for cooperatives).

### 6.7 Security, Privacy and Compliance

- Compliance with Moroccan **Law 09-08** on personal data protection (CNDP declaration/authorization); align with GDPR if serving EU-linked exporters.
- Explicit consent for photo use in model training; allow opt-out and deletion.
- Plot locations are sensitive: encrypt at rest and in transit; share only aggregated data with cooperatives unless the farmer consents.
- Pesticide advice must respect **ONSSA-approved product lists** and label directions; include safety warnings (protective equipment, pre-harvest intervals, bee protection).
- Terms of service clarifying that the app provides decision support, not a guarantee.

### 6.8 Hardware / Infrastructure Budget Items

- GPU compute for training (cloud GPUs; a single modern GPU is enough for MVP).
- Test phones: 8-10 low/mid-range Android devices.
- Field data collection kits (phones, tripods/colour reference cards, GPS).
- Optional: soil sensors for pilot plots (a few dozen to a few hundred units).

---

## 7. Business Model

### 7.1 Revenue Streams

1. **Cooperative subscription (core)**
   - Per-member per-month or per-hectare per-season pricing, billed to the cooperative.
   - Tiers: *Basic* (diagnosis + advice), *Plus* (irrigation + alerts + dashboard), *Premium* (sensors, satellite, reports, traceability).
2. **Input supplier commissions**
   - Referral fees when a farmer buys a recommended, approved product through the app or a partner dealer.
   - **Safeguard**: recommendation logic must remain independent. Show non-chemical options first, rank by agronomic fit (not by commission), and label sponsored links clearly. Losing farmer trust would end the business.
3. **Data and reports (carefully)**
   - Aggregated, anonymized disease and water-use insights for ministries, researchers, insurers and agro-industry.
4. **Grants and programs**
   - Climate adaptation, water-efficiency and digital agriculture grants and pilot contracts.
5. **Future**: exporter/traceability modules, insurance referrals.

### 7.2 Unit Economics to Validate in Pilots

- Willingness to pay per member (start by testing several price points).
- Cost per active farmer per month (cloud, SMS, support).
- Cooperative sales cycle length (often long; plan for pilots funded by grants).
- Measured benefit: yield protected, pesticide spend saved, water/energy saved. **This evidence is your sales argument.**

### 7.3 Go-to-Market

- Start in one region and 2-3 crops with a strong cooperative or ORMVA partner (e.g. Souss-Massa for citrus/vegetables and Tashelhit; Atlas/Haouz for olives and almonds; Saiss or Gharb for cereals and vegetables).
- Train a few "lead farmers" or cooperative technicians as local champions.
- Use WhatsApp groups and radio/local events to spread adoption.

---

## 8. Step-by-Step Plan

### Phase 0: Discovery and Validation (Months 0-2)

1. Interview 40-60 farmers and 10-15 cooperatives: top 3 crops, top diseases, how they decide when to irrigate, phone usage, language and literacy, willingness to pay.
2. Meet agronomists, ONCA advisors, INRA/university researchers, and ORMVA staff to identify partners and data sources.
3. Choose **one region, 2-3 crops, 1 Amazigh variety** and define the priority disease list with experts.
4. Run a **Wizard-of-Oz test**: farmers send photos via WhatsApp; experts reply in Darija/Tashelhit. This validates demand and generates the first labeled data.
5. Write the pilot agreement and data-sharing agreement with a cooperative.

### Phase 1: Data and Knowledge Foundation (Months 2-6)

6. Build the **knowledge base**: disease sheets, treatment guidance, approved product list, irrigation parameters (Kc, root depth, thresholds) for each crop, all validated by agronomists.
7. Launch **field data collection**: a simple collection app, photo protocol, annotation guide; pay local collectors and agronomist labelers.
8. Assemble the **glossary and translations**; hire native-speaker translators and voice talent; record the first audio library.
9. Set up the cloud foundation, repositories, CI/CD, data versioning, and annotation tooling.

### Phase 2: MVP Build (Months 4-9)

10. Train the first diagnosis models with transfer learning; evaluate on a held-out field dataset; iterate on weak classes.
11. Build the **irrigation engine** (FAO-56) and test it against known irrigation schedules and reference data for the pilot crops.
12. Build the **mobile app**: onboarding with phone OTP, plot creation, camera diagnosis, advice screens with audio, irrigation card, notifications, offline mode.
13. Build the backend API and a minimal cooperative dashboard.
14. Internal testing, usability tests with low-literacy farmers, performance tests on low-end phones.

### Phase 3: Pilot (Months 9-14)

15. Deploy with **100-300 farmers** in 1-3 cooperatives for one full crop season.
16. Provide in-person training and a support line (WhatsApp).
17. Collect usage analytics, diagnosis feedback ("was this correct?"), and farmer outcomes.
18. Compare pilot vs. control farmers: disease losses, pesticide spend, water and energy use, yield.
19. Improve models with new field data; fix UX issues; refine language and audio.

### Phase 4: Launch and Scale (Months 14-24)

20. Publish results (case study with partner institutes); finalize pricing and contracts.
21. Roll out to more cooperatives and regions; add crops and the other Amazigh varieties.
22. Add WhatsApp/SMS/USSD channels, supplier marketplace, satellite NDVI, expert escalation.
23. Raise funding or secure grants; build a small team for support, partnerships and agronomy.
24. Plan expansion to Algeria, Tunisia and other markets with dialect adaptation.

---

## 9. Team and Roles

| Role | Responsibility |
|---|---|
| Product lead / founder | Vision, partnerships, pilots, fundraising |
| Agronomist / plant pathologist (x1-2) | Disease list, labeling, advice validation, field trials |
| ML engineer (x1-2) | Vision models, on-device optimization, MLOps |
| NLP/speech engineer (part-time or contract) | Darija/Amazigh text and speech pipeline |
| Mobile developer (x1-2) | Android/Flutter app |
| Backend/data engineer (x1) | APIs, irrigation engine, data pipelines |
| UX designer with rural user-research experience | Voice-first, icon-first UI |
| Native-speaker linguists and voice talent | Translation, terminology, audio recording |
| Field coordinators | Farmer onboarding, data collection, training, support |
| Business development | Cooperative and supplier relationships |

---

## 10. Indicative Budget (Rough Order of Magnitude)

Costs vary widely; validate with real quotes.

| Item | Estimate (first 12-18 months) |
|---|---|
| Team (core 5-8 people, partly part-time) | Largest share of budget |
| Field data collection and labeling | Moderate to high (labeled data is the main asset) |
| Cloud and GPU compute | Low to moderate for MVP |
| Voice recording and translation | Low to moderate |
| Pilot logistics, training, devices | Moderate |
| Legal, data protection, insurance | Low |
| Optional soil sensors for pilot | Low to moderate |

Funding sources to explore: ADA, Innov Invest / Moroccan innovation programs, development agencies, climate and water grants, agritech accelerators, university partnerships.

---

## 11. Key Performance Indicators

**Product**
- Diagnosis top-1 and top-3 accuracy on real field photos; share of "uncertain" cases.
- Time from photo to advice; offline success rate.

**Adoption**
- Monthly active farmers, retention across the season, advice follow-through rate.

**Impact (the evidence that sells the product)**
- Reduction in crop loss compared with control farmers.
- Reduction in pesticide spend and misapplication.
- Water and energy saved per hectare.
- Income gain per farmer.

**Business**
- Number of paying cooperatives, revenue per member, churn, cost per active farmer, commission revenue share.

---

## 12. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Models fail on real field photos | Collect local field data early; use out-of-distribution detection; "uncertain, ask expert" flow |
| Wrong advice harms crops or health | Curated, expert-validated advice; approved-product list only; clear safety warnings; liability terms; expert escalation |
| Low-resource language quality | Native-speaker review; start with one Amazigh variety; recorded audio before synthetic TTS |
| Poor connectivity | Offline-first design; SMS/WhatsApp fallback |
| Low digital literacy | Voice/icon UI, in-person onboarding, local champions |
| Slow cooperative sales | Grant-funded pilots; prove ROI; partner with ORMVAs and programs |
| Conflict of interest with input suppliers | Independent recommendation logic; transparent sponsored labeling |
| Irrigation inaccuracy | Calibrate with local data and sensors; farmer feedback loop; conservative recommendations at first |
| Data privacy issues | Consent, minimization, aggregation, CNDP compliance |
| Dependence on external data APIs | Cache data, use multiple weather sources, fallback methods |
| Seasonality (data and revenue) | Multi-crop portfolio; multi-region; subscription per season |

---

## 13. Ethics and Social Impact

- **Inclusion**: support Amazigh and Darija speakers and low-literacy users on equal footing.
- **Farmer data ownership**: farmers control their data and benefit when it is used.
- **Sustainable practices**: prioritize integrated pest management and reduce overuse of pesticides and water.
- **Transparency**: show confidence levels and limitations honestly.
- **Gender**: include women farmers and cooperatives (e.g. argan and saffron cooperatives) in design and pilots.

---

## 14. Tech Stack Summary

| Area | Suggested tools |
|---|---|
| Mobile | Flutter or React Native, TensorFlow Lite / ONNX Runtime Mobile, SQLite |
| ML | PyTorch or TensorFlow, timm, Albumentations, MLflow, DVC, Label Studio |
| Speech/NLP | Whisper fine-tuning, VITS or similar TTS, recorded audio library |
| Backend | FastAPI or NestJS, PostgreSQL + PostGIS, Redis, Celery, Docker |
| Geo / climate data | Open-Meteo, NASA POWER, ERA5, SoilGrids, Sentinel-2 / Google Earth Engine |
| Messaging | WhatsApp Business API, SMS gateway, FCM |
| Web dashboard | React/Next.js, MapLibre/Leaflet |
| DevOps | GitHub Actions, Terraform, Kubernetes or managed services, Sentry, Grafana |

---

## 15. Immediate Next Actions (First 30 Days)

1. Choose pilot region, crops, and Amazigh variety.
2. Sign up 1-2 cooperatives and 1 research partner (INRA/university) for a pilot letter of intent.
3. Start the WhatsApp Wizard-of-Oz service with 20-30 farmers.
4. Draft the priority disease list and the irrigation parameter table with an agronomist.
5. Define the photo-collection protocol and start collecting images.
6. Prototype the irrigation engine in a notebook using Open-Meteo data for one crop.
7. Prepare a 10-slide pitch and a grant application (ADA, innovation programs, climate/water funds).

---

*This document is a planning blueprint. Statistics, costs, regulations and program names should be verified with current official sources and local partners before use in funding applications or contracts.*
