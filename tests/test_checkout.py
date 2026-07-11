import pytest

from testdata.credentials import (
    CARD_CVC,
    CARD_EXPIRY_MONTH,
    CARD_EXPIRY_YEAR,
    CARD_NAME,
    CARD_NUMBER,
)

# The logged-in tests below share one account's server-side cart. Pin them
# to a single xdist worker so they run sequentially instead of racing each
# other's cart contents when the suite is run with -n auto.
pytestmark = pytest.mark.xdist_group(name="shared_account_cart")


def test_checkout_requires_login(products_page, cart_page, checkout_page):
    products_page.open()
    products_page.add_first_n_to_cart(1)

    cart_page.open()
    cart_page.proceed_to_checkout()

    assert checkout_page.requires_login()


def test_order_review_shows_the_item(
    logged_in_page, products_page, cart_page, checkout_page
):
    cart_page.clear()

    products_page.open()
    name = products_page.product_names_list()[0]
    products_page.add_first_n_to_cart(1)

    cart_page.open()
    cart_page.proceed_to_checkout()

    assert checkout_page.review_item_names() == [name]


def test_order_confirmation_appears(
    logged_in_page, products_page, cart_page, checkout_page
):
    cart_page.clear()

    products_page.open()
    products_page.add_first_n_to_cart(1)

    cart_page.open()
    cart_page.proceed_to_checkout()
    checkout_page.place_order()
    checkout_page.pay_with_dummy_card(
        CARD_NAME, CARD_NUMBER, CARD_CVC, CARD_EXPIRY_MONTH, CARD_EXPIRY_YEAR
    )

    checkout_page.expect_order_confirmed()
