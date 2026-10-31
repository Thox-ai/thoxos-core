# Handoff — thoxos-core

Status: PUBLIC v0.1.0 released 2026-10-31 (programme decision D10).
Repository: https://github.com/Thox-ai/thoxos-core — release:
https://github.com/Thox-ai/thoxos-core/releases/tag/v0.1.0

Done:
- Entitlement reference implementation + 25/25 tests (D4 contract).
- Image definitions (E2/P4/P6/QEMU) + validator 27/27.
- RAUC A/B OTA template.
- Full documentation set: user guide, quickstart, install guides
  (bare metal, dual-boot Intel Mac, Apple silicon VM, device classes),
  RUN.md, KERNEL.md, whitepaper v0.1.0 (MD/HTML/PDF/DOCX), UX
  walkthrough captures with REAL/SIMULATION labels.

In progress: nothing in this repo. Programme-level next steps below.

Next:
- linux-thox first import (patch series + defconfigs).
- thoxd (Rust daemon), device portal, MeshStack Local, SDK.
- Built device images per class; Gate G1 physical qualification.

Key files: entitlement/thox_entitlement.py (contract implementation),
images/validate.py (definition validator), docs/PENDING-VERIFY.md
(open-claims register — read before making any new public claim).

Conventions: DCO sign-off on every commit; AI contributions disclosed
in PR descriptions; tests above must stay green.

Blockers: built images wait on the linux-thox import and a Buildroot
tree on a fleet build host.

Last verified: 2026-10-31, publish pass (bundle sha256sum -c passed;
suites re-run from the packaged tree during packaging).
