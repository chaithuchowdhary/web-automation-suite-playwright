from playwright.sync_api import expect


def test_add_single_product_to_cart(products_page, cart_page):
    products_page.open()
    name = products_page.product_names_list()[0]
    products_page.add_first_n_to_cart(1)

    cart_page.open()
    assert cart_page.item_count() == 1
    assert cart_page.item_names() == [name]


def test_add_multiple_products_to_cart(products_page, cart_page):
    products_page.open()
    names = products_page.product_names_list()[:3]
    products_page.add_first_n_to_cart(3)

    cart_page.open()
    assert cart_page.item_count() == 3
    assert cart_page.item_names() == names


def test_cart_shows_correct_name_and_price(products_page, cart_page):
    products_page.open()
    name = products_page.product_names_list()[0]
    products_page.add_first_n_to_cart(1)

    cart_page.open()
    assert cart_page.item_names() == [name]
    assert cart_page.item_prices()[0].startswith("Rs.")


def test_remove_item_updates_cart_count(products_page, cart_page):
    products_page.open()
    names = products_page.product_names_list()[:2]
    products_page.add_first_n_to_cart(2)

    cart_page.open()
    assert cart_page.item_count() == 2

    cart_page.remove_item(names[0])
    expect(cart_page.cart_rows).to_have_count(1)
    assert cart_page.item_names() == [names[1]]
