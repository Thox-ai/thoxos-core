# ThoxOS on Apple silicon Macs (M1 and later)

**The honest position, first.** There is **no native ThoxOS install
for Apple silicon Macs** — no dual boot, no bare-metal port — and
THOX does not claim one. The supported route today is to run the
ThoxOS Desktop Edition (ARM64) inside a **virtual machine** on macOS,
using UTM (which can use Apple's Virtualization framework). That is
a real, working way to use ThoxOS on an M-series Mac; it is not the
same as running it on the metal, and the limits in this guide are
stated plainly rather than smoothed over.

**Second honest note (October 31, 2026).** No public Desktop
Edition ARM64 image exists yet. An internal Desktop Edition release
candidate (`1.0.0-rc.1+20261025`, Debian 13 + COSMIC) was built and
gated in a VM, but it is not downloadable — v0.1.0 ships its build
definitions and hashes only — and it carries four open defects. The
steps below are the procedure the public release will ship with;
steps depending on the image are marked PENDING-VERIFY (register
item P5).

Your AI. Your Data. Your Rules.™

## What a virtual machine gives you — and what it does not

You get: the full ThoxOS Core experience — the COSMIC desktop, local
AI chat, local models, MeshStack Local participation as a network
peer, offline operation, updates with rollback inside the VM — in a
window on your Mac, with macOS untouched and the VM deletable in one
step.

You do not get: bare-metal performance (expect a capable but not
native-feeling system); direct access to the Mac's GPU/NPU for
inference acceleration (models run on the VM's virtual CPUs, so
choose smaller models than the same Mac could run natively); or
USB/device-class features that need real hardware. If you need
native performance on Apple silicon today, the honest answer is:
not yet. The QEMU/virtual route is also exactly how THOX's own
virtual device lab class works, so the VM experience is a tested
shape, not an afterthought.

## Before you start

You need:

- A Mac with an Apple silicon chip (Apple menu → About This Mac →
  "Chip: Apple M…").
- macOS current enough for UTM's Virtualization support (UTM's site
  states its requirements; keep macOS updated).
- Free disk space: 40 GB or more for the VM (64 GB recommended).
- RAM: the VM needs at least 4 GB; on a Mac with 8 GB total, give the
  VM 4 GB and expect to close heavy Mac apps while it runs. On 16 GB
  or more, 6–8 GB for the VM is comfortable.
- UTM, downloaded from its official site (mac.getutm.app) or the Mac
  App Store.
- The ThoxOS Desktop Edition **ARM64** image and its published
  SHA-256 checksum (PENDING-VERIFY — published at thox.ai with the
  release). Do not use the x86_64 image on Apple silicon.

## Steps

1. **Install UTM** and open it once so macOS finishes its first-run
   approvals.
2. **Download and verify the image.** Download the ARM64 image from
   thox.ai only. In Terminal: `shasum -a 256 <image-file>` and
   compare with the published checksum, character for character. A
   mismatch means delete and download again.
3. **Create the virtual machine.** In UTM choose "Create a New
   Virtual Machine" → "Virtualize" (not "Emulate" — virtualize uses
   the Apple Virtualization performance path) → "Linux".
4. **Attach the image.** Select the ThoxOS ARM64 image as the boot
   image / installation media when UTM asks.
5. **Size the machine.** Memory: 4096 MB minimum (6144–8192 MB if
   your Mac has 16 GB or more). CPU cores: half your Mac's cores is
   a good default. Storage: create a drive of at least 40 GB
   (64 GB recommended).
6. **Name and finish.** Name it "ThoxOS", review the summary, and
   save.
7. **Start the VM and install.** The ThoxOS installer boots inside
   the VM window. Choose "Erase disk and install" — inside a VM,
   "the disk" is the virtual drive you just created; your Mac's real
   drive is not visible to the installer and cannot be erased by it.
   Set your name and a user password, and complete the install.
8. **Restart the VM** when prompted; if it boots from the install
   image again, shut the VM down, remove the installation media in
   UTM's drive settings for this VM, and start it again.
9. **First boot.** Continue with RUN.md: first-boot setup,
   entitlement (only with a paid plan), adding models (pick the
   smaller models — see the note in "What a virtual machine gives
   you"), and updates.

## Verify it worked

1. The VM boots to the COSMIC desktop with no install media
   attached.
2. In a ThoxOS terminal inside the VM: `systemctl status thoxd`
   reports the Core service active, and `uname -m` reports `aarch64`.
3. Turn off the Mac's Wi-Fi (or disconnect the network) and open the
   local AI chat in the VM: Core works offline with no account (add
   a model first if needed — RUN.md). Note: turning off Wi-Fi also
   disconnects the VM, which is the point of the test.
4. Shut the VM down from inside ThoxOS, then start it again from
   UTM: a clean cold boot confirms the install is self-contained.

## Recovery and removal

- **VM misbehaves:** shut it down and start it again; a VM that
  fails its first-boot health checks after an update offers the
  previous slot at its boot menu, exactly as on bare metal.
- **Snapshot habit (recommended):** before big changes, shut the VM
  down and duplicate its file in UTM (right-click the VM → clone /
  duplicate). A clone is a complete spare ThoxOS.
- **Remove ThoxOS completely:** shut the VM down, delete it in UTM,
  and empty the Trash. macOS was never modified; nothing else needs
  cleaning up.
- **Mac problems:** a VM cannot damage macOS. If the Mac itself has
  trouble, that is a macOS matter, not a ThoxOS one.

## Support

Help, downloads, checksums, and UTM setup notes: **thox.ai**.

## License

This guide is CC BY 4.0. macOS, Mac, and Apple silicon are trademarks
of Apple Inc.; UTM is a trademark of its respective owner. This
guide is not affiliated with or endorsed by Apple.

© 2026 THOX.ai LLC. THOX, ThoxOS, and MeshStack are trademarks of
THOX.ai LLC.
