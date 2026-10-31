#!/usr/bin/env python3
"""THOX entitlement reference implementation (ticket ENT-01).

Implements decision D4 of the ThoxOS Open Source programme:

  * Entitlement is a signed, offline-verifiable token (JWT-shaped).
  * Verification happens locally; paid features are enforced server-side
    only on THOX-operated services. There is NO DRM and NO kill switch
    in ThoxOS Core.
  * A token gets a 30-day offline grace period after it expires.
  * A lapsed, absent, or invalid token must NEVER disable free Core
    features. Free features are not gated by this module at all in
    practice: ``check_feature`` returns True for them unconditionally.

Token format (three base64url segments, dot-separated)::

    base64url(header) "." base64url(payload) "." base64url(signature)

  header    = {"alg": "HS256", "typ": "THOX-ENT"}
  payload   = {"sub": <account id>, "plan": <plan name>,
               "features": [<feature id>, ...],
               "iat": <issued-at, unix seconds>, "exp": <expiry, unix seconds>}
  signature = HMAC-SHA256(secret, header_b64 + "." + payload_b64)

This is a REFERENCE IMPLEMENTATION of the entitlement contract, written
with the Python 3 standard library only. It is not production key
management: there is no key storage, rotation, revocation list, or
hardware binding here, by design.

Usage (secret via --secret or the THOX_ENT_SECRET environment variable):

    python3 thox_entitlement.py issue --sub acct_123 --plan plus \
        --features meshstack.remote,thoxroute.cloud --ttl-days 365
    python3 thox_entitlement.py verify --token <TOKEN>
    python3 thox_entitlement.py check --token <TOKEN> --feature meshstack.remote
    python3 thox_entitlement.py demo
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import math
import os
import sys
import time
from dataclasses import dataclass, field
from typing import Iterable, Optional, Sequence, Union

# --------------------------------------------------------------------------
# Feature catalogue (programme of record)
# --------------------------------------------------------------------------

#: Features that are free forever in ThoxOS Core. They are NEVER gated:
#: check_feature() returns True for them regardless of token state,
#: including no token at all and an invalid token.
FREE_FEATURES = frozenset(
    {
        "core-os",
        "meshstack.local",
        "local-ai",
        "security-updates",
        "thoxbeam.local",
    }
)

#: Features provided by THOX-operated services; these are the only ones
#: an entitlement token can grant.
PAID_FEATURES = frozenset(
    {
        "meshstack.remote",
        "meshstack.scheduler-pro",
        "thoxroute.cloud",
        "backup.managed",
        "models.premium",
        "thoxwork",
    }
)

ALL_FEATURES = FREE_FEATURES | PAID_FEATURES

#: Offline grace period after token expiry (decision D4): 30 days.
GRACE_SECONDS = 30 * 24 * 60 * 60

SECONDS_PER_DAY = 24 * 60 * 60

HEADER = {"alg": "HS256", "typ": "THOX-ENT"}

#: Clearly-labeled demo-only secret, used solely by the `demo` subcommand.
#: It is not a real credential and must never protect anything real.
DEMO_SECRET = "demo-secret-NOT-FOR-PRODUCTION"

SecretLike = Union[str, bytes]


# --------------------------------------------------------------------------
# Encoding helpers
# --------------------------------------------------------------------------


def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _b64url_decode(segment: str) -> bytes:
    if not isinstance(segment, str):
        raise ValueError("token segment is not text")
    padding = "=" * (-len(segment) % 4)
    return base64.urlsafe_b64decode(segment + padding)


def _canonical_json(obj) -> bytes:
    return json.dumps(obj, separators=(",", ":"), sort_keys=True).encode("utf-8")


def _secret_bytes(secret: SecretLike) -> bytes:
    if isinstance(secret, bytes):
        return secret
    if isinstance(secret, str):
        return secret.encode("utf-8")
    raise ValueError("a signing secret is required (str or bytes)")


def _sign(secret: SecretLike, signing_input: bytes) -> bytes:
    return hmac.new(_secret_bytes(secret), signing_input, hashlib.sha256).digest()


# --------------------------------------------------------------------------
# Verification result
# --------------------------------------------------------------------------

STATUS_VALID = "valid"
STATUS_GRACE = "grace"
STATUS_EXPIRED = "expired"
STATUS_INVALID = "invalid"


@dataclass(frozen=True)
class Verification:
    """Result of verifying a token at a given moment.

    status: one of "valid", "grace", "expired", "invalid".
      valid   -- signature good and now <= exp
      grace   -- signature good and exp < now <= exp + 30 days
      expired -- signature good and now > exp + 30 days
      invalid -- bad signature, malformed token, or no token at all
    features: the paid feature set carried by the token (empty when the
      token is invalid or absent). Free features are never listed here;
      they are unconditional.
    grace_days_remaining: whole days of grace left (ceiling), set only
      when status == "grace".
    """

    status: str
    features: frozenset = frozenset()
    sub: Optional[str] = None
    plan: Optional[str] = None
    iat: Optional[int] = None
    exp: Optional[int] = None
    now: Optional[float] = None
    grace_days_remaining: Optional[int] = None
    reason: str = ""

    @property
    def paid_features_active(self) -> bool:
        """True when paid features may be used (valid or in grace)."""
        return self.status in (STATUS_VALID, STATUS_GRACE)

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "sub": self.sub,
            "plan": self.plan,
            "features": sorted(self.features),
            "iat": self.iat,
            "exp": self.exp,
            "now": self.now,
            "grace_days_remaining": self.grace_days_remaining,
            "reason": self.reason,
        }


# --------------------------------------------------------------------------
# Issue / verify
# --------------------------------------------------------------------------


def issue_token(
    secret: SecretLike,
    sub: str,
    plan: str,
    features: Iterable[str],
    ttl_days: float,
    now: Optional[float] = None,
) -> str:
    """Issue a signed entitlement token.

    ``now`` is injectable for tests and demos; it defaults to the
    current time. ``iat`` is int(now) and ``exp`` is iat + ttl_days.
    """
    if now is None:
        now = time.time()
    iat = int(now)
    exp = iat + int(ttl_days * SECONDS_PER_DAY)
    payload = {
        "sub": sub,
        "plan": plan,
        "features": sorted(set(features)),
        "iat": iat,
        "exp": exp,
    }
    header_b64 = _b64url_encode(_canonical_json(HEADER))
    payload_b64 = _b64url_encode(_canonical_json(payload))
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    signature_b64 = _b64url_encode(_sign(secret, signing_input))
    return f"{header_b64}.{payload_b64}.{signature_b64}"


def _invalid(now, reason: str) -> Verification:
    return Verification(status=STATUS_INVALID, now=now, reason=reason)


def verify_token(
    secret: SecretLike, token: Optional[str], now: Optional[float] = None
) -> Verification:
    """Verify ``token`` at moment ``now`` (unix seconds, injectable).

    Never raises for a bad token: malformed input, a bad signature, or
    a missing token all return status "invalid". (A missing *secret*
    does raise ValueError; that is a caller bug, not a token state.)
    """
    if now is None:
        now = time.time()

    if not token or not isinstance(token, str):
        return _invalid(now, "no token presented")

    parts = token.split(".")
    if len(parts) != 3:
        return _invalid(now, "malformed token: expected 3 segments")
    header_b64, payload_b64, signature_b64 = parts

    try:
        header = json.loads(_b64url_decode(header_b64))
        payload = json.loads(_b64url_decode(payload_b64))
        presented_sig = _b64url_decode(signature_b64)
    except Exception:
        return _invalid(now, "malformed token: undecodable segment")

    if not isinstance(header, dict) or header.get("alg") != "HS256" or header.get("typ") != "THOX-ENT":
        return _invalid(now, "unexpected token header")
    if not isinstance(payload, dict):
        return _invalid(now, "malformed token: payload is not an object")

    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    expected_sig = _sign(secret, signing_input)
    if not hmac.compare_digest(expected_sig, presented_sig):
        return _invalid(now, "bad signature")

    # Signature is good from here on; validate the claims we rely on.
    try:
        exp = int(payload["exp"])
        iat = int(payload["iat"])
    except (KeyError, TypeError, ValueError):
        return _invalid(now, "malformed token: missing/invalid iat or exp")
    features = payload.get("features") or []
    if not isinstance(features, list) or not all(isinstance(f, str) for f in features):
        return _invalid(now, "malformed token: features is not a list of strings")

    base = dict(
        features=frozenset(features),
        sub=payload.get("sub"),
        plan=payload.get("plan"),
        iat=iat,
        exp=exp,
        now=now,
    )

    if now <= exp:
        return Verification(status=STATUS_VALID, reason="token valid", **base)
    if now <= exp + GRACE_SECONDS:
        remaining = exp + GRACE_SECONDS - now
        return Verification(
            status=STATUS_GRACE,
            grace_days_remaining=math.ceil(remaining / SECONDS_PER_DAY),
            reason="token expired but inside the 30-day offline grace period",
            **base,
        )
    return Verification(
        status=STATUS_EXPIRED,
        reason="token expired and the 30-day grace period has lapsed",
        **base,
    )


# --------------------------------------------------------------------------
# Feature checks -- the heart of D4
# --------------------------------------------------------------------------


def feature_access(
    verification: Optional[Verification], feature: str
) -> tuple:
    """Return (allowed: bool, reason: str) for ``feature``.

    Free features are ALWAYS allowed, with any verification state --
    including verification=None (no token), an invalid token, and an
    expired token. This is the no-kill-switch guarantee of D4, enforced
    here by checking the free list before looking at the token at all.

    Paid features are allowed only when the token status is valid or
    grace AND the feature is in the token's feature list.
    Unknown feature ids are denied (fail closed for anything not in the
    free catalogue).
    """
    if feature in FREE_FEATURES:
        return True, "free Core feature: never gated by entitlement"

    if feature not in PAID_FEATURES:
        return False, f"unknown feature id: {feature}"

    if verification is None:
        return False, "paid feature requires an entitlement token (none presented)"
    if verification.status == STATUS_INVALID:
        return False, f"paid feature requires a valid token (token invalid: {verification.reason})"
    if verification.status == STATUS_EXPIRED:
        return False, "paid feature unavailable: subscription lapsed beyond the grace period"
    # status is valid or grace
    if feature not in verification.features:
        return False, f"feature {feature} is not in the token's feature list"
    if verification.status == STATUS_GRACE:
        return (
            True,
            f"feature granted by token, in grace period "
            f"({verification.grace_days_remaining} day(s) of grace remaining)",
        )
    return True, "feature granted by valid token"


def check_feature(verification: Optional[Verification], feature: str) -> bool:
    """True if ``feature`` may be used under ``verification``.

    Free features always return True. See feature_access() for the
    full rule set and human-readable reasons.
    """
    allowed, _ = feature_access(verification, feature)
    return allowed


# --------------------------------------------------------------------------
# Demo (scripted end-to-end scenario, fixed clock, demo secret)
# --------------------------------------------------------------------------


def run_demo(out=None) -> int:
    out = out or sys.stdout

    def say(text=""):
        print(text, file=out)

    demo_features = ["meshstack.remote", "thoxroute.cloud"]
    base_now = 1_700_000_000  # fixed clock: the demo is deterministic

    say("=== THOX entitlement demo (reference implementation, ENT-01) ===")
    say(f"Demo secret: {DEMO_SECRET!r} (demo only, protects nothing)")
    say("")

    say("Stage 1: issue a token (plan=plus, ttl=365 days)")
    token = issue_token(DEMO_SECRET, "acct_demo", "plus", demo_features, 365, now=base_now)
    say(f"  token: {token}")
    payload = json.loads(_b64url_decode(token.split(".")[1]))
    exp = payload["exp"]
    say(f"  claims: sub={payload['sub']} plan={payload['plan']} "
        f"features={payload['features']} iat={payload['iat']} exp={exp}")
    say("")

    say("Stage 2: verify at issue time and check features")
    v = verify_token(DEMO_SECRET, token, now=base_now)
    say(f"  status: {v.status}")
    for feature in ["meshstack.remote", "core-os"]:
        allowed, reason = feature_access(v, feature)
        say(f"  check {feature}: {'allowed' if allowed else 'denied'} ({reason})")
    say("")

    say("Stage 3: simulated grace (now = exp + 15 days)")
    v = verify_token(DEMO_SECRET, token, now=exp + 15 * SECONDS_PER_DAY)
    say(f"  status: {v.status} (grace days remaining: {v.grace_days_remaining})")
    allowed, reason = feature_access(v, "meshstack.remote")
    say(f"  check meshstack.remote: {'allowed' if allowed else 'denied'} ({reason})")
    say("")

    say("Stage 4: simulated lapse (now = exp + 31 days)")
    v = verify_token(DEMO_SECRET, token, now=exp + 31 * SECONDS_PER_DAY)
    say(f"  status: {v.status}")
    allowed, reason = feature_access(v, "meshstack.remote")
    say(f"  check meshstack.remote: {'allowed' if allowed else 'denied'} ({reason})")
    say("  ...and every free Core feature still works (the D4 guarantee):")
    all_free_ok = True
    for feature in sorted(FREE_FEATURES):
        allowed, reason = feature_access(v, feature)
        all_free_ok = all_free_ok and allowed
        say(f"  check {feature}: {'allowed' if allowed else 'denied'} ({reason})")
    say("")
    say("Stage 5: no token at all")
    allowed, reason = feature_access(None, "core-os")
    say(f"  check core-os (no token): {'allowed' if allowed else 'denied'} ({reason})")
    allowed, reason = feature_access(None, "meshstack.remote")
    say(f"  check meshstack.remote (no token): {'allowed' if allowed else 'denied'} ({reason})")
    say("")
    say("Demo complete: paid features follow the token; free Core never does.")
    return 0 if all_free_ok else 1


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def _resolve_secret(args) -> Optional[str]:
    return getattr(args, "secret", None) or os.environ.get("THOX_ENT_SECRET")


def _require_secret(args) -> str:
    secret = _resolve_secret(args)
    if not secret:
        print(
            "error: no signing secret. Pass --secret or set THOX_ENT_SECRET.",
            file=sys.stderr,
        )
        raise SystemExit(2)
    return secret


def _parse_features(text: Optional[str]) -> list:
    if not text:
        return []
    return [f.strip() for f in text.split(",") if f.strip()]


def main(argv: Optional[Sequence[str]] = None) -> int:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--secret",
        default=argparse.SUPPRESS,
        help="signing secret (default: THOX_ENT_SECRET env var)",
    )

    parser = argparse.ArgumentParser(
        prog="thox_entitlement",
        description="THOX entitlement reference implementation (ENT-01, decision D4).",
    )
    parser.add_argument(
        "--secret",
        default=None,
        help="signing secret (default: THOX_ENT_SECRET env var)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_issue = sub.add_parser("issue", parents=[common], help="issue a token and print it")
    p_issue.add_argument("--sub", required=True, help="account id (sub claim)")
    p_issue.add_argument("--plan", default="plus", help="plan name (default: plus)")
    p_issue.add_argument(
        "--features",
        default="",
        help="comma-separated paid feature ids to grant",
    )
    p_issue.add_argument("--ttl-days", type=float, default=365, help="token lifetime in days")

    p_verify = sub.add_parser("verify", parents=[common], help="verify a token, print JSON")
    p_verify.add_argument("--token", required=True, help="the token to verify")

    p_check = sub.add_parser(
        "check", parents=[common], help="check one feature; exit 0 allowed, 1 denied"
    )
    p_check.add_argument("--token", default=None, help="the token to check (optional)")
    p_check.add_argument("--feature", required=True, help="feature id to check")

    sub.add_parser("demo", parents=[common], help="run the scripted end-to-end demo")

    args = parser.parse_args(argv)

    if args.command == "demo":
        return run_demo()

    if args.command == "issue":
        secret = _require_secret(args)
        token = issue_token(
            secret,
            args.sub,
            args.plan,
            _parse_features(args.features),
            args.ttl_days,
        )
        print(token)
        return 0

    if args.command == "verify":
        secret = _require_secret(args)
        result = verify_token(secret, args.token)
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
        return 0

    if args.command == "check":
        verification = None
        if args.token:
            secret = _require_secret(args)
            verification = verify_token(secret, args.token)
        allowed, reason = feature_access(verification, args.feature)
        print(f"{'allowed' if allowed else 'denied'}: {args.feature} ({reason})")
        return 0 if allowed else 1

    parser.error(f"unknown command {args.command!r}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
