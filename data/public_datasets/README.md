# Public datasets (step B0.1)

Single place where public data is registered, downloaded and normalized. **Owner: @itsya-ssine.**

Register every dataset in `registry.csv` before use. Verify the license on the dataset's own page; do not copy a license from memory.

Target record after normalization:
`image_path, crop, label, source_dataset, license, split`

Planned work:
- Download scripts with checksums (files go to DVC, never git).
- Taxonomy map that unifies class names across datasets.
- Duplicate detection, including augmented copies of the same source image.

Never commit dataset files.
