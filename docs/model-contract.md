# Model I/O contract (draft)

Owner: @rihabetm. Reviewer: @itsya-ssine.

| Item | Value |
|---|---|
| Input | RGB image, 224x224, float32 or uint8 (INT8 model) |
| Normalization | To be set after the backbone is chosen (A0.2) |
| Output | Class probabilities, ordered by `classes.json` |
| Top-k returned to app | 3 |
| Confidence | Calibrated (temperature scaling) |
| OOD score | Float in [0, 1]; above the threshold means "not a plant / not sure" |
| Model metadata | `modelVersion`, `classesVersion`, `sha256`, `minAppVersion` |
| Size target | Under 25 MB |
| Latency target | Under 500 ms on a mid-range phone (native path) |

Plugin result shape: see `plugins/tflite/README.md`.
