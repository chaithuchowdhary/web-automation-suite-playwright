import pytest
from playwright.sync_api import expect


@pytest.mark.parametrize("term", ["top", "dress", "jeans", "tshirt", "saree"])
def test_search_returns_results(products_page, term):
    products_page.open()
    products_page.search(term)

    expect(products_page.results_heading).to_be_visible()
    expect(products_page.product_cards.first).to_be_visible()
    assert products_page.product_cards.count() > 0


def test_search_nonsense_term_returns_no_results(products_page):
    products_page.open()
    products_page.search("zzzznonexistentproduct123")

    expect(products_page.results_heading).to_be_visible()
    assert products_page.product_cards.count() == 0
