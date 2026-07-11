from playwright.sync_api import Page


class BasePage:
    """Common helpers shared by every page object.

    Holds the Playwright ``page`` and small conveniences. Locators are
    resolved lazily via Playwright's auto-waiting APIs everywhere - no
    manual ``time.sleep`` or ``wait_for_timeout`` calls.
    """

    def __init__(self, page: Page):
        self.page = page

    def goto(self, path: str = "/"):
        self.page.goto(path)
        return self

    @property
    def title(self) -> str:
        return self.page.title()

    def scroll_into_view(self, locator):
        locator.scroll_into_view_if_needed()
        return locator

    @staticmethod
    def normalize_text(text: str) -> str:
        """Collapse whitespace (incl. non-breaking spaces) so text compares
        reliably - the site renders the same product name with slightly
        different whitespace on the listing vs. the cart page."""
        return " ".join(text.replace("\xa0", " ").split())
