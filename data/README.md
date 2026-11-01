# Data

Raw and processed data are **not** committed to git. Use DVC (set up in step A1.1). Only READMEs, registries and `.gitkeep` files are tracked.

Rules:
- Public datasets only. Every dataset is listed in `public_datasets/registry.csv` with its source and license before it is used.
- No farmer-supplied or user-uploaded photos are used for training or evaluation.
- Never split train/val/test by random image. Deduplicate first, keep images of the same source plant together where metadata allows, and prefer holding out whole datasets (see `docs/evaluation-protocol.md`).
- The held-out public test set is frozen and never used for training.
