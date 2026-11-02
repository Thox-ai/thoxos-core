# thoxos-core

[![License](https://img.shields.io/badge/license-Apache--2.0-blue?style=flat-square)](LICENSE)
[![THOX.ai](https://img.shields.io/badge/THOX.ai-portfolio-05A451?style=flat-square)](https://thox.ai)

ThoxOS Core: the free, open-source operating system for THOX devices. thoxd system services, device portal, first-boot, local AI runtime glue, MeshStack Local, and Buildroot image definitions per compute class, with A/B OTA and rollback.

**Status:** Public release v0.1.0 (2026-10-31) under the ThoxOS open-source
programme (open/paid line approved 2026-10-29; public release directed by the
founders 2026-10-31). This release contains the tested entitlement reference
implementation, the per-class image definitions with their validator, and the
RAUC A/B OTA templates. Built device images, the thoxd daemon, and the portal
are NOT in this release yet; the layout below marks what is present and what
is planned. Devices ship February to April 2027 with ThoxOS on board.

## Layout (target)

```
entitlement/  PRESENT: entitlement reference implementation (Python, stdlib)
              + 25-test suite implementing the D4 contract: offline signed
              tokens, 30-day grace, free Core features can never be revoked
images/       PRESENT: Buildroot config fragments per compute class
              (e2/ p4/ p6/ qemu/) + units + validator (27 checks)
ota/          PRESENT: RAUC A/B system.conf template + health-gate flow
thoxd/        PLANNED: system daemon + status (Rust)
portal/       PLANNED: device portal + first-boot
mesh-local/   PLANNED: MeshStack Local (discovery + WireGuard local mesh)
sdk/          PLANNED: local API contracts (ThoxAction JSON) + TXF notes
```

Device image repos fold into `images/` by git subtree import (DECIDE-01 D-C4),
preserving history, after one image per class builds from this tree.

## Preview

Annotated end-user walkthroughs (download and install, first boot,
first model, desktop tour) live in [docs/previews/](docs/previews/),
each capture labelled REAL or SIMULATION in
[docs/previews/MANIFEST.md](docs/previews/MANIFEST.md), with the
combined walkthrough video at
`docs/previews/thoxos-ux-walkthrough.mp4`.

## Quick start

```sh
git clone https://github.com/Thox-ai/thoxos-core.git
cd thoxos-core/entitlement && python3 thox_entitlement.py demo && python3 -m unittest
cd .. && python3 images/validate.py
ollama run thox-ai/thoxair-0.5b   # a published THOX model, on any machine
```

Full path: [docs/QUICKSTART.md](docs/QUICKSTART.md).

## Models

The THOX model family lives on the THOX.ai Hugging Face organisation:
https://huggingface.co/Thox-ai — device models are also published on
Ollama under the `thox-ai` namespace. The ThoxOS-Kernel family cards
are published there; its weights ship with ThoxOS host deployments and
are not distributed from this repository.

## Documentation

- [User Guide](docs/USER_GUIDE.md)
- [Quickstart](docs/QUICKSTART.md)
- [Development](docs/DEVELOPMENT.md)
- [Run ThoxOS](docs/RUN.md) — first boot, models, updates, add-ons
- [Kernel](docs/KERNEL.md)
- [Install guides](docs/install/) — bare metal, dual-boot Intel Mac, Apple silicon, device classes
- [Whitepaper](docs/whitepaper/) — "ThoxOS: An Open Kernel and Operating System for Local-First AI" (MD/HTML/PDF/DOCX)
- [Previews](docs/previews/)
- [Release notes](docs/RELEASE_NOTES.md) · [Release manifest](docs/RELEASE_MANIFEST.md) · [Pending-verify register](docs/PENDING-VERIFY.md)
- Agent handoff: [.agents/HANDOFF.md](.agents/HANDOFF.md)

## Releases

Formal releases live on the
[Releases page](https://github.com/Thox-ai/thoxos-core/releases).
v0.1.0 is a source release; its tarball and SHA-256 sidecar are
attached there.

## Governance

THOX.ai LLC is the steward of this repository. Changes to public contracts
(ABIs, local APIs, the free/paid line) require an RFC. The THOX trademark
policy applies: the license covers the code, not the THOX marks.
Publishing and announcement decisions for THOX programmes are made by
the THOX.ai founders.

## Research

The architecture, evidence boundaries and validation protocol for this work are documented in:

**ThoxOS and ThoxInux: Architecture, Evidence, and a Validation Protocol for Local-First AI** (public technical draft, version 0.2.0-review, 1 November 2026), Craig Ross and Tommy Xaypanya, THOX.ai LLC. Paper, source and evidence ledger: https://github.com/ttracx/thox-research-paper/tree/main/papers/thoxos — Release: https://github.com/ttracx/thox-research-paper/releases/tag/thoxos-0.2.0-review

Status: public technical draft; experimental validation is incomplete; not peer reviewed.

## License

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md).
