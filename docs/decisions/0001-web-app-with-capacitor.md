# ADR 0001: Build a React PWA and package it with Capacitor

- **Status:** Accepted
- **Context:** Two engineers need one codebase shared by the farmer app and the cooperative dashboard.
- **Decision:** React + TypeScript PWA, packaged for Android with Capacitor. Native plugins only where needed (on-device inference).
- **Consequences:** Shared UI and API client with the dashboard; iOS is nearly free later. Risks: older WebViews, weaker background sync, web inference speed. The Phase 0 spike (A0.3) decides the inference path.
