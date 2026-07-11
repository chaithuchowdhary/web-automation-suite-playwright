"""
Test credentials, read from environment variables.

Locally: copy .env.example to .env and fill in real values (.env is git-ignored).
In CI: values come from GitHub Actions secrets - see .github/workflows/main.yml.

Nothing secret lives in this file, so it is safe to commit.
"""

import os

from dotenv import load_dotenv

# Local convenience only. Real environment variables take precedence over .env,
# so CI (which has no .env file) is unaffected.
load_dotenv(override=False)


def _required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable {name!r}. "
            "Copy .env.example to .env and fill it in (locally), or add it as a "
            "repository secret (in CI)."
        )
    return value


# Account used by test_login.py, test_checkout.py and test_end_to_end.py.
# Must already be registered on https://www.automationexercise.com
EMAIL = _required("EMAIL")
PASSWORD = _required("PASSWORD")

# Dummy payment card details used by test_checkout.py and test_end_to_end.py.
# automationexercise.com's payment form is a sandbox - it never charges a real
# card - but these stay out of source control regardless.
CARD_NAME = _required("CARD_NAME")
CARD_NUMBER = _required("CARD_NUMBER")
CARD_CVC = _required("CARD_CVC")
CARD_EXPIRY_MONTH = _required("CARD_EXPIRY_MONTH")
CARD_EXPIRY_YEAR = _required("CARD_EXPIRY_YEAR")
