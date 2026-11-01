# Evaluation protocol (step A0.1)

Replaces the field photo collection protocol. All data is public (see `data/public_datasets/registry.csv`).

Cover:
- Which public datasets are used for pretraining, fine-tuning and held-out testing.
- Cross-dataset tests: train on lab-style data (for example PlantVillage), test on in-the-wild data (for example PlantDoc), and report the gap.
- Leakage rules: deduplicate first, including augmented copies; keep images of the same source plant together where metadata allows; never split by random image.
- Robustness tests: blur, lighting, background and JPEG compression applied to the held-out set to mimic phone cameras.
- Out-of-distribution tests: non-crop plants, hands, soil, blurry photos.
- Metrics: per-class precision and recall, top-1 and top-3, calibration, abstain rate.
- Model card: known domain gap and limits, published with each model release.
