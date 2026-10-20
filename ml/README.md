# ML

Diagnosis models, evaluation, export. **Owner: @rihabetm.**

```
ml/
  spikes/inference_benchmark/   Phase 0 go/no-go: web vs native inference
  configs/                      Training and evaluation configs
  src/                          Training, evaluation, quality checks, export
```

Rules: datasets versioned with DVC, experiments tracked with MLflow, the field test set frozen and split by farm/field and date.
