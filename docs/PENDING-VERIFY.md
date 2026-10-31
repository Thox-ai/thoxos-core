# PENDING-VERIFY register — ThoxOS documentation set, 2026-10-31

Every claim in this documentation set that depends on work not yet
done is listed here instead of being asserted in the documents. The
whitepaper, KERNEL.md, the install guides, and RUN.md cite these
item numbers at the point of use. An item leaves this register only
when the evidence named in its "closes when" line exists and has
been checked by whoever re-issues the affected document.

Verified at writing time (2026-10-31): the entitlement reference
implementation passes 25 of 25 tests in the staging tree; the
image-definition validator passes 27 of 27 checks; the kernel and
Lab repositories are scaffolds/specifications as described.

**Reconciliation update (2026-10-31, after bundle verification).**
Team F's release bundle now exists at
~/workspace/thoxos-release-20261031/bundle/ and is verified
(Sadie, 2026-10-31: `sha256sum -c` passes on all four artefacts).
Items P1 and P8 are resolved below on that evidence; P7 is re-based
on decision D10. Publication itself — creating the public
repositories and download pages — has not happened yet; it is the
last step of the release, per D10.

| ID | Pending item | Blocks / cited by | Closes when |
| --- | --- | --- | --- |
| P1 | **RESOLVED (2026-10-31).** Release bundle contents verified from Team F's build in ~/workspace/thoxos-release-20261031/bundle/ (`sha256sum -c` passes on all four; RELEASE_MANIFEST.md is the record). The v0.1.0 bundle is: `thoxos-core-0.1.0.tar.gz` (23,136 B, sha256 `f9ed49a0a986dab83ef048083cd8f33548ee7349c0942f9660c6e55d243247df`); `linux-thox-0.1.0.tar.gz` (13,677 B, sha256 `4f58b57d39feb256ad1ade9d8b95be3d90a980c024c15c43ce9ee850f793f84a`); `thox-kernel-lab-specs-0.1.0.tar.gz` (12,689 B, sha256 `e05072efc07c8357c8ab902d13d7e7b87238d132597855c7fcc1bb96d0e6c90f`); `thoxos-images-0.1.0.tar.gz` (18,977 B, sha256 `c72a778ccf2dce1667957499aa79827791492613dc49c355a16f2d8066cc1d65`). Download locations are not part of this resolution; they arrive with the publication step (P7) | Whitepaper status box; release copy | Bundle exists and is hash-verified; names, sizes, and checksums above are copied from the built artefacts |
| P2 | linux-thox first import: LTS source import, patch-series extraction from the Insider line, the four defconfigs (`thox_e2_defconfig`, `thox_p4_defconfig`, `thox_p6_defconfig`, `thox_desktop_defconfig`), and arm64 + x86_64 CI | KERNEL.md build instructions; whitepaper §5.1, gate H3 | Import commit exists in the repo; CI output for both architectures is recorded |
| P3 | Built Buildroot device images per class (E2, P4, P6, QEMU) and a first boot of at least the QEMU class | INSTALL-DEVICE-CLASSES.md (whole flashing flow); RUN.md portal flows; whitepaper §7–§8 | Image artefacts exist with checksums; a boot log or capture is on record |
| P4 | A RAUC bundle actually built, installed to an idle slot, health-gated, and a deliberately broken bundle rolled back automatically | INSTALL guides' rollback sections; RUN.md §4; whitepaper §8, gate H2 | The install + rollback sequence is executed on at least one target (QEMU class acceptable for the first closure) and logged |
| P5 | Desktop Edition installable image (Debian 13 + COSMIC + linux-thox desktop defconfig) for x86_64 and ARM64. **State note (2026-10-31):** an internal Desktop Edition release candidate exists — `1.0.0-rc.1+20261025`, Debian 13 + COSMIC, built on a fleet host and gated in a VM — but it is **not** a v0.1.0 downloadable asset: v0.1.0 ships its build *definitions* and the RC's hashes only (see the thoxos-images package README), the RC carries four open defects (cosmic-greeter fails in its shipped configuration; the ThoxOS Shell requires GLIBC_2.43 against Debian 13's 2.41; the launcher renders no results; the porcelain light switch is unproven), its kernel is Debian's 6.12.113 rather than linux-thox, and bare-metal and dual-boot installs are unexercised | INSTALL-BARE-METAL.md; INSTALL-DUAL-BOOT-INTEL-MAC.md; INSTALL-APPLE-SILICON.md; RUN.md desktop flows | A public installable image exists with checksums; one install per guide route is performed and the guide re-issued with real file names |
| P6 | ThoxOS kernel model weights (27B teacher; 4B and 0.8B students after base selection) and their filled evaluation sections | Whitepaper §9.2; RUN.md §3.2 | Weights exist in the family repositories with evaluation results recorded on the cards; per-member release gates in the kernel release plan are met |
| P7 | Public publication itself: repository URLs, download pages, security contact. **Authorisation basis changed (2026-10-31):** publication is directed by decision **D10** (Tommy, 2026-10-31 06:17 CT), which supersedes the D9 announcement-only amendment for ThoxOS — ThoxOS is released genuinely public, with the publication flip as the LAST step, after bundle verification (done: see P1). **What remains:** the publication step itself — creating the public repositories and release/download pages, publishing the security contact, and verifying every URL live by an anonymous check. The desktop build tree publishes as its own repository in a separate later pass (CAO sequencing under D10), and the 6.5 GB COSMIC `.img.zst` is NOT a v0.1.0 release asset | KERNEL.md (clone URL, security contact); all guides (download locations) | Public repositories and download pages exist; URLs verified live by an anonymous check |
| P8 | **RESOLVED (2026-10-31) on Team F's packaging evidence** (BUILD-ATTEMPT-LOG.md §1 in the release directory). The validator's two broken-tree regression guards were exercised manually against copies of the packaged tree, and both fire correctly: portal enablement marker removed from `images/e2/units.txt` → validator reports **26/27, FAIL: e2 thoxos-portal.service carries enablement marker (portal regression guard)**; `[slot.rootfs.1]` renamed in the RAUC template → validator reports **26/27, FAIL: rauc template defines [slot.rootfs.1]**. The guards behave exactly as designed. Note on method: the automated unittest versions of these two tests still cannot run in the packaging sandbox (Python `tempfile` has no usable temporary directory there — an environment limit, not a tree defect), so the resolution rests on the manual exercise recorded by Team F, not on a green unit-suite run | Whitepaper §10.2 | Broken-tree behaviours exercised and recorded (done, per Team F's log) |

## The "not yet" list, in one place

For the reader who wants the gaps without the register format:

- No ThoxOS *device* image has been built. A Desktop Edition
  release candidate (Debian 13 + COSMIC, `1.0.0-rc.1+20261025`) was
  built previously and gated in a VM; it is an internal artefact
  with four open defects, it is not part of the v0.1.0 bundle
  (which ships its build definitions and hashes), and no
  bare-metal or dual-boot install of it has been exercised (P5).
- No device is qualified; nothing has run on physical ThoxAir,
  ThoxMini, or ThoxClip hardware.
- The Linux kernel tree has not been imported; there are no
  defconfigs yet. The v0.1.0 linux-thox package ships the pinned
  bases (Linux 6.6.161 for devices, 6.12.115 for desktop), the
  build script, an explicitly empty patch series, and per-class
  config fragments labelled as intent.
- No update bundle has ever been installed or rolled back.
- No kernel-model weights exist; the student bases are not chosen.
- There is no native ThoxOS route for Apple silicon, by design
  honesty: the VM route is the supported one.
- The v0.1.0 release bundle exists and is hash-verified (P1), but
  nothing in this set is publicly downloadable yet: publication is
  directed under D10 and the publication step itself is what
  remains (P7).

## License

This register is CC BY 4.0.

© 2026 THOX.ai LLC.
