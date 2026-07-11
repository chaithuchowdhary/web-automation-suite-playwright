"""
Template for testdata/credentials.py.

Copy this file to testdata/credentials.py and fill in real values.
testdata/credentials.py is git-ignored so your personal/test credentials
never get committed.
"""

# Account used by test_login.py, test_checkout.py and test_end_to_end.py.
# Must already be registered on https://www.automationexercise.com
EMAIL = "your_email@example.com"
PASSWORD = "your_password"

# Dummy payment card details used by test_checkout.py and test_end_to_end.py.
# automationexercise.com's payment form is a sandbox - it never charges a
# real card - but keep these out of source control regardless.
CARD_NAME = "Test User"
CARD_NUMBER = "4111111111111111"
CARD_CVC = "123"
CARD_EXPIRY_MONTH = "12"
CARD_EXPIRY_YEAR = "2030"
