# Dual boot ThoxOS on an Intel Mac (alongside macOS)

**Read this first — the honest current state (October 31, 2026).**
No public ThoxOS Desktop Edition image exists yet, so this dual
boot cannot be performed today. An internal Desktop Edition release
candidate (`1.0.0-rc.1+20261025`, Debian 13 + COSMIC) was built and
gated in a VM, but it is not downloadable (v0.1.0 ships its build
definitions and hashes only), it carries four open defects, and no
dual-boot install of it has been exercised. This guide is the
procedure the public image will ship with, published early for
review. Steps depending on the public image are marked
PENDING-VERIFY (register item P5).
This guide is for **Intel** Macs only. If your Mac has an Apple
silicon chip (M1 or later), use INSTALL-APPLE-SILICON.md instead —
the route there is a virtual machine, and it is the only supported
route.

Your AI. Your Data. Your Rules.™

## How this works

An Intel Mac can start up from more than one operating system. You
will make free space on the internal drive, install the ThoxOS
Desktop Edition into that space from a USB stick, and then choose
which system to run each time you start the Mac: hold the **Option
(⌥)** key at startup to get the boot picker. macOS stays installed
and untouched in its own partition the whole time.

## Before you start

You need:

- An Intel-based Mac (check: Apple menu → About This Mac — if it
  says "Chip: Apple M…", stop; use the Apple silicon guide).
- At least 40 GB of free space you can give to ThoxOS (64 GB
  recommended if you plan to keep local AI models on it).
- A USB stick of 8 GB or more (it will be erased).
- A **current Time Machine backup** (or another full backup) of the
  Mac. Repartitioning a drive is the risky step in any dual boot.
  Back up first, and confirm the backup completed.
- The ThoxOS Desktop Edition image and its published SHA-256
  checksum (PENDING-VERIFY — published at thox.ai with the release).
- Your Mac plugged into power.

## Steps

1. **Back up.** Run a Time Machine backup to completion. Do not skip
   this: every later step is reversible except a partitioning
   mistake on an unbacked-up drive.
2. **Make free space.** Open Disk Utility, select the internal drive,
   and use Partition to add a new partition of 40 GB or more. Format
   it as MS-DOS (FAT) as a placeholder — the ThoxOS installer will
   reformat the space it uses. Name it THOX so you can recognise it
   later. Do not delete or resize the macOS partition itself beyond
   adding this new one.
3. **(Macs with the Apple T2 chip only) Allow external booting.**
   Restart into macOS Recovery (hold Command (⌘) + R at startup),
   open Startup Security Utility from the Utilities menu, and set
   "External boot" to allow booting from external media. Macs
   without a T2 chip skip this step.
4. **Download and verify the image, then write the USB stick.**
   Download from thox.ai only; verify with `shasum -a 256
   <image-file>` in Terminal and compare with the published
   checksum, character for character; then write the image to the
   USB stick with a reputable USB writer. A mismatched checksum
   means: delete, download again, do not install.
5. **Boot the installer.** Restart the Mac and immediately hold the
   **Option (⌥)** key until the boot picker appears. Select the USB
   stick (shown as an external / EFI boot volume).
6. **Try the live session.** Confirm keyboard, trackpad, display,
   Wi-Fi, and sound. Intel Mac hardware varies by model year; if
   Wi-Fi does not work in the live session, it will not work after
   install either — stop and check thox.ai for your model's status
   before continuing.
7. **Install into the THOX partition only.** In the installer, choose
   manual / custom partitioning and select the partition you created
   in step 2 as the install target. **Do not select the whole disk,
   and do not touch the macOS partition.** Create the ThoxOS system
   layout inside the THOX space when prompted, set your name and a
   user password, and complete the install.
8. **Restart.** Remove the USB stick. The Mac will start into
   whichever system you pick: hold **Option (⌥)** at startup for the
   picker, and choose macOS or ThoxOS. To change the default, set
   the startup disk in macOS System Settings (or leave macOS as the
   default and use the picker when you want ThoxOS).
9. **First boot of ThoxOS.** Continue with RUN.md: first-boot setup,
   entitlement (only with a paid plan), adding models, updates.

## Verify the dual boot worked

1. Start the Mac holding Option (⌥): both macOS and ThoxOS appear in
   the picker.
2. Boot macOS: it starts normally and your files are as you left
   them.
3. Boot ThoxOS: it reaches the COSMIC desktop; in a terminal,
   `systemctl status thoxd` reports the Core service active.
4. In ThoxOS, disconnect from the internet and open the local AI
   chat: Core works offline with no account (add a model first if
   needed — RUN.md).

## Recovery and removing ThoxOS

- **ThoxOS will not boot, macOS is fine:** boot macOS and use it
  normally — a broken ThoxOS install does not affect macOS. Re-run
  the ThoxOS installer into the THOX partition when ready.
- **A ThoxOS update failed:** the previous system is kept in a
  second slot; the boot menu offers it. Select it to return to the
  last known-good ThoxOS with your files untouched.
- **Remove ThoxOS completely:** boot macOS, open Disk Utility,
  select the THOX partition, and delete it (the minus button in the
  Partition view), then let the macOS partition reclaim the space.
  ThoxOS is gone; macOS and your backup are unaffected.
- **The Mac will not start at all:** boot macOS Recovery (Command
  (⌘) + R) and restore from your Time Machine backup. This is why
  step 1 is not optional.

## Support

Help, downloads, checksums, and per-model hardware notes:
**thox.ai**.

## License

This guide is CC BY 4.0. macOS, Mac, and Time Machine are trademarks
of Apple Inc.; this guide is not affiliated with or endorsed by
Apple.

© 2026 THOX.ai LLC. THOX, ThoxOS, and MeshStack are trademarks of
THOX.ai LLC.
