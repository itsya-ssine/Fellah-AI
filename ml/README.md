# ML

Diagnosis models, evaluation, export. **Owner: @rihabetm.**

```
ml/
  spikes/inference_benchmark/   Phase 0 go/no-go: web vs native inference
  configs/                      Training and evaluation configs
  src/                          Training, evaluation, quality checks, export
```

Rules: public datasets only, versioned with DVC; experiments tracked with MLflow; the held-out public test set frozen; splits deduplicated and never random by image (see `docs/evaluation-protocol.md`).
