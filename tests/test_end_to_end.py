import pytest

from testdata.credentials import (
    CARD_CVC,
    CARD_EXPIRY_MONTH,
    CARD_EXPIRY_YEAR,
    CARD_NAME,
    CARD_NUMBER,
)

# Shares the same account/cart as test_checkout.py - keep it on the same
# xdist worker/group so the two files never mutate the cart concurrently.
pytestmark = pytest.mark.xdist_group(name="shared_account_cart")


def test_full_purchase_journey(
    logged_in_page, login_page, products_page, cart_page, checkout_page
):
    # 1. Login (via the logged_in_page fixture).
    assert login_page.is_logged_in()
    cart_page.clear()

    # 2. Search for a product.
    products_page.open()
    products_page.search("dress")
    name = products_page.product_names_list()[0]

    # 3. Add it to the cart and go straight to the cart from the modal.
    products_page.add_to_cart(0)
    products_page.go_to_cart_from_modal()
    assert cart_page.item_names() == [name]

    # 4. Checkout and pay with a dummy card.
    cart_page.proceed_to_checkout()
    checkout_page.place_order()
    checkout_page.pay_with_dummy_card(
        CARD_NAME, CARD_NUMBER, CARD_CVC, CARD_EXPIRY_MONTH, CARD_EXPIRY_YEAR
    )

    # 5. Confirm the order was placed.
    checkout_page.expect_order_confirmed()
