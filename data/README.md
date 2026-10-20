# Data

Raw and processed data are **not** committed to git. Use DVC (set up in step A1.1). Only READMEs and `.gitkeep` files are tracked.

Rules:
- Split train/val/test by farm/field and date, never by random image.
- The field test set is frozen and never used for training.
- Every photo must have a consent flag (Law 09-08).
