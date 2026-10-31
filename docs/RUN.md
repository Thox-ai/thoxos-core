# Run ThoxOS: first boot, models, updates, add-ons

**State note (October 31, 2026).** The entitlement behaviour in this
guide is implemented and test-verified in the ThoxOS staging tree
(25 of 25 tests). The screens named below are the specified first-run
experience; they are exercised on real images only when images are
built (PENDING-VERIFY register, items P3 and P5). Where this guide
says a model or image is not available yet, it is not — yet.

Your AI. Your Data. Your Rules.™

## 1. First boot

1. Power on. ThoxOS runs its first-boot health checks (Core services,
   portal, local mesh, networking) before it shows you anything — a
   device that cannot pass them says so instead of failing silently
   later.
2. Choose language, keyboard, and time zone.
3. Connect to your network, or skip it. **No step of first boot
   requires the internet or an account.** A device keypair is created
   on the device, locally; it is registered to an account only if
   you later sign in for paid services.
4. Create your user and password.
5. You land on the ThoxOS portal (devices) or the COSMIC desktop
   (Desktop Edition). Core is fully working at this point: local AI
   (once a model is added, section 3), local files and apps,
   MeshStack Local with your other devices, and security updates.

## 2. Entitlement: only if you bought a plan

Core needs no activation, no key, and no sign-in — ever. Entitlement
exists only to switch on paid add-ons (section 5), and it is built so
it can never take Core away:

1. Sign in with your THOX account from the portal's Services page
   (or the account page at thox.ai) and choose "Activate this
   device".
2. The device receives a signed entitlement token and stores it
   locally. From then on, verification happens **on the device,
   offline** — no check-in, no phone-home.
3. What the states mean, in plain terms:
   - **Active:** your plan is current; paid features are on.
   - **Grace (30 days):** your plan's term ended within the last 30
     days. Paid features keep working while you renew. A device that
     cannot reach the internet is never cut off abruptly.
   - **Expired:** more than 30 days past the term. Paid *hosted*
     features switch off. **Everything in Core keeps working —
     including security updates, which are free by policy and are
     never gated.**
   - Nothing about expiry can brick, lock, or degrade your device.
     There is no kill switch and no DRM in ThoxOS; paid services are
     enforced by the hosted services themselves, not by your device
     refusing to work.
4. Moving to a new device: sign in there and activate it; your old
   device keeps Core forever, and its paid token simply lapses at
   the end of its grace window.

## 3. Adding models

### 3.1 The published THOX models (available now, on any computer)

The current THOX device models run anywhere Ollama runs — including
a ThoxOS Desktop Edition machine, and including a Mac or PC that has
never seen ThoxOS. One line each:

```
ollama run thox-ai/thoxair-0.5b        # ThoxAir flagship (smallest)
ollama run thox-ai/thoxedge-0.8b       # ThoxEdge
ollama run thox-ai/thoxmini-phi4mini   # ThoxMini flagship (largest)
ollama run thox-ai/thoxclip-qwen3-0.6b # ThoxClip
```

Pick by memory, not by name: the Air model (~0.4 GB download) suits
2 GB-class machines; the Mini model (~2.5 GB download) needs a
4 GB-class machine or better and will not fit the smallest devices —
the whitepaper's capacity section shows the arithmetic. On ThoxOS
itself, the portal's Models page adds the same models by name
(PENDING-VERIFY P3/P5 for the page flow on real images); the terminal
commands above work on ThoxOS exactly as written.

### 3.2 The ThoxOS kernel models (not yet)

The ThoxOS-Kernel family — **ThoxOS-Kernel-27B** (host tier),
**ThoxOS-Kernel-4B** (ThoxMini/ThoxClip), **ThoxOS-Kernel-0.8B**
(smallest devices) — is specialised for kernel and OS work and will
be the on-device OS agent when it ships. **Status: model cards are
published; no weights exist yet**, the student models' bases are not
final, and production waits on a teacher host. There is no download
command to give you today, and any page offering one is not us. When
the family releases, each model arrives through the same Models page
and `ollama run` route as section 3.1, with its evaluation results
published on its card first.

### 3.3 Your own models

Any GGUF model that fits your device's class can be added the same
way (`ollama pull`, or import a GGUF file). Premium THOX fine-tune
packs, when offered, are a paid add-on (`models.premium`) and plug
into the same Models page — buying one changes what is listed for
your account, never how models run.

## 4. Updating

1. **Automatic (default).** Devices check for updates, download the
   signed bundle, and install it into the idle system slot. On the
   next boot the new system must pass its health checks; if anything
   fails, the device **rolls back automatically** to the previous
   system. Your data partition is never touched by an update.
2. **Manual.** Portal → Updates → Check now. The same signed,
   health-gated, rollback-safe flow runs; only the timing is yours.
3. **What you will see.** The About panel shows the image version
   and which slot (A or B) is active; after a successful update the
   other slot is active. A failed update shows as "update rolled
   back" with the previous version still running — that is the
   system working as designed, not an error to fix.
4. **Subscriptions and updates.** Security updates are free and are
   never blocked by a lapsed plan. Paid fleet tooling (section 5)
   can schedule *when* a fleet is offered an update; it cannot change
   the on-device safety flow.

## 5. Where the paid add-ons plug in

All add-ons arrive the same way: your plan grants feature ids on
your entitlement token (section 2), and the corresponding service
appears in the portal. Nothing extra is installed on the device for
hosted features, and removing a plan removes the features at the end
of the grace window — nothing else changes.

| Add-on | Feature id | Where it shows up |
| --- | --- | --- |
| MeshStack remote access + relays | `meshstack.remote` | Portal → Mesh: reach your mesh from anywhere |
| MagStack Scheduler Pro + KV v2 | `meshstack.scheduler-pro` | Portal → Mesh: cross-device placement and KV sharing |
| ThoxRoute Cloud | `thoxroute.cloud` | Portal → Routing: hosted models and escalation when local devices are not enough |
| Managed backup | `backup.managed` | Portal → Backup: encrypted, THOX-operated backup |
| Premium models | `models.premium` | Portal → Models: premium fine-tune packs listed for your account |
| ThoxWork | `thoxwork` | The ThoxWork workspace, signed in with the same account |

The line that does not move: what runs entirely on your hardware and
your network is Core and stays free. What needs computers THOX
operates is what a plan pays for. Prices are published at thox.ai
with the release; they are not quoted in this document set.

## 6. If something is wrong

- **A paid feature is off but you paid:** check Portal → Services
  for the entitlement state. "Grace" means renew soon; "Expired"
  means renew. If it says Active and the feature is still off, sign
  out and back in once to refresh the token, then contact support.
- **A model will not load:** it almost always does not fit. Check
  the model size against your device's class (section 3.1) and pick
  the smaller model.
- **An update rolled back twice in a row:** leave the device on the
  working system and contact support with the version numbers from
  the About panel; do not attempt a manual flash for an update
  problem (flashing is a recovery tool — see the device install
  guide).
- **Everything else:** support, downloads, and advisories at
  **thox.ai**. Community support is free; plans add SLA support.

## License

This guide is CC BY 4.0.

© 2026 THOX.ai LLC. THOX, ThoxOS, ThoxAir, ThoxMini, ThoxClip,
ThoxEdge, and MeshStack are trademarks of THOX.ai LLC.
