import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage

from testdata.credentials import EMAIL, PASSWORD

# Real ad/analytics domains observed live on automationexercise.com. Google's
# full-page "vignette" interstitial (loaded from these domains) can cover the
# checkout/payment form and block every locator on the page, so these are
# blocked for every test - this also makes the whole suite faster and more
# stable, not just checkout.
AD_BLOCK_PATTERNS = [
    "**/*googlesyndication.com/**",
    "**/*doubleclick.net/**",
    "**/*googleadservices.com/**",
    "**/*google.com/pagead/**",
    "**/*fundingchoicesmessages.google.com/**",
    "**/*adtrafficquality.google/**",
    "**/*google-analytics.com/**",
    "**/*googletagmanager.com/**",
]


@pytest.fixture(autouse=True)
def block_ads(page):
    for pattern in AD_BLOCK_PATTERNS:
        page.route(pattern, lambda route: route.abort())
    yield


@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def products_page(page):
    return ProductsPage(page)


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@pytest.fixture
def checkout_page(page):
    return CheckoutPage(page)


@pytest.fixture
def logged_in_page(page, login_page):
    """A page already authenticated with the credentials from the environment."""
    login_page.open()
    login_page.login(EMAIL, PASSWORD)
    return page
