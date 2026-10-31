# MANIFEST — ThoxOS Open UX captures pack (2026-10-31)

Labels: **REAL** = capture of an actual running surface. **SIMULATION** = demo/design
surface. **INSTRUCTION CARD** = typeset instructions, not a capture. **GEN** = typeset
video card generated for this pack. **DOC/SCRIPT** = text deliverable.

Provenance paths are the source files the figures were taken from. Figures are
byte-identical to their sources (hardlinked in the build sandbox, which blocks
pixel-content copies; sha256 equality below is the proof). Annotation is carried as
markup (`walkthrough.html` per set); `ANNOTATE.py` bakes it on demand.

## Set A — walkthroughs/a-download-and-install/

| File | sha256 | Label | Source |
|---|---|---|---|
| a-01-target.png | `81f4e1d9d07dcb4b51e082b3f03cb4339cea888896843a2219378253db3c8957` | REAL | thoxos-desktop-previews-work/repo/docs/screenshots/provision/1-target-dark.png |
| a-02-image.png | `9918e2ba06a694b2db3080e04a428ffeefe7943cbb48de385a4607de94bbe4e5` | REAL | …/provision/2-image-dark.png |
| a-03-disk.png | `111e15cfbba784f26cde878eacae0652fba0d0d01e44891e1142663e0990f2be` | REAL | …/provision/3-disk-dark.png |
| a-04-wifi.png | `e399d86197ba2585b013f0b8f87dc5f9dfc50ce84b433074d6540521cf778256` | REAL | …/provision/4-wifi-dark.png |
| a-05-write.png | `88c67c50b11c6ff3dccc500eef07bc54596e3962ad04a701affb460dbc7453f9` | REAL | …/provision/5-write-dark.png |
| a-06-next-steps.png | `40cadb41b9404f482663a06c7f3f6021f89f9d1a366ade56a1bf47ecfb99720c` | REAL | …/provision/6-next-steps-dark.png |
| a-07-apple-silicon-path.png | `d334f9bb104fe963c6a4c353eaf621379d853ae6e2c806b9634e724565aa762d` | SIMULATION | …/docs/screenshots/desk/offline-preview.png (TXF web preview page) |
| WALKTHROUGH.md | `ea0c7bc1307ca50d814fea28dd93327878234b3090fc3386be7a9fb972274a5d` | DOC | Written for this pack |
| walkthrough.html | `bbd1eb6b133923dda652db5524737ffaa8fdc3b5bd2e4ab9c990ed2e70f8abfa` | DOC | Markup walkthrough, #05A451 callout overlays |

## Set B — walkthroughs/b-first-boot-and-activation/

| File | sha256 | Label | Source |
|---|---|---|---|
| b-01-boot-menu.png | `f29abbc06cfb4a89a801bab827119f2632795ee1a259f72df8917386233be0b7` | REAL (VM) | …/vm/x86_64-dual/00-firmware.png, run x86_64-dual-20261025T211931Z |
| b-02-boot-log.png | `bfb8e70b88e17c6f72b24a011fc089d73430dc3b0a4233cfe434a2a5bb6cf845` | REAL (VM) | …/vm/x86_64-dual/01-splash.png |
| b-03-first-run-setup.png | `d30e99741e72a9b67fe5d2d2fdcc2d6c21dee58d153a30920caa68782bc4c43f` | REAL (VM) | …/vm/x86_64-dual/02-greeter.png |
| b-04-shell-home.png | `830351b9c49c5179ad1c42cedb55a7e8856c495c0a64444a6cd8af87c9689f27` | REAL (VM) | …/vm/x86_64-dual/04-shell-home.png (also used as d-01-home) |
| b-05-demo-welcome-annotated.png | `63c99624d7fedaa96ef72e851354e1641e96d9b8c1c377eea4f96e70845c9116` | SIMULATION | thoxos-open-release-20261031/guide/shots/app-step-1-annotated.png (baked) |
| b-06-demo-activation-annotated.png | `3bc24c00d30e7752c6c06eda9ef7fe2d6ec61c7afc10b06b188a1809028b3d7c` | SIMULATION | …/guide/shots/app-step-4-annotated.png (baked) |
| b-07-demo-grace-annotated.png | `9dfca6e17efa842e1af10c4fc7e3859f7eceb0a8b44dccb181da8ce985367329` | SIMULATION | …/guide/shots/app-step-5-annotated.png (baked) |
| b-08-demo-lapse-airplane-annotated.png | `2a159cde803ee04157e18304970a4048283a5fdbb67da7d11d8104c06dd3fc13` | SIMULATION | …/guide/shots/app-step-6-annotated.png (baked) |
| b-09-entitlement-terminal-output.txt | `7735f1678cb41ff166785fd2461a7b233142587e9e06731ed7063668957e7c44` | REAL | thoxos-open-proof-20261030/terminal-demo.txt (reference implementation output) |
| WALKTHROUGH.md | `bea36b3b2c94c12345361188d9805be3fb85c55e7325650ba907c3796f7d8aba` | DOC | Written for this pack |
| walkthrough.html | `f303b368f812d2e56ef083aa31ce3bbfad466d7fc2716d27ede4aa36818e236c` | DOC | Markup walkthrough, #05A451 callout overlays |

## Set C — walkthroughs/c-run-your-first-model/

| File | sha256 | Label | Source |
|---|---|---|---|
| c-01-doctor.png | `1dececfa84e1e24471aa53da3ba2fa3360ba7a5a88ef389b8bf6ee61b97f1950` | REAL (VM) | …/vm/x86_64-dual/08-terminal-doctor.png |
| c-02-first-model-command-card.png | `bfed4c48b333e367f8a18848c27ba315f2d4eb0fe343e5bc06a4ed9ebfdd77db` | INSTRUCTION CARD | Typeset for this pack (ffmpeg/drawtext); commands from the verified model one-liners pack |
| c-03-shell-chat.png | `37639f4334300f1c8bbf392c822288069d947ef539a4bcfecb1bdc48f33cca44` | REAL (VM) | …/vm/x86_64-dual/05-shell-chat.png (also used as d-05-chat) |
| c-04-runtimes-explainer.png | `57994a34545e26597d6ce48834026f77cb4bc1a808b13e785664f929eed63fd3` | SIMULATION | …/docs/screenshots/desk/runtimes.png (TXF web preview page) |
| WALKTHROUGH.md | `7ff6d78740ad0d6c710756328f3e72b4d248aea44a61d2fc217286086b8e473a` | DOC | Written for this pack |
| walkthrough.html | `66a3a4673331823522a9829049371393469c71ce234aeeabac0c7d195a0162d8` | DOC | Markup walkthrough, #05A451 callout overlays |

## Set D — walkthroughs/d-desktop-tour/

| File | sha256 | Label | Source |
|---|---|---|---|
| d-01-home.png | `830351b9c49c5179ad1c42cedb55a7e8856c495c0a64444a6cd8af87c9689f27` | REAL (VM) | Same capture as b-04 (…/vm/x86_64-dual/04-shell-home.png) |
| d-02-devices.png | `8a81489b05846030f47befc9b346f10305a4f48ac195b9633bc900707d34a21f` | REAL (VM) | …/vm/x86_64-dual/06-shell-devices.png |
| d-03-apps.png | `d4cf069099fb66ef532b75ced1a788983caa9ca87ee201dc2c08446f26a539f4` | REAL | …/docs/screenshots/shell/apps-dark-1440.png (compiled shell capture) |
| d-04-vault.png | `734f2359c6dded6baab854f53bec73c538fc8575c5493b87d7890df0968f9932` | REAL | …/docs/screenshots/shell/vault-dark-1440.png (compiled shell capture) |
| d-05-chat.png | `37639f4334300f1c8bbf392c822288069d947ef539a4bcfecb1bdc48f33cca44` | REAL (VM) | Same capture as c-03 |
| d-06-design-boot.png | `1adb58565cfab57084e9b8b33d989ddabb2075f06766515d50c917b37e1e28dd` | SIMULATION | thoxos-desktop-sadie-previews/png/01-boot.png (design render) |
| d-07-design-slate-desktop.png | `5339ff7077d8503e1163fd21cc50d07e8ffc7eede9122e195c44ca0630b89a0f` | SIMULATION | thoxos-desktop-sadie-previews/png/03-v1-slate-desktop.png (design render; any "answer" in it is part of the drawing) |
| WALKTHROUGH.md | `fc6c6c47ed9150e04427688f4affdcc296cab98f1c02cec72667f6958aa6a9af` | DOC | Written for this pack |
| walkthrough.html | `ae40725cb803bf6339b226a036e6168e7200c46dd8060a810f3e4959c56f758e` | DOC | Markup walkthrough, #05A451 callout overlays |

## Video — video/

| File | sha256 | Label | Source |
|---|---|---|---|
| source-entitlement-demo-walkthrough.mp4 | `b9b42cc6806728758a20cc8597cd43cc9dda09e863ddacb88dd169b2a5399756` | SIMULATION (real recording of the demo) | thoxos-open-release-20261031/demo-walkthrough.mp4, 20.0 s |
| source-desktop-preview-walkthrough.mp4 | `de50c087bb7947b00be682f443bc74163462ff0ac421c1abdb4adede261de4f7` | SIMULATION (real recording of the preview page) | thoxos-open-proof-20261030/walkthrough.mp4, 17.4 s |
| card-01-title.mp4 | `9286d22ea29a210cb906f2af94df3d257dd9e2a441d7aaaf018a142d487e5df7` | GEN | Typeset for this pack |
| card-02-part1.mp4 | `2d6a638bbda5dca56bef48d364ef887bfcfbbbc46749a15e2350865c65ccfa65` | GEN | Typeset for this pack |
| card-03-part2.mp4 | `3c33279fea009d87a0372332efdbc852ee01f929c4476dac496b5062e40a47b9` | GEN | Typeset for this pack |
| card-04-close.mp4 | `f454b7e4a59510dcaf4fe9f48a3cd0446c597e4e9d754f0b0d8c44be3df27d92` | GEN | Typeset for this pack |
| concat-list.txt | `813424afb1495d4d7b19ed7d5d436fd6df78f2bfca7095efe585c1571b9acfec` | SCRIPT | Edit decision list |
| ASSEMBLE.sh | `4b90fecccbab05c133797d453ffd7d014bd038892bb03353eb8599f8db991ba5` | SCRIPT | Renders the combined video |
| VIDEO.md | `7048c7a922ee97b4f630638aafd6c365bc10c662bd5968e761c5f7a1c58e9fe5` | DOC | Video status and honesty notes |

## Pack root

| File | sha256 | Label |
|---|---|---|
| README.md | `ea818b700f8eede15ca78411dedc101d7521ab5a69a24298880a1288746161e0` | DOC |
| GAPS.md | `014ad2cbda25837a17a40c59630d207cc9b701823c8b4eb2e75ea875dbf41441` | DOC |
| ANNOTATE.py | `cfba536a63911130c59b17af32759dc89b2f8fb9d3e2895471bf94ea9f3e85a1` | SCRIPT |
| MANIFEST.md | (this file; hash computed on delivery) | DOC |

## Disclosures

- **Duplicates in the source run, excluded:** the VM run's `03-desktop.png` is
  byte-identical to `02-greeter.png`, and `07-thoxy-panel.png` is byte-identical to
  `06-shell-devices.png`. Neither duplicate is presented as a distinct screen.
- **Reused across sets, disclosed:** b-04 = d-01 (shell home) and c-03 = d-05 (shell
  chat); each reuse is named in both walkthroughs.
- **Annotation colour audit:** the markup layer (HTML/CSS) and `ANNOTATE.py` use
  #05A451 exclusively for callouts; the HTML files contain zero occurrences of
  #10B981 or #00FF88 (grep-verified at build time). Source figures were not altered,
  so their own pixels are exactly as captured.
- **Sandbox note:** this build session could not write existing image/video pixel
  content (platform content filter; see GAPS.md Part 2). Figures are therefore
  hardlinks — byte-identical to sources, which the hashes above prove — and the
  baked-annotation and video-concat steps ship as `ANNOTATE.py` and
  `video/ASSEMBLE.sh`.

## Finishing outputs — baked annotations + assembled video (added 2026-10-31)

Produced on KnightHub (WSL2), staged at `/mnt/d/thoxos-ux-finishing-20261031/pack`
(the build sandbox cannot write existing image/video pixel content; KnightHub
can). `ANNOTATE.py` ran clean (exit 0, no forbidden-pixel flags: the annotation
layer uses #05A451 only and no source figure tripped the #10B981/#00FF88 audit).
Labels below are inherited unchanged from each source figure — annotation does
not change a capture's REAL / SIMULATION label. The demo figures b-05..b-08 were
already baked by the release capture team and are not re-processed; the
instruction card c-02 is typeset and skipped, per `ANNOTATE.py`. All outputs
were copied back and verified: local sha256 matches the KnightHub originals
(22/22), and all 47 pre-existing pack files still match the hashes above.

### Baked annotations — walkthroughs/<set>/annotated/

| File | sha256 | Label (inherited) |
|---|---|---|
| a-download-and-install/annotated/a-01-target-annotated.png | `2c41c2aed0b473e945b2566f6835ef27508a7eafa46faacf43781139e2f6b613` | REAL |
| a-download-and-install/annotated/a-02-image-annotated.png | `7c67f07649b00513619892ed84ae1f80515ec849b264233dee0d4a6ed8de21bd` | REAL |
| a-download-and-install/annotated/a-03-disk-annotated.png | `5ede81f34877a38c70f3131158598c32b477304bb774072db56cff3a8be9c7f8` | REAL |
| a-download-and-install/annotated/a-04-wifi-annotated.png | `8978a181fe523555ed1e39c3be21867edfddfa3b79fe13c3b1d564d0ebc97cda` | REAL |
| a-download-and-install/annotated/a-05-write-annotated.png | `24d15abf012e48deaa1e4825123421871f8830e13d9e54b86b4df0959e2787ee` | REAL |
| a-download-and-install/annotated/a-06-next-steps-annotated.png | `544fc4e4e27dfc1f12a4f9d1d7b955ba1c583a12a6b9a01270c77f7d0f15428a` | REAL |
| a-download-and-install/annotated/a-07-apple-silicon-path-annotated.png | `f34fb2c0f3cf0d81da1734f511c42d7b5ceca0a2fe7f8010a7aa7e7a0d0c37a6` | SIMULATION |
| b-first-boot-and-activation/annotated/b-01-boot-menu-annotated.png | `1be2c4ede6fd252949b4a046d743f5b1b2f8a7b057ceac5804204292c01fee98` | REAL (VM) |
| b-first-boot-and-activation/annotated/b-02-boot-log-annotated.png | `6bd116a367004a54327c95d4568a555ca3fad88b357fdf41dd5e442258abf930` | REAL (VM) |
| b-first-boot-and-activation/annotated/b-03-first-run-setup-annotated.png | `2588f0b21174760746c47724aa2d6bc87dff6eb3c82b69e4ae5d39d55967990e` | REAL (VM) |
| b-first-boot-and-activation/annotated/b-04-shell-home-annotated.png | `0aa5ed090e5435d2dba9395dd1c81778d2266022a4ed36b0cc7243310615f794` | REAL (VM) |
| c-run-your-first-model/annotated/c-01-doctor-annotated.png | `b78cb416837c78edcb80da02ca1fb81eca631f5bf53b14dc81a02a41c1671ec1` | REAL (VM) |
| c-run-your-first-model/annotated/c-03-shell-chat-annotated.png | `74ff7fbde998936a71fd73ecf050e66e23fe97b872e8a259b102c739a4c89a5d` | REAL (VM) |
| c-run-your-first-model/annotated/c-04-runtimes-explainer-annotated.png | `9ecb28dad2f2b67fa3c540c706d821ace7eb7566a475661d2f53f76c183afa05` | SIMULATION |
| d-desktop-tour/annotated/d-01-home-annotated.png | `dda212acefa504b81f4f269570727592157648775a256a8e3f276d3482a3f7c0` | REAL (VM) |
| d-desktop-tour/annotated/d-02-devices-annotated.png | `b46f1e9e70acf16c43ba3058b3a79d34d4decdaf1940effa857aac2fff188d24` | REAL (VM) |
| d-desktop-tour/annotated/d-03-apps-annotated.png | `695daa2136eb6bfd50f883b0fed73451e806d56560739ad3bcfb580cb76eec74` | REAL |
| d-desktop-tour/annotated/d-04-vault-annotated.png | `89ce322c97e06fa516d986625970bd148a069bd784f4161b61f8c9fb073aacbb` | REAL |
| d-desktop-tour/annotated/d-05-chat-annotated.png | `b6af0a5fead419e9ec95ee81e0eda3e31d3745d521521a892d33c8b07249a3bb` | REAL (VM) |
| d-desktop-tour/annotated/d-06-design-boot-annotated.png | `01facb80d3150c90e9886a9434222a326c7d0411a79a1f759179b5e1bbe2f6b7` | SIMULATION |
| d-desktop-tour/annotated/d-07-design-slate-desktop-annotated.png | `6fce947c42789200e5a9d634bf62bb6a3815e55a7ac8c967aefd540297868bd1` | SIMULATION |

### Assembled video — video/

| File | sha256 | Label | Notes |
|---|---|---|---|
| thoxos-ux-walkthrough.mp4 | `2c7125903281360d50a77fa564c6f0b1356e3346b063e29fd6a1aadf953a909a` | ASSEMBLED CUT (cards GEN; both recordings SIMULATION surfaces, real recordings) | `sh ASSEMBLE.sh` on KnightHub. 49.4 s, 1440×900, H.264, 30 fps, silent, 1,162,412 B. Duration is the exact sum of the parts: 4 cards × 3.0 s + 20.0 s entitlement recording + 17.4 s desktop recording (the "~52 s" in ASSEMBLE.sh/VIDEO.md was an estimate). Frames spot-checked at 25 s (entitlement demo, step 7) and 45 s (desktop preview, self-labelled SIMULATED UI). |
