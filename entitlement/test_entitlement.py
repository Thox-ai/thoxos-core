#!/usr/bin/env python3
"""Tests for the THOX entitlement reference implementation (ENT-01).

Run from this directory:

    python3 -m unittest
    python3 -m unittest test_entitlement -v

Every test injects its clock explicitly (fixed unix timestamps); no
test depends on real time.
"""

import base64
import json
import unittest

import thox_entitlement as ent

SECRET = "test-secret-not-a-real-credential"
WRONG_SECRET = "some-other-secret"

# Fixed clock for the whole suite.
T0 = 1_700_000_000
DAY = ent.SECONDS_PER_DAY


def issue(features=("meshstack.remote",), ttl_days=365, sub="acct_test", plan="plus"):
    return ent.issue_token(SECRET, sub, plan, list(features), ttl_days, now=T0)


def exp_of(token):
    payload_b64 = token.split(".")[1]
    raw = base64.urlsafe_b64decode(payload_b64 + "=" * (-len(payload_b64) % 4))
    return json.loads(raw)["exp"]


class RoundTripTests(unittest.TestCase):
    def test_issue_verify_round_trip(self):
        token = issue(features=("meshstack.remote", "thoxroute.cloud"))
        v = ent.verify_token(SECRET, token, now=T0)
        self.assertEqual(v.status, "valid")
        self.assertEqual(v.sub, "acct_test")
        self.assertEqual(v.plan, "plus")
        self.assertEqual(v.features, frozenset({"meshstack.remote", "thoxroute.cloud"}))
        self.assertEqual(v.iat, T0)
        self.assertEqual(v.exp, T0 + 365 * DAY)

    def test_token_shape_and_header(self):
        token = issue()
        parts = token.split(".")
        self.assertEqual(len(parts), 3)
        header = json.loads(
            base64.urlsafe_b64decode(parts[0] + "=" * (-len(parts[0]) % 4))
        )
        self.assertEqual(header, {"alg": "HS256", "typ": "THOX-ENT"})

    def test_clock_is_injected_not_real_time(self):
        # The same token verified at three injected moments must give the
        # three lifecycle states, deterministically and repeatably.
        token = issue(ttl_days=30)
        exp = exp_of(token)
        self.assertEqual(ent.verify_token(SECRET, token, now=T0).status, "valid")
        self.assertEqual(ent.verify_token(SECRET, token, now=exp + 1).status, "grace")
        self.assertEqual(
            ent.verify_token(SECRET, token, now=exp + 31 * DAY).status, "expired"
        )
        # Repeat: identical inputs, identical outputs.
        self.assertEqual(ent.verify_token(SECRET, token, now=T0).status, "valid")


class RejectionTests(unittest.TestCase):
    def test_tampered_payload_rejected(self):
        token = issue()
        header_b64, payload_b64, sig_b64 = token.split(".")
        payload = json.loads(
            base64.urlsafe_b64decode(payload_b64 + "=" * (-len(payload_b64) % 4))
        )
        payload["plan"] = "enterprise"  # attacker edits the claim, keeps old signature
        forged_payload = (
            base64.urlsafe_b64encode(
                json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
            )
            .rstrip(b"=")
            .decode()
        )
        forged = f"{header_b64}.{forged_payload}.{sig_b64}"
        v = ent.verify_token(SECRET, forged, now=T0)
        self.assertEqual(v.status, "invalid")
        self.assertEqual(v.features, frozenset())

    def test_wrong_secret_rejected(self):
        token = issue()
        v = ent.verify_token(WRONG_SECRET, token, now=T0)
        self.assertEqual(v.status, "invalid")

    def test_malformed_tokens_rejected(self):
        for bad in [
            "",
            "not-a-token",
            "only.two",
            "a.b.c.d",
            "..",
            "!!!.@@@.###",
            "e30.e30.e30",  # decodable JSON, wrong header/claims
        ]:
            with self.subTest(token=bad):
                v = ent.verify_token(SECRET, bad, now=T0)
                self.assertEqual(v.status, "invalid")

    def test_missing_token_is_invalid_not_an_exception(self):
        self.assertEqual(ent.verify_token(SECRET, None, now=T0).status, "invalid")
        self.assertEqual(ent.verify_token(SECRET, "", now=T0).status, "invalid")


class GraceWindowTests(unittest.TestCase):
    def setUp(self):
        self.token = issue(ttl_days=90)
        self.exp = exp_of(self.token)

    def test_valid_at_expiry_instant(self):
        v = ent.verify_token(SECRET, self.token, now=self.exp)
        self.assertEqual(v.status, "valid")

    def test_grace_at_exp_plus_29_days(self):
        v = ent.verify_token(SECRET, self.token, now=self.exp + 29 * DAY)
        self.assertEqual(v.status, "grace")

    def test_grace_at_exactly_exp_plus_30_days(self):
        v = ent.verify_token(SECRET, self.token, now=self.exp + 30 * DAY)
        self.assertEqual(v.status, "grace")
        self.assertGreaterEqual(v.grace_days_remaining, 0)

    def test_expired_at_exp_plus_31_days(self):
        v = ent.verify_token(SECRET, self.token, now=self.exp + 31 * DAY)
        self.assertEqual(v.status, "expired")

    def test_grace_reports_days_remaining(self):
        v = ent.verify_token(SECRET, self.token, now=self.exp + 15 * DAY)
        self.assertEqual(v.status, "grace")
        self.assertEqual(v.grace_days_remaining, 15)

    def test_paid_feature_allowed_in_grace(self):
        v = ent.verify_token(SECRET, self.token, now=self.exp + 10 * DAY)
        self.assertEqual(v.status, "grace")
        self.assertTrue(ent.check_feature(v, "meshstack.remote"))

    def test_paid_feature_denied_after_grace_lapses(self):
        v = ent.verify_token(SECRET, self.token, now=self.exp + 31 * DAY)
        self.assertEqual(v.status, "expired")
        self.assertFalse(ent.check_feature(v, "meshstack.remote"))


class FreeFeatureGuaranteeTests(unittest.TestCase):
    """The D4 guarantee: free Core features are NEVER gated."""

    def assert_all_free_allowed(self, verification):
        for feature in sorted(ent.FREE_FEATURES):
            with self.subTest(feature=feature):
                self.assertTrue(ent.check_feature(verification, feature))

    def test_free_features_cover_the_programme_list(self):
        self.assertEqual(
            ent.FREE_FEATURES,
            frozenset(
                {
                    "core-os",
                    "meshstack.local",
                    "local-ai",
                    "security-updates",
                    "thoxbeam.local",
                }
            ),
        )

    def test_free_allowed_with_no_token(self):
        self.assert_all_free_allowed(None)

    def test_free_allowed_with_expired_token(self):
        token = issue(ttl_days=1)
        v = ent.verify_token(SECRET, token, now=T0 + 40 * DAY)
        self.assertEqual(v.status, "expired")
        self.assert_all_free_allowed(v)

    def test_free_allowed_with_invalid_token(self):
        v = ent.verify_token(SECRET, "garbage.token.value", now=T0)
        self.assertEqual(v.status, "invalid")
        self.assert_all_free_allowed(v)

    def test_free_allowed_with_wrong_secret_token(self):
        token = issue()
        v = ent.verify_token(WRONG_SECRET, token, now=T0)
        self.assertEqual(v.status, "invalid")
        self.assert_all_free_allowed(v)


class PaidFeatureTests(unittest.TestCase):
    def test_paid_allowed_when_valid_and_listed(self):
        v = ent.verify_token(SECRET, issue(), now=T0)
        self.assertTrue(ent.check_feature(v, "meshstack.remote"))

    def test_paid_denied_when_not_in_feature_list(self):
        token = issue(features=("thoxroute.cloud",))
        v = ent.verify_token(SECRET, token, now=T0)
        self.assertEqual(v.status, "valid")
        self.assertFalse(ent.check_feature(v, "meshstack.remote"))
        self.assertTrue(ent.check_feature(v, "thoxroute.cloud"))

    def test_paid_denied_with_no_token(self):
        for feature in sorted(ent.PAID_FEATURES):
            with self.subTest(feature=feature):
                self.assertFalse(ent.check_feature(None, feature))

    def test_paid_denied_with_invalid_token(self):
        v = ent.verify_token(WRONG_SECRET, issue(), now=T0)
        self.assertFalse(ent.check_feature(v, "meshstack.remote"))

    def test_paid_catalogue_matches_programme(self):
        self.assertEqual(
            ent.PAID_FEATURES,
            frozenset(
                {
                    "meshstack.remote",
                    "meshstack.scheduler-pro",
                    "thoxroute.cloud",
                    "backup.managed",
                    "models.premium",
                    "thoxwork",
                }
            ),
        )

    def test_unknown_feature_denied(self):
        v = ent.verify_token(SECRET, issue(), now=T0)
        self.assertFalse(ent.check_feature(v, "no.such.feature"))


if __name__ == "__main__":
    unittest.main()
