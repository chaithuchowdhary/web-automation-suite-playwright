from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = page.locator('[data-qa="login-email"]')
        self.password_input = page.locator('[data-qa="login-password"]')
        self.login_button = page.locator('[data-qa="login-button"]')
        self.error_message = page.locator("form").get_by_text(
            "Your email or password is incorrect!"
        )
        self.logout_link = page.get_by_role("link", name="Logout")
        self.logged_in_as = page.get_by_text("Logged in as")

    def open(self):
        self.goto("/login")
        return self

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()
        return self

    def logout(self):
        self.logout_link.click()
        return self

    def is_logged_in(self) -> bool:
        return self.logged_in_as.is_visible()

    def expect_login_error(self):
        expect(self.error_message).to_be_visible()
