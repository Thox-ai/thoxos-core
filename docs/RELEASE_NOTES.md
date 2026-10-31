# ThoxOS v0.1.0 — Release Notes

**Date:** 2026-10-31 · **Programme:** ThoxOS Open (ThoxOS Core, linux-thox,
Thox Kernel Lab) · **Licenses:** GPL-2.0-only (kernel package),
Apache-2.0 (Core userspace, Kernel Lab), CC BY 4.0 (programme docs)

ThoxOS v0.1.0 is the first packaged release of the ThoxOS open-source
programme: the source and specifications that exist today, packaged
honestly at the state they are actually in. It is a source release.
What runs, what is specification, and what is planned are separated
below and are not interchangeable.

## What runs today

- **Entitlement reference implementation** (`thoxos-core`, `entitlement/`)
  The D4 contract in working, tested code: signed offline tokens
  (JWT-shaped, HMAC-SHA256), a 30-day grace window, and the guarantee
  that free Core features — the OS itself, MeshStack Local, local AI,
  security updates, ThoxBeam Local — are never gated by any token
  state. 25-test suite passes from the packaged tree and from the
  extracted release tarball. This is a reference implementation for the
  contract, with a labelled demo secret; production key management is
  separate work.
- **Image-definition validator** (`thoxos-core`, `images/validate.py`)
  Validates every device-class definition and the OTA template:
  27/27 checks pass. Its two regression guards were exercised against
  deliberately broken trees during packaging and fire correctly —
  including the guard for the historical defect where a device image
  shipped with its portal service present but never enabled.
- **ThoxOS Desktop Edition (internal RC, previously built)** — Debian
  13 + COSMIC, version `1.0.0-rc.1+20261025`, built on a fleet host and
  gated in a VM harness before this release. The RC artifacts are not
  attached to v0.1.0; this release ships their build *definitions*
  (`thoxos-images`, `desktop/`) with the RC hashes and its four named
  defects recorded in the open (see the images package README). The
  desktop RC is an internal evaluation build, not a public download.

## What is specification

- **Thox Kernel Lab S1–S9** (`thox-kernel-lab-specs`): the clean-room
  specification set for the experimental Rust microkernel — syscall
  ranges, design principles, tiered memory T0–T6, device fabric
  framing, mesh cognition, compliance at the boundary, the agent
  object lifecycle and capability model (S7), invariants as
  behavioural requirements (S8), and scheduler behaviour (S9). One
  item is openly unfinished: S9.3 names the inference-waiter wake
  policy without defining it; defining it is an open specification
  task. No Lab kernel code exists yet, and no shipping device runs or
  is promised to run Lab code — shipping devices run ThoxOS Core on
  linux-thox.
- **linux-thox patch intent** (`PATCHES.md`): six intent areas, target
  fewer than 30 upstreamable patches. Intent, not patches.

## What is definition (not built output)

- **Device image definitions** for classes E2, P4, P6 and the QEMU
  virtual-lab class: Buildroot config fragments, expected systemd
  unit lists (the image CI assertion source), machine-readable class
  facts, and the RAUC A/B OTA template with its health-gate and
  automatic-rollback rules. No image has been built from these
  definitions yet.
- **Desktop build definitions**: the mkosi configurations and layout
  that produced the internal RC above.
- **linux-thox v0.1 packaging**: pinned upstream bases (Linux 6.6.161
  for device classes, 6.12.115 for desktop, verified against
  kernel.org on release day), an empty patch-series framework, and
  per-class config fragments expressing the hardening and low-memory
  intent. The build script downloads the pinned tarball, verifies its
  SHA-256 against kernel.org's published sums (fail closed), applies
  the series, merges the fragment, and builds. The kernel build could
  not be executed in the packaging environment; the exact blockers
  are recorded in BUILD-ATTEMPT-LOG.md.

## What is planned (not in this release)

- The linux-thox first import: the THOX patch series extracted from
  the Insider line on a fleet host, and the full `thox_*_defconfig`
  files generated from these fragments.
- `thoxd` (the Rust system daemon), the device portal, MeshStack
  Local, and the SDK inside thoxos-core.
- Built device images per class, and physical-device qualification
  (programme Gate G1) ahead of the February–April 2027 device ship
  window.
- Kernel Lab implementation crates (`lab-abi`, `lab-util`,
  `lab-tier-memory`) under the Clean-Room Charter's provenance rules.
- Desktop RC defect fixes: the cosmic-greeter shipped-configuration
  failure, the ThoxOS Shell glibc floor, the launcher result list,
  and the porcelain light switch — then bare-metal and dual-boot
  proof.

## Included packages

| Package | Contents |
| --- | --- |
| `thoxos-core-0.1.0.tar.gz` | ThoxOS Core source: entitlement reference implementation + tests, image definitions + validator, RAUC OTA template, docs |
| `linux-thox-0.1.0.tar.gz` | Kernel packaging: pins, build script, empty patch series + intent, config fragments |
| `thox-kernel-lab-specs-0.1.0.tar.gz` | Kernel Lab specifications S1–S9 + Clean-Room Charter |
| `thoxos-images-0.1.0.tar.gz` | Device-class definitions + OTA template; desktop (Debian 13 + COSMIC) build definitions |

Hashes and claim limits: `RELEASE_MANIFEST.md`. Build evidence:
`BUILD-ATTEMPT-LOG.md`. Asset provenance: `INVENTORY.md`.
