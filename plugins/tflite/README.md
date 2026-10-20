# @fellah/capacitor-tflite

Native Capacitor plugin (Kotlin) for on-device inference. **Owner: @rihabetm.**

Planned API (see `docs/model-contract.md`):

```ts
classify(options: { imagePath: string }): Promise<{
  top3: { classId: string; confidence: number }[];
  oodScore: number;
  modelVersion: string;
  latencyMs: number;
}>;
```

Models are loaded from app storage so they can be updated without a Play Store release.
Starts as a minimal prototype for the inference spike (step A0.3).
