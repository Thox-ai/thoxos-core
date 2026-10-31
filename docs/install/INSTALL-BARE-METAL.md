# Install ThoxOS on a 64-bit PC (bare metal)

**Read this first — the honest current state (October 31, 2026).**
No public ThoxOS Desktop Edition image exists yet. A Desktop
Edition release candidate (`1.0.0-rc.1+20261025`, Debian 13 +
COSMIC) was built on a fleet host and gated in a VM; it is an
**internal artefact, not a download**: the v0.1.0 release ships its
build *definitions* and the RC's hashes (in the thoxos-images
package), the RC carries four open defects (the greeter fails in
its shipped configuration; the ThoxOS Shell needs a newer C
library than Debian 13 ships; the launcher renders no results; the
porcelain light switch is unproven), and no bare-metal install of
it has been exercised. There is nothing to download today, and any
site offering a "ThoxOS ISO" right now is not us. This guide is the
install procedure the public image will ship with, published with
the documentation so it can be reviewed first. Steps that depend on
the public image are marked PENDING-VERIFY; the documentation set's
PENDING-VERIFY register tracks them (item P5). When the image
ships, this guide is re-issued with the download link, file name,
and checksum filled in.

Your AI. Your Data. Your Rules.™

## What you are installing

The Desktop Edition: Debian 13 with the COSMIC desktop and the
linux-thox kernel (6.12 LTS base; the desktop configuration is
published in v0.1.0 as a config fragment — `thox_desktop_defconfig`
is generated from it at the linux-thox first import), plus
ThoxOS Core — the local services, the model runtime, and the
entitlement client described in the whitepaper. (The internal RC
above predates that import: its kernel is Debian's 6.12.113, not
linux-thox.) Core is free and
works fully offline with no account. Paid add-ons (hosted relay,
cloud routing, premium models, ThoxWork) are optional and explained
in RUN.md.

## Before you start

You need:

- A 64-bit computer: x86_64 (Intel or AMD) or ARM64. 32-bit machines
  are not supported.
- At least 4 GB of RAM (8 GB recommended for local AI models) and
  32 GB of free disk space.
- A USB stick of 8 GB or more. Everything on it will be erased.
- A backup of anything on the computer you cannot afford to lose.
  Installing an operating system can erase a disk if a step is done
  on the wrong drive. Back up first.
- The ThoxOS Desktop Edition image file and its published SHA-256
  checksum (PENDING-VERIFY — published at thox.ai with the release).
- About 45 minutes.

## Steps

1. **Download the image and check it.** Download the Desktop Edition
   image from thox.ai only. Then verify the checksum before using
   the file — this proves the download is complete and untampered:
   - On Linux: `sha256sum <image-file>` and compare with the
     published checksum, character for character.
   - On macOS: `shasum -a 256 <image-file>`.
   - On Windows: `Get-FileHash <image-file>` in PowerShell.
   If the checksum does not match, delete the file and download
   again. Do not install from an unmatched image.
2. **Write the image to the USB stick.** Use a reputable USB writer
   (for example balenaEtcher, or `dd` on Linux/macOS if you are
   comfortable with it). Choose the ThoxOS image as the source and
   the USB stick as the target. Double-check the target: writing
   erases the selected drive completely.
3. **Decide: replace or dual boot.** This guide installs ThoxOS as
   the computer's only system (the installer erases the internal
   disk in step 6). If you want to keep your current system
   alongside, stop here and follow the dual-boot notes in step 6
   instead.
4. **Boot from the USB stick.** Restart the computer and open its
   boot menu (commonly F12, F2, Esc, or Del during startup — your
   manufacturer's support page names the key). Select the USB stick.
   On ARM64 machines, boot the stick through the device's UEFI boot
   menu the same way.
5. **Try it first (recommended).** The installer offers a live
   session. Use it to confirm your keyboard, display, Wi-Fi, and
   sound work before installing anything.
6. **Install.** Start the installer and follow the prompts:
   - Language, keyboard layout, and time zone.
   - Disk choice: "Erase disk and install ThoxOS" for a single-system
     install. For dual boot, choose "Install alongside" / manual
     partitioning and use free space you prepared beforehand — never
     shrink a partition from inside the installer without a backup.
   - Your name, computer name, and a user password. Use a password
     you do not reuse elsewhere.
   - Optional disk encryption: offered at install time. If you
     enable it, the recovery key is yours — THOX cannot recover an
     encrypted disk for you.
7. **Restart and remove the USB stick** when prompted.
8. **First boot.** Continue with RUN.md: first-boot setup,
   entitlement (only if you bought a plan), adding models, and
   updates.

## Verify the install worked

1. The computer boots to the COSMIC desktop without the USB stick.
2. Open a terminal and run `uname -r` — the version should be a
   6.12-series linux-thox build (exact build string PENDING-VERIFY).
3. Run `systemctl status thoxd` — the ThoxOS Core service should
   report active. If it does not, see Recovery below.
4. With the network cable unplugged / Wi-Fi off, open the local AI
   chat and send a message. Core is local-first: it must work with
   no internet and no account. (A model may need to be added first —
   RUN.md covers that.)

## Recovery and rollback

- **Install went wrong before it finished:** boot the USB stick
  again and re-run the installer. An interrupted install is not
  recoverable in place; starting over is the safe path.
- **ThoxOS installed but will not boot:** boot the USB stick, choose
  the live session, and use the installer's repair option when
  offered (PENDING-VERIFY). Your data partition, if the install
  completed, is separate from the system partition by design.
- **An update broke something:** ThoxOS keeps the previous system in
  a second slot. On device-class hardware this rollback is
  automatic. On the Desktop Edition, if a new system fails its
  first-boot health checks, the boot menu offers the previous slot —
  select it, and the system returns to the last known-good state
  with your files untouched.
- **Going back to your previous OS:** reinstall it from your own
  install media. Your backup from "Before you start" is the way
  back; ThoxOS does not keep a copy of another operating system.

## Support

Help, downloads, checksums, and security advisories: **thox.ai**.
Community support is free for everyone; paid plans add SLA support —
see RUN.md for where add-ons plug in.

## License

Desktop Edition components carry their own licenses (kernel
GPL-2.0-only, THOX userspace Apache-2.0, Debian and COSMIC under
theirs). This guide is CC BY 4.0.

© 2026 THOX.ai LLC. THOX, ThoxOS, and MeshStack are trademarks of
THOX.ai LLC.
