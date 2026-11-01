# ADR 0003: Use public datasets only

- **Status:** Accepted
- **Context:** The original plan relied on farmers and experts: interviews, a WhatsApp Wizard-of-Oz test, field photo collection, expert labeling, agronomist sign-off on advice, expert escalation of uncertain cases, and a farmer pilot with feedback loops.
- **Decision:** Remove every dependency on farmer- or expert-supplied data, labels, validation or feedback. Models are trained and evaluated on public datasets. Advice and irrigation parameters come from published public sources. Uncertain diagnoses return "not sure, retake the photo" instead of going to a human.
- **Consequences:**
  - Domain gap: public images (especially lab-style ones) differ from real phone photos. Mitigate with in-the-wild public sets, augmentation, cross-dataset evaluation, OOD rejection and a published model card.
  - No Morocco-specific ground truth. Coverage is limited to crops and diseases present in public data.
  - No human review of advice. Mitigate with mandatory source citations, chemical data copied only from the public ONSSA list, and no generated doses.
  - No pilot, so no measured field impact. Quality is reported on public benchmarks and on-device tests only.
