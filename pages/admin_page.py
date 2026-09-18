from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class AdminPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    def open(self):
        self.page.goto("admin.htm")

        expect(
            self.page.get_by_text("Administration")
        ).to_be_visible()

    def set_loan_provider_web_service(self):

        # Locate the row containing Loan Provider
        loan_provider_row = (
            self.page.locator("tr")
            .filter(has_text="Loan Provider:")
        )

        loan_provider = loan_provider_row.locator("select")

        expect(loan_provider).to_be_visible()

        loan_provider.select_option(
            label="Web Service"
        )

        # Confirm selection before saving
        expect(
            loan_provider.locator("option:checked")
        ).to_have_text("Web Service")

        # Save admin configuration
        self.page.get_by_role(
            "button",
            name="Submit"
        ).click()