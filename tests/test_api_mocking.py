"""
Playwright network interception (page.route) demos.

automationexercise.com's own pages (home, /products, ...) are rendered
server-side and don't fetch product data over an in-page JSON call, so
there is nothing client-side to mock on those pages directly. To still
demonstrate mocking/aborting a *real* JSON API of the target site, these
tests target https://www.automationexercise.com/api/productsList - a real,
public JSON endpoint the site exposes - and drive it the same way a page
would: by requesting it and inspecting what the browser renders.

The third test blocks real ad/analytics domains observed on the live
/products page (googlesyndication, doubleclick, fundingchoices,
adtrafficquality, ...). The same domains are also blocked for every test via
the autouse `block_ads` fixture in conftest.py - this test demonstrates and
verifies that blocking mechanism explicitly.
"""

import json
import time

import pytest
from playwright.sync_api import expect

from tests.conftest import AD_BLOCK_PATTERNS

PRODUCTS_API_URL = "**/api/productsList"
PRODUCTS_API_PAGE = "/api/productsList"


def test_mocked_api_response_is_rendered(page):
    fake_payload = {
        "responseCode": 200,
        "products": [
            {
                "id": 9999,
                "name": "Mocked Test Product",
                "price": "Rs. 1",
                "brand": "PytestBrand",
                "category": {
                    "usertype": {"usertype": "Women"},
                    "category": "Mocked",
                },
            }
        ],
    }

    def fulfill_with_fake_data(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(fake_payload),
        )

    page.route(PRODUCTS_API_URL, fulfill_with_fake_data)
    page.goto(PRODUCTS_API_PAGE)

    expect(page.locator("body")).to_contain_text("Mocked Test Product")
    expect(page.locator("body")).to_contain_text("PytestBrand")


def test_blocked_api_fails_fast_instead_of_hanging(page):
    page.route(PRODUCTS_API_URL, lambda route: route.abort("failed"))

    started_at = time.monotonic()
    with pytest.raises(Exception):
        page.goto(PRODUCTS_API_PAGE, timeout=10_000)
    elapsed = time.monotonic() - started_at

    # A gracefully-failing backend errors out almost immediately - it must
    # not silently hang until the full navigation timeout is reached.
    assert elapsed < 9


def test_blocking_ad_and_analytics_requests_speeds_up_page(page):
    blocked_requests: list[str] = []

    def block_and_record(route):
        blocked_requests.append(route.request.url)
        route.abort()

    # page already has the autouse block_ads routes registered (added during
    # fixture setup, before this test body ran). Registering the same
    # patterns again here takes priority - Playwright tries the
    # most-recently-added matching handler first - so this handler records
    # the URL and aborts before the fixture's handler ever runs.
    for pattern in AD_BLOCK_PATTERNS:
        page.route(pattern, block_and_record)

    page.goto("/products")
    expect(page.get_by_role("heading", name="All Products")).to_be_visible()

    ad_markers = (
        "googlesyndication",
        "doubleclick",
        "googleadservices",
        "google.com/pagead",
        "fundingchoicesmessages",
        "adtrafficquality",
        "google-analytics",
        "googletagmanager",
    )
    assert blocked_requests, "expected at least one ad/analytics request to be blocked"
    assert all(any(marker in url for marker in ad_markers) for url in blocked_requests)
