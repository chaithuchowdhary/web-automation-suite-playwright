import re

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.review_rows = page.locator("#cart_info tbody tr")
        self.comment_box = page.locator("#ordermsg textarea")
        self.place_order_button = page.get_by_role("link", name="Place Order")

        # Login-required modal shown when checkout is attempted while logged out.
        self.checkout_modal = page.locator("#checkoutModal")
        self.checkout_modal_login_link = self.checkout_modal.get_by_role(
            "link", name="Register / Login"
        )

        # Payment page.
        self.name_on_card_input = page.locator('[data-qa="name-on-card"]')
        self.card_number_input = page.locator('[data-qa="card-number"]')
        self.cvc_input = page.locator('[data-qa="cvc"]')
        self.expiry_month_input = page.locator('[data-qa="expiry-month"]')
        self.expiry_year_input = page.locator('[data-qa="expiry-year"]')
        self.pay_button = page.locator('[data-qa="pay-button"]')
        self.order_placed_heading = page.get_by_text("Order Placed!")

    def requires_login(self) -> bool:
        return self.checkout_modal.is_visible()

    def go_to_login_from_modal(self):
        self.checkout_modal_login_link.click()
        return self

    def review_item_names(self) -> list[str]:
        texts = self.review_rows.locator(".cart_description h4 a").all_inner_texts()
        return [self.normalize_text(t) for t in texts]

    def place_order(self):
        self.place_order_button.click()
        # Confirm we actually landed on the payment page and its form is
        # interactable before any caller tries to fill it in.
        expect(self.page).to_have_url(re.compile(r"/payment$"))
        expect(self.name_on_card_input).to_be_visible()
        return self

    def pay_with_dummy_card(
        self, name: str, number: str, cvc: str, month: str, year: str
    ):
        self.name_on_card_input.fill(name)
        self.card_number_input.fill(number)
        self.cvc_input.fill(cvc)
        self.expiry_month_input.fill(month)
        self.expiry_year_input.fill(year)
        self.pay_button.click()
        return self

    def expect_order_confirmed(self):
        expect(self.order_placed_heading).to_be_visible()
