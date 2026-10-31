# Release manifest — ThoxOS v0.1.0 (2026-10-31)

Every artifact in `bundle/`, with SHA-256 and size. All hashes were
computed on the packaged files and re-verified after archiving
(`sha256sum -c` passes on every sidecar).

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `thoxos-core-0.1.0.tar.gz` | 23,136 | `f9ed49a0a986dab83ef048083cd8f33548ee7349c0942f9660c6e55d243247df` |
| `linux-thox-0.1.0.tar.gz` | 13,677 | `4f58b57d39feb256ad1ade9d8b95be3d90a980c024c15c43ce9ee850f793f84a` |
| `thox-kernel-lab-specs-0.1.0.tar.gz` | 12,689 | `e05072efc07c8357c8ab902d13d7e7b87238d132597855c7fcc1bb96d0e6c90f` |
| `thoxos-images-0.1.0.tar.gz` | 18,977 | `c72a778ccf2dce1667957499aa79827791492613dc49c355a16f2d8066cc1d65` |

Each tarball also ships with a `<name>.tar.gz.sha256` sidecar in
`bundle/`. Supporting documents at the release root (not in `bundle/`):
`INVENTORY.md`, `RELEASE_NOTES.md`, `BUILD-ATTEMPT-LOG.md`,
`PUBLISH-RUNBOOK.md`.

## Provenance and fidelity

- **thoxos-core-0.1.0**: assembled from the staging tree
  `thoxos-opensource-20261029/phase1/thoxos-core` at commit `67085d5`
  (on tag `v0.1.0-staging`). 30/30 files byte-identical to staging,
  verified per-file by SHA-256. Test evidence: entitlement suite
  25/25 OK and image validator 27/27, run from the packaged tree and
  again from the extracted tarball (see BUILD-ATTEMPT-LOG.md).
- **linux-thox-0.1.0**: the 9 staging files (`ab75bf1`) are
  byte-identical except `README.md`, whose status block was rewritten
  for the release package to state the v0.1.0 scope plainly (staging
  original sha256 `52015e5f…`). Authored for this release:
  `BUILDING.md`, `tools/build-linux-thox.sh`, `patches/README.md` +
  `patches/series` (empty series), `configs/README.md` + four config
  fragments. Pins verified against kernel.org `releases.json`
  2026-10-31: Linux 6.6.161 (devices), 6.12.115 (desktop).
- **thox-kernel-lab-specs-0.1.0**: 9 of 10 files byte-identical to
  staging (`38fcc45`); `README.md` status block rewritten for the
  release package the same way (staging original sha256 `fd4ee616…`).
- **thoxos-images-0.1.0**: `device/` is byte-identical to the
  thoxos-core `images/` + `ota/` trees (17/17 files). `desktop/`
  definition files are byte-identical to the desktop build tree
  (`thoxos-debian/repo`): variants.json `0aa46eb1…`, mkosi.conf
  `725fe3fc…`, mkosi-cosmic.conf `211b5506…`,
  Dockerfile.builder-debian `fe11f53d…`, repart.d set `ed285c79…` /
  `5a364294…` / `ad84cf07…` / `0c4bc77c…`; `thoxd.service` transcribed
  from `thoxos-debian/thoxd.service.txt`. The two package READMEs are
  authored for this release.

## Claim limits (binding on all release copy)

1. **No built device image exists.** The e2/p4/p6/qemu classes are
   Buildroot *definitions* (fragments), validated for internal
   consistency only. No device has booted ThoxOS Core from this tree.
2. **No THOX-patched kernel exists.** The linux-thox patch series is
   empty in v0.1.0; the defconfigs named in the README land with the
   first import. A build from this package produces the pinned
   upstream LTS kernel with THOX config fragments — and could not be
   executed in the packaging environment (blockers in
   BUILD-ATTEMPT-LOG.md §2).
3. **The desktop RC is internal.** The Debian 13 + COSMIC desktop
   artifacts (`1.0.0-rc.1+20261025`) were built on a fleet host and
   VM-gated; they are not in this bundle (a 6.5 GB `.img.zst` is a
   release-asset decision for the publish pass, with the four named
   defects in the open), they are not bare-metal or dual-boot proven,
   and their kernel is Debian's 6.12.113, not linux-thox.
4. **Kernel Lab is specifications only.** S1–S9 are requirements
   extracted under the Clean-Room Charter. There is no Lab code, and
   S9.3 (inference-waiter wake policy) is openly undefined in the
   source design and remains an open specification task.
5. **The entitlement code is a reference implementation.** It proves
   the D4 contract (signed offline tokens, 30-day grace, free Core
   features never gated) with a labelled demo secret; it is not
   production key management.
6. **No model weights of any kind are in this bundle.** The model
   programme is separate; nothing here speaks to it.
7. Devices ship February–April 2027 per the campaign; nothing in this
   bundle changes or evidences device qualification (Gate G1 remains
   open in the programme record).
