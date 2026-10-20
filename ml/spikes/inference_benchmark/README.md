# Inference spike (step A0.3): web vs native

**Question:** can on-device diagnosis run in the web layer, or do we need the native TFLite plugin?
**Owner: @rihabetm.** Reviewer: @itsya-ssine.

## Setup
- Same quantized model (INT8) for all runs, same 50 test images.
- 3-4 phones: Android 8+, 2-3 GB RAM (at least one low-end, one mid-range).
- Three paths:
  1. ONNX Runtime Web (WASM, SIMD)
  2. TensorFlow.js
  3. Native TFLite through a minimal Capacitor plugin

## Measure (per phone and path)
- Latency: cold start, then median and p95 over 50 images
- Peak memory
- Battery drain over 100 inferences
- Crashes or out-of-memory events
- App startup time

## Decision rule
- Web acceptable if under about 1.5 s per image with no memory problems on a 2 GB phone.
- Otherwise use native TFLite (target under 500 ms).
- If the WebView itself is unreliable on target phones, escalate the Flutter question before building more.

## Output
Fill in `results.csv` and write the decision in `docs/decisions/0002-inference-path.md`.
