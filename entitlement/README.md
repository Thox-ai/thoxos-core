# THOX Entitlement — Reference Implementation (ENT-01)

A single-file, Python 3 standard-library-only implementation of the
ThoxOS entitlement contract, plus a CLI and a test suite. No third-party
dependencies.

**This is a reference implementation for the entitlement contract, not
production key management.** It demonstrates and pins down the token
format, the verification states, and the feature-gating rules so that
production implementations (in Core services and the THOX cloud) can be
checked against one shared contract. It deliberately contains no key
storage, no key rotation, no revocation infrastructure, and no secrets:
the signing secret is supplied by the caller (CLI flag or environment
variable), and the only secret value in the code is the clearly labeled
demo value used by the `demo` subcommand, which protects nothing.

## The rules it implements (decision D4)

1. **Signed offline token.** Entitlement is a JWT-shaped token —
   `base64url(header).base64url(payload).base64url(HMAC-SHA256)` with
   header `{"alg": "HS256", "typ": "THOX-ENT"}` — verified locally,
   with no network call.
2. **Server-side enforcement only.** Paid features live on
   THOX-operated services, and those services enforce entitlement.
   ThoxOS Core contains **no DRM and no kill switch**.
3. **30-day offline grace.** After a token expires, paid features keep
   working for 30 more days (status `grace`, with days remaining
   reported), so a device that cannot reach the renewal service is
   never cut off abruptly.
4. **Free features are never gated.** A lapsed, absent, or even invalid
   token must never disable free Core features. `check_feature()`
   returns `True` for free features before it ever looks at the token.

### Verification states

| Status    | Meaning                                             |
|-----------|-----------------------------------------------------|
| `valid`   | Signature good, `now <= exp`                        |
| `grace`   | Signature good, `exp < now <= exp + 30 days`        |
| `expired` | Signature good, `now > exp + 30 days`               |
| `invalid` | Bad signature, malformed token, or no token         |

Payload claims: `sub` (account id), `plan`, `features` (list of paid
feature ids), `iat`, `exp` (unix seconds).

### Feature catalogue

Free forever (never gated): `core-os`, `meshstack.local`, `local-ai`,
`security-updates`, `thoxbeam.local`.

Paid (token-granted): `meshstack.remote`, `meshstack.scheduler-pro`,
`thoxroute.cloud`, `backup.managed`, `models.premium`, `thoxwork`.

A paid feature is allowed only when the token status is `valid` or
`grace` **and** the feature is in the token's feature list. Unknown
feature ids are denied.

## Run the demo

```sh
python3 thox_entitlement.py demo
```

The demo runs a scripted, deterministic end-to-end scenario on a fixed
clock with the labeled demo secret: it issues a token, verifies it,
checks features, then simulates the grace period (exp + 15 days, paid
features still allowed) and a lapsed subscription (exp + 31 days, paid
features denied while every free feature stays allowed).

## Run the tests

```sh
cd entitlement/
python3 -m unittest            # or: python3 -m unittest test_entitlement -v
```

The suite covers the issue/verify round-trip, tampered-payload and
wrong-secret rejection, malformed tokens, the grace-window boundaries
(exp + 29d still grace, exp + 31d expired), paid features in grace and
denied when unlisted, and the D4 guarantee: free features allowed with
no token, with an expired token, and with an invalid token. All clocks
are injected; nothing depends on real time.

## CLI

The signing secret comes from `--secret` or the `THOX_ENT_SECRET`
environment variable. It is never hardcoded.

```sh
export THOX_ENT_SECRET='...'   # supplied by your own secret handling

# Issue (prints the token)
python3 thox_entitlement.py issue --sub acct_123 --plan plus \
    --features meshstack.remote,thoxroute.cloud --ttl-days 365

# Verify (prints JSON: status, claims, feature set)
python3 thox_entitlement.py verify --token <TOKEN>

# Check one feature (prints allowed/denied + reason; exit 0/1)
python3 thox_entitlement.py check --token <TOKEN> --feature meshstack.remote
python3 thox_entitlement.py check --feature core-os        # no token needed
```

## Library use

```python
from thox_entitlement import issue_token, verify_token, check_feature

token = issue_token(secret, "acct_123", "plus", ["meshstack.remote"], ttl_days=365)
v = verify_token(secret, token, now=some_unix_time)
check_feature(v, "meshstack.remote")   # True while valid/in grace
check_feature(None, "core-os")         # True, always
```
