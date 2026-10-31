# thoxos-core — Development

## Architecture

ThoxOS Core is the userspace of ThoxOS: system services (`thoxd`,
planned, Rust), the device portal and first-boot experience (planned),
local AI runtime glue, MeshStack Local (planned), and the Buildroot
image definitions per compute class with RAUC A/B OTA. It runs on
linux-thox (see the `linux-thox` repository). The open/paid line is a
programme decision of record: anything that runs fully on one device
or the user's LAN with no THOX cloud is open and free; anything needing
THOX infrastructure, fleet scale, hosted models, or SLA is a paid
service. Security updates are never paywalled.

## What exists in v0.1.0

- `entitlement/` — reference implementation of the entitlement contract
  (decision D4) in Python (stdlib only), with its 25-test suite.
- `images/` — Buildroot config fragments, expected unit lists and class
  facts for E2/P4/P6/QEMU, plus `validate.py` (27 checks).
- `ota/` — RAUC A/B `system.conf` template.

## Dev environment and tests

Python 3.10+, no third-party dependencies for the shipped code.

```sh
cd entitlement && python3 -m unittest     # 25 tests
python3 images/validate.py                # 27/27
```

## Conventions

- Default branch `main`. DCO sign-off (`Signed-off-by`) on every
  commit. AI-generated contributions must be disclosed in the PR
  description.
- Performance-first implementation choice per component, recorded in
  the change that introduces it. Rust is the default candidate for
  production services and daemons.
- No secrets, tokens, or credentials in the tree, ever.

## Known limitations (v0.1.0)

- No built device image exists; definitions only.
- The entitlement code is a reference implementation with a labelled
  demo secret; production key management is separate work.
- `thoxd`, portal, MeshStack Local and SDK are planned, not present.

## Roadmap

linux-thox first import, `thoxd`, device portal, MeshStack Local, SDK,
built device images, physical-device qualification (programme Gate G1).

## Work log

- 2026-10-29: Phase 1 staging created under the ThoxOS open-source
  programme.
- 2026-10-30: Core 0.1 staging tested (entitlement 25/25, validator
  27/27).
- 2026-10-31: Public release v0.1.0 under programme decision D10.
