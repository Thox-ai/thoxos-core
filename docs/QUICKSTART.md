# thoxos-core — Quickstart

Five minutes, tested commands only. Requires Python 3.10+ (standard
library only) for the code paths, and Ollama for the model path.

## 1. Get the code

```sh
git clone https://github.com/Thox-ai/thoxos-core.git
cd thoxos-core
```

Or download `thoxos-core-0.1.0.tar.gz` from the
[v0.1.0 release](https://github.com/Thox-ai/thoxos-core/releases/tag/v0.1.0)
and verify it against the published SHA-256 sidecar before extracting.

## 2. Run what runs today

```sh
cd entitlement/
python3 thox_entitlement.py demo     # end-to-end entitlement scenario
python3 -m unittest                  # 25 tests, expect OK
cd ..
python3 images/validate.py           # expect 27/27 checks pass
```

## 3. Run a THOX model

```sh
ollama run thox-ai/thoxair-0.5b
```

More models and sizing guidance: [RUN.md](RUN.md) section 3.

## 4. Next

- Full guide: [USER_GUIDE.md](USER_GUIDE.md)
- Install routes: [install/](install/)
- What is not built yet, in one register: [PENDING-VERIFY.md](PENDING-VERIFY.md)
