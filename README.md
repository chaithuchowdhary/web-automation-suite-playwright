# Web Automation Suite - automationexercise.com

Cross-browser UI test automation for [automationexercise.com](https://www.automationexercise.com),
built with Playwright, Python and Pytest using the Page Object Model.

## Tech stack

- **Playwright (Python)** - browser automation with built-in auto-waiting (no manual sleeps)
- **Pytest** - test runner and assertions
- **pytest-playwright** - wires Playwright fixtures (`page`, `browser`, `--browser`, `base_url`, tracing/video/screenshot flags) into Pytest
- **pytest-xdist** - parallel test execution (`-n auto`)

## Project structure

```
pages/            Page Object Model classes (BasePage, LoginPage, ProductsPage, CartPage, CheckoutPage)
tests/            Test suites + conftest.py (shared page-object fixtures)
testdata/         Test data (credentials.py is git-ignored; credentials_example.py is the template)
reports/          Reserved for HTML/other custom test reports
pytest.ini        base_url, failure-only screenshot/trace/video, xdist grouping
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install playwright pytest-playwright pytest-xdist
playwright install chromium firefox webkit
```

Copy the credentials template and fill in a real, already-registered
automationexercise.com account plus dummy card details:

```bash
cp testdata/credentials_example.py testdata/credentials.py
```

`testdata/credentials.py` is git-ignored so personal credentials never get committed.

## What the tests cover

| File | Coverage |
|---|---|
| `test_smoke.py` | Home page loads, title contains "Automation Exercise" |
| `test_login.py` | Valid login, wrong-password error message, logout |
| `test_search.py` | Parametrized search across several terms (top, dress, jeans, tshirt, saree) asserting results appear; a nonsense term asserting zero results |
| `test_cart.py` | Add one product, add multiple products, verify name/price shown in cart, remove an item and confirm the count updates |
| `test_checkout.py` | Checkout redirects to login when logged out, the review step shows the item added, placing an order with a dummy card shows "Order Placed!" |
| `test_end_to_end.py` | One full journey: login -> search -> add to cart -> view cart -> checkout -> dummy payment -> confirmation |
| `test_api_mocking.py` | Playwright `page.route` network interception: (1) mocks the site's real `/api/productsList` JSON endpoint with fake data and asserts it's rendered, (2) aborts that same request to simulate a dead backend and asserts the page fails fast instead of hanging, (3) blocks real ad/analytics domains (`googlesyndication`, `doubleclick`, `fundingchoicesmessages`, `adtrafficquality`) observed on the live site and asserts the page still renders |

`test_checkout.py` and `test_end_to_end.py` log into the **same** test
account, which shares one server-side cart. They're tagged with
`@pytest.mark.xdist_group` (module-level `pytestmark`) so `-n auto` always
runs them on one worker instead of racing each other's cart contents;
`CartPage.clear()` also resets the cart at the start of each of those tests.

**21 tests total**, runnable across **3 browser engines** (Chromium, Firefox, WebKit) with one command each, or all three in one invocation.

## Running the tests

Run everything on the default browser (Chromium):

```bash
pytest
```

Run cross-browser, all three engines in one command:

```bash
pytest --browser chromium --browser firefox --browser webkit
```

Run in parallel:

```bash
pytest -n auto
```

Run cross-browser AND in parallel together:

```bash
pytest --browser chromium --browser firefox --browser webkit -n auto
```

## Debugging failures: screenshots, video, traces

`pytest.ini` enables screenshot/video/trace capture **only on failure**:

```ini
addopts = --screenshot=only-on-failure --tracing=retain-on-failure --video=retain-on-failure --output=test-results
```

On a failing test, artifacts land under `test-results/<test-name>/`:

```
test-results/tests-test-cart-py-test-add-single-product-to-cart-chromium/
├── test-failed-1.png
├── video.webm
└── trace.zip
```

Open a saved trace with Playwright's trace viewer:

```bash
playwright show-trace test-results/<test-folder>/trace.zip
```

## Exact commands

```bash
# Run all tests on one browser (Chromium)
pytest

# Run across all three engines in one command
pytest --browser chromium --browser firefox --browser webkit

# Run in parallel
pytest -n auto

# Run cross-browser AND parallel together
pytest --browser chromium --browser firefox --browser webkit -n auto

# Open a saved trace
playwright show-trace test-results/<test-folder>/trace.zip
```

## Notes

- automationexercise.com is a live public practice site loaded with real ad
  network scripts (Google Ad Manager, Funding Choices, etc.), including a
  full-page "vignette" interstitial that can cover the checkout/payment form
  and block every locator on the page. An autouse `block_ads` fixture in
  `tests/conftest.py` blocks those domains (googlesyndication, doubleclick,
  googleadservices, fundingchoicesmessages, adtrafficquality,
  google-analytics, googletagmanager) for **every** test, which also makes
  the whole suite noticeably faster. `test_api_mocking.py`'s third test
  verifies this blocking explicitly.
- The Page Object classes use only Playwright locators (`get_by_role`,
  `get_by_placeholder`, `page.locator` with the site's `data-qa` attributes)
  and Playwright's built-in auto-waiting (`expect(...).to_be_visible()`,
  action auto-wait on `.click()`/`.fill()`) - there are no manual
  `time.sleep()` or fixed waits anywhere in the suite.
