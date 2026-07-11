from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_rows = page.locator("#cart_info tbody tr")
        self.proceed_to_checkout_button = page.get_by_text("Proceed To Checkout")
        self.empty_cart_message = page.get_by_text("Cart is empty!")

    def open(self):
        self.goto("/view_cart")
        return self

    def item_count(self) -> int:
        return self.cart_rows.count()

    def item_names(self) -> list[str]:
        texts = self.cart_rows.locator(".cart_description h4 a").all_inner_texts()
        return [self.normalize_text(t) for t in texts]

    def item_prices(self) -> list[str]:
        return self.cart_rows.locator(".cart_price p").all_inner_texts()

    def item_quantities(self) -> list[str]:
        return self.cart_rows.locator(".cart_quantity button").all_inner_texts()

    def row_for_product(self, name: str):
        return self.cart_rows.filter(has_text=name)

    def remove_item(self, name: str):
        self.row_for_product(name).locator(".cart_quantity_delete").click()
        return self

    def proceed_to_checkout(self):
        self.proceed_to_checkout_button.click()
        return self

    def clear(self):
        """Empty the cart. Logged-in tests share one account's server-side
        cart, so this guarantees a clean starting point regardless of what
        other tests (possibly running in parallel) have added."""
        self.open()
        while self.cart_rows.count() > 0:
            remaining = self.cart_rows.count()
            self.cart_rows.first.locator(".cart_quantity_delete").click()
            expect(self.cart_rows).to_have_count(remaining - 1)
        return self
