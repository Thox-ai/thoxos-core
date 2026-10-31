# linux-thox — the ThoxOS kernel

**Status as of October 31, 2026.** linux-thox is packaged in the
ThoxOS v0.1.0 release bundle as pins, a build script, an explicitly
empty patch series, and per-class config fragments: Linux 6.6.161
for the device classes and 6.12.115 for the desktop class (pins
verified against kernel.org on release day). The first import of
the Linux LTS source, the patch series itself, and the defconfigs
have **not landed yet** (see *Build instructions* and the
PENDING-VERIFY register in this documentation set). Everything
below describes the kernel's decided design; where a step depends
on the import, it says so.

Your AI. Your Data. Your Rules.™

## What linux-thox is

linux-thox is the kernel ThoxOS Core runs. It is a Linux LTS fork,
licensed GPL-2.0-only, and it is deliberately *not* a new kernel: the
THOX delta on top of upstream Linux is a readable patch series plus
published configuration files, so anyone can see exactly what THOX
changes and why. `git log v6.6..HEAD` is the whole THOX story — that
one command is the audit surface. In v0.1.0 the configuration is
published as per-class config *fragments* (intent, under `configs/`
in the linux-thox package); the defconfig files are generated from
those fragments at the first import.

| Base | Used for | Why |
| --- | --- | --- |
| Linux 6.6 LTS (v0.1.0 pin: 6.6.161) | Device classes E2, P4, P6 | Long-term support series, programme-locked for devices until a device-qualification cycle justifies moving |
| Linux 6.12 LTS (v0.1.0 pin: 6.12.115) | Desktop class | Current long-term support series for the Desktop Edition (Debian 13 userland, COSMIC desktop) |

Full source accompanies every binary image, with the GPL source
offer, at release.

## The patch series

Target: fewer than 30 patches, each upstreamable in principle. The
series is organised in six families (from the staging PATCHES.md,
the design of record):

1. **BSP and device enablement** per production compute class, at
   category level.
2. **MagStack connector detection** with power and clustering
   uevents — the kernel exposes the interface only; scheduling
   decisions live in userspace (the Scheduler, whose advanced form is
   a paid service, never a kernel module).
3. **Accelerator plumbing** via upstream DRM/accel and dma-buf. No
   binary blobs live in this repository.
4. **Hardening**: KSPP-recommended configuration, module signing,
   lockdown, dm-verity support.
5. **Low-memory and burst tuning** for the smallest class: zram and
   MGLRU for E2; inference-burst scheduler and cpufreq defaults.
6. **Memory-tier pressure signals** for `thox-kvd` v1 — signals only;
   no KV-cache transfer happens in-kernel.

The series is extracted from the THOX Insider line (`thoxos-insider`,
Developer Edition) at first import: the Insider delta is re-expressed
as this series, and anything upstream has since absorbed is dropped
rather than carried. The import runs on a fleet host with the source
tree; it does not happen from the staging skeleton. In the v0.1.0
package the series framework is present and the series itself is
explicitly empty — the six families above are the intent it will
carry, not patches that exist today.

## Configuration classes (defconfigs specified; fragments published)

Four defconfigs are specified to define what each class builds.
**No defconfig file exists yet**: they are generated at the first
import. What v0.1.0 publishes is the same intent as four per-class
config fragments (`configs/` in the linux-thox package, one per
class below), which the build script merges over the pinned base
configuration. Read the table as the specification the fragments
express and the defconfigs will encode.

| Defconfig (specified) | Class | Floor summary |
| --- | --- | --- |
| `thox_e2_defconfig` | E2 — ThoxAir (Wireless Edge Node) | Quad-core Arm 64-bit, 1.6 GHz+; 2 GB RAM; 16 GB flash |
| `thox_p4_defconfig` | P4 — ThoxMini (Personal Edge Server) | 8-core hybrid Arm, NPU 3 TOPS+; 4 GB RAM; 32 GB flash |
| `thox_p6_defconfig` | P6 — ThoxClip (clip-on edge compute) | P4 floors with 6 GB RAM; 64 GB flash |
| `thox_desktop_defconfig` | Desktop | 64-bit x86_64 and ARM64 personal computers |

There is also a virtual QEMU class used as the lab and CI target,
mirroring the E2 configuration. Results on it qualify software
behaviour, never physical hardware.

## Build instructions

**PENDING-VERIFY: the first import has not landed, so the defconfig
targets below describe the intended tree. What exists today is the
v0.1.0 package: `tools/build-linux-thox.sh` downloads the pinned
tarball for your class, verifies its SHA-256 against kernel.org's
published sums (fail closed), applies the (empty) patch series,
merges the class config fragment, and builds — that script is the
runnable path in v0.1.0. The defconfig targets become runnable when
the import lands and the defconfigs are generated from the
fragments; the register in this documentation set tracks that item
(P2).**

Prerequisites: a 64-bit Linux build host, the standard kernel build
toolchain (compiler, `make`, `bc`, `bison`, `flex`, `libssl-dev` or
your distribution's equivalents), and enough disk for a kernel tree
and build output (plan on 30 GB free).

1. Get the linux-thox package (`linux-thox-0.1.0.tar.gz` in the
   v0.1.0 release bundle; the public repository is created at the
   publication step — publication is directed under decision D10,
   and the register tracks the step itself as PENDING-VERIFY P7).
2. Check out the release tag for your target base (`v6.6`-series for
   devices, `v6.12`-series for desktop).
3. Configure for your class (after the first import):
   `make ARCH=arm64 thox_e2_defconfig` (substitute your class:
   `thox_p4_defconfig`, `thox_p6_defconfig`, or
   `make thox_desktop_defconfig` on x86_64). In v0.1.0, use the
   build script instead, which merges `configs/` fragments.
4. Build: `make -j"$(nproc)"` (add `Image` / `modules` targets as your
   packaging requires on ARM64).
5. Verify what you built is what THOX published: the THOX delta is
   the commit series on top of the LTS tag — review it with
   `git log v6.6..HEAD` before trusting a tree from any mirror.
6. CI expectation at release: the defconfigs, once generated and
   published with the first import, build clean for arm64 and
   x86_64 and boot under QEMU (release evaluation gate H3 in the
   whitepaper). Until CI output is public, treat any
   prebuilt kernel binary from a third party as untrusted.

## The other kernel: Thox Kernel Lab

THOX also maintains the **Thox Kernel Lab**, a clean-room research
programme specifying a small capability-based kernel with a formally
analysed core. It is **specifications only** (documents S1–S9, two
rounds complete, one scheduler item — S9.3, the inference-waiter wake
policy — still open). No code has been ported into it from any
earlier kernel project, and nothing in ThoxOS runs on it. A Lab
design may graduate into ThoxOS only by passing a graduation gate:
prototype, differential test evidence against linux-thox, a migration
plan, and a public decision record. The Lab exists so the long-term
kernel research is public and honest; the shipping kernel is Linux,
and this document set never blurs the two.

## Contribution posture

- Contributions are accepted under the Developer Certificate of
  Origin: add a `Signed-off-by` line (DCO 1.1) to every commit.
- AI-generated contributions must be disclosed in the pull-request
  template.
- Changes to public contracts — kernel ABIs, local APIs, and the
  free/paid feature line — require a public RFC before code.
  Security fixes and patch-series maintenance do not.
- Patches should be upstreamable in principle; THOX-specific glue
  belongs in the patch series or in userspace, not in drivers copied
  out of upstream.
- The license covers the code, not the marks: forks may not call
  themselves ThoxOS or use THOX trademarks. "Built on ThoxOS Core" as
  a factual statement is allowed.
- Security reports: follow the security contact published at thox.ai
  at release time (PENDING-VERIFY P7).

## License

linux-thox is GPL-2.0-only. This document is CC BY 4.0.

© 2026 THOX.ai LLC. THOX, ThoxOS, and MeshStack are trademarks of
THOX.ai LLC.
