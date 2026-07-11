from playwright.sync_api import Page

from pages.base_page import BasePage


class ProductsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.search_input = page.locator("#search_product")
        self.search_button = page.locator("#submit_search")
        self.results_heading = page.get_by_role("heading", name="Searched Products")
        self.product_cards = page.locator(".product-image-wrapper")
        self.product_names = page.locator(".productinfo p")
        self.cart_modal = page.locator("#cartModal")
        self.continue_shopping_button = page.locator(".close-modal")
        self.view_cart_link = page.locator("#cartModal").get_by_role("link", name="View Cart")

    def open(self):
        self.goto("/products")
        return self

    def search(self, term: str):
        self.search_input.fill(term)
        self.search_button.click()
        return self

    def product_names_list(self) -> list[str]:
        return [self.normalize_text(t) for t in self.product_names.all_inner_texts()]

    def add_to_cart_by_name(self, name: str):
        card = self.page.locator(".product-image-wrapper").filter(has_text=name)
        card.locator(".add-to-cart").first.click()
        return self

    def add_to_cart(self, index: int = 0):
        """Click "Add to cart" for the nth product card, leaving the modal open."""
        self.product_cards.nth(index).locator(".add-to-cart").first.click()
        return self

    def add_first_n_to_cart(self, count: int):
        for index in range(count):
            self.product_cards.nth(index).locator(".add-to-cart").first.click()
            self.continue_shopping_button.click()
        return self

    def dismiss_cart_modal(self):
        self.continue_shopping_button.click()
        return self

    def go_to_cart_from_modal(self):
        self.view_cart_link.click()
        return self
