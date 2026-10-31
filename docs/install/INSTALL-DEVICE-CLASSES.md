# ThoxOS on THOX devices (classes E2, P4, P6)

**Read this first — the honest current state (October 31, 2026).**
No ThoxOS device image has been built yet for any class — not for
ThoxAir, not for ThoxMini, not for ThoxClip — and **no device is
qualified**. What exists today is the class specification (below), a
validator that checks those specifications (27 of 27 checks pass on
the staging tree), and the update design this guide describes. There
is nothing to flash today, and any site offering a "ThoxOS device
image" right now is not us. This guide is published with the
documentation so the procedure can be reviewed before images exist;
every step that depends on a built image is marked PENDING-VERIFY
(register items P3 and P4).

Your AI. Your Data. Your Rules.™

## The classes

ThoxOS targets are classes with category-level floors, not
individual boards. An image is built per class.

| Class | Device | Floor summary | On-device model class |
| --- | --- | --- | --- |
| E2 | ThoxAir (Wireless Edge Node) | Quad-core Arm 64-bit (1.6 GHz+); 2 GB RAM; 16 GB flash | ~1B, 4-bit |
| P4 | ThoxMini (Personal Edge Server) | 8-core hybrid Arm, NPU 3 TOPS+; 4 GB RAM; 32 GB flash | ~3B, quantized |
| P6 | ThoxClip (clip-on edge compute) | P4 floors with 6 GB RAM; 64 GB flash | ~3B, quantized |
| QEMU | Virtual lab / CI | Virtual, mirrors E2 | Mirrors E2 |

Device images are built with Buildroot (v1 decision) and carry the
linux-thox kernel (6.6 LTS base, v0.1.0 pin 6.6.161) with the
matching class configuration — published in v0.1.0 as per-class
config fragments; the class defconfigs they express
(`thox_e2_defconfig`, `thox_p4_defconfig`, `thox_p6_defconfig`) are
generated at the linux-thox first import, which has not happened
yet (PENDING-VERIFY P2).

## How a device gets its first image (the factory/recovery flow)

PENDING-VERIFY throughout this section: the flow is specified; it has
never been executed on hardware.

1. **Get the right image.** From thox.ai, download the factory image
   for your device's class and verify its published SHA-256 checksum
   before use (on any computer: `sha256sum <image-file>` on Linux,
   `shasum -a 256` on macOS). A wrong-class image is rejected by the
   device's installer checks by design; a wrong checksum means
   delete and download again.
2. **Prepare the install medium** named in the release notes for your
   class (the release notes are part of the image package,
   PENDING-VERIFY P3) and write the factory image to it with a
   reputable USB/SD writer.
3. **Start the device into recovery.** The per-device recovery entry
   (button sequence or boot-menu key) ships in the device's own quick
   start; it is hardware documentation, and it is part of the image
   package rather than this guide.
4. **Flash.** The recovery installer verifies the image signature
   before writing anything (an unsigned or tampered image is a hard
   reject), writes the factory image across both system slots and
   creates the persistent data partition, then reboots.
5. **First boot and health gate.** The device runs its first-boot
   health checks (Core service, portal, local mesh, networking). If
   they pass, setup begins — continue with RUN.md. If they fail, the
   device stays in recovery and says so; re-flash from step 2 with a
   freshly verified image.

## How updates work after that (no flashing, ever)

Day-to-day updates never use the flashing flow. Updates arrive as
signed bundles installed by RAUC into whichever system slot is idle;
the device reboots into the new slot, runs the health gate, and
either stands on the new system or **rolls back automatically** to
the previous one, with your data partition untouched either way. You
never need a computer, a cable, or a recovery session for an update,
and a lapsed subscription never blocks one: security updates are a
free Core feature. RUN.md covers checking for and applying updates.

## Verify (once images exist)

1. The device boots to the ThoxOS portal and completes first-boot
   setup (RUN.md).
2. The portal's About panel shows the class, the image version, and
   the active slot.
3. With the device disconnected from the internet, local chat and
   the local mesh still work (Core is local-first; no account is
   required for anything in this paragraph).
4. After the first update, the About panel shows the other slot
   active — proof the A/B flow, not a reflash, did the work.

## Recovery

- **Bad update:** nothing to do — rollback is automatic (above). If
  a device ever fails to return on the previous slot, use the
  recovery flow with a verified factory image; your data partition
  is preserved by the recovery installer unless you explicitly
  choose a full erase.
- **Forgotten device password:** recovery flow, "reset with data
  preserved" option where offered (PENDING-VERIFY P3). If you
  enabled disk encryption with your own key, a forgotten key means
  the data is unrecoverable by design — THOX holds no copy.
- **Bricked (no boot at all):** the recovery flow is the designed
  path back; if recovery itself cannot start, that is a hardware
  service matter — contact support via thox.ai.

## Support

Help, image downloads, checksums, and recovery documentation:
**thox.ai**. Community support is free; paid plans add SLA support.

## License

This guide is CC BY 4.0.

© 2026 THOX.ai LLC. THOX, ThoxOS, ThoxAir, ThoxMini, ThoxClip, and
MeshStack are trademarks of THOX.ai LLC.
