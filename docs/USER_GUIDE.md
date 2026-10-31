# thoxos-core — User Guide

ThoxOS Core is the free, open-source operating system for THOX devices:
local-first, no account required, no DRM, no kill switch. This guide
covers what v0.1.0 contains, how to run what runs today, and how to
install and run ThoxOS as the programme's images land. Anything that
depends on work not yet done is marked as such, in place — see
[PENDING-VERIFY.md](PENDING-VERIFY.md) for the full register.

Your AI. Your Data. Your Rules.™

## What is in v0.1.0

| Component | State |
| --- | --- |
| Entitlement reference implementation (`entitlement/`) | Working, tested code (25/25 tests). Proves the entitlement contract below. |
| Image definitions + validator (`images/`) | Definitions for classes E2, P4, P6 and QEMU; validator passes 27/27 checks. No device image has been built from these definitions yet. |
| OTA template (`ota/`) | RAUC A/B `system.conf` template with health-gate and automatic-rollback rules. No update bundle has been built or installed yet. |
| `thoxd`, device portal, MeshStack Local, SDK | Planned. Not in this release. |

## Running the entitlement reference implementation

Requires Python 3 (standard library only, no dependencies).

```sh
cd entitlement/
python3 thox_entitlement.py demo          # scripted end-to-end scenario
python3 -m unittest                       # 25 tests
```

The contract it implements (programme decision D4):

- Entitlement is a signed offline token (JWT-shaped, HMAC-SHA256),
  verified on the device with no network call.
- Paid features are enforced by THOX-operated services, never by the
  device refusing to work. Core contains no DRM and no kill switch.
- After a plan ends, paid features keep working for a 30-day grace
  window. After grace, hosted paid features switch off; everything in
  Core — the OS, MeshStack Local, local AI, security updates,
  ThoxBeam Local — keeps working forever. Security updates are never
  paywalled.

Full detail: [entitlement/README.md](../entitlement/README.md) and
[RUN.md](RUN.md).

## Validating the image definitions

```sh
python3 images/validate.py    # 27/27 checks
```

The validator checks every class definition: required files, class-fact
sanity, RAM floor ordering, the portal-enablement regression guard, and
the RAUC A/B slot layout.

## Installing ThoxOS

- Bare metal (64-bit x86_64 and ARM64 PCs): [install/INSTALL-BARE-METAL.md](install/INSTALL-BARE-METAL.md)
- Dual boot on Intel Macs: [install/INSTALL-DUAL-BOOT-INTEL-MAC.md](install/INSTALL-DUAL-BOOT-INTEL-MAC.md)
- Apple silicon (VM route; no native port is claimed): [install/INSTALL-APPLE-SILICON.md](install/INSTALL-APPLE-SILICON.md)
- Device classes E2/P4/P6 (definitions only today; the guide leads with
  that state): [install/INSTALL-DEVICE-CLASSES.md](install/INSTALL-DEVICE-CLASSES.md)

Honest state: a Desktop Edition internal release candidate
(`1.0.0-rc.1+20261025`, Debian 13 + COSMIC) was built and VM-gated; it
is not a v0.1.0 download. v0.1.0 ships its build definitions (in the
`thoxos-images` repository) with the RC's hashes and its four named
open defects recorded. Bare-metal and dual-boot installs have not been
exercised yet.

## Running models

The published THOX device models run anywhere Ollama runs, including a
ThoxOS machine:

```sh
ollama run thox-ai/thoxair-0.5b
ollama run thox-ai/thoxedge-0.8b
ollama run thox-ai/thoxmini-phi4mini
ollama run thox-ai/thoxclip-qwen3-0.6b
```

Serve the Edge model with thinking disabled (`"think": false` at
request level) per its model card. The ThoxOS-Kernel model family is
specialised for kernel and OS work; its cards are published and its
weights are not yet released — see [RUN.md](RUN.md) section 3.2.

## First boot, updates, add-ons

See [RUN.md](RUN.md): first-boot flow, entitlement activation, adding
models, updating, and the paid add-on catalogue. First boot never
requires the internet or an account.

## Kernel

ThoxOS Core runs on linux-thox. See [KERNEL.md](KERNEL.md) and the
`linux-thox` repository.

## Whitepaper

"ThoxOS: An Open Kernel and Operating System for Local-First AI"
(v0.1.0) is in [whitepaper/](whitepaper/) — Markdown, HTML, PDF and
DOCX editions.

## End-user experience captures

Annotated walkthroughs (download and install, first boot and
activation, first model, desktop tour) are in
[previews/](previews/), each labelled REAL or SIMULATION in
[previews/MANIFEST.md](previews/MANIFEST.md), with the combined
walkthrough video at `previews/thoxos-ux-walkthrough.mp4`.

## Troubleshooting

- Tests fail on a clean checkout: confirm Python 3.10+; the entitlement
  suite and validator use only the standard library.
- A guide step references an image or download that does not exist
  yet: check [PENDING-VERIFY.md](PENDING-VERIFY.md) — the item is
  registered there with what closes it.

## FAQ

- **Is ThoxOS Core free?** Yes. Core and MeshStack Local are free and
  open source. Hosted and fleet-scale services are paid add-ons;
  security updates are never paywalled.
- **Does Core phone home?** No. Entitlement verification is offline;
  first boot needs no account.
- **Can I run it today?** The entitlement implementation and validator
  run today. Installable images are not yet published; the desktop
  build definitions and the internal RC record are in `thoxos-images`.

License: Apache-2.0. See [LICENSE](../LICENSE) and [NOTICE.md](../NOTICE.md).
Programme documentation in `docs/` is CC BY 4.0.
