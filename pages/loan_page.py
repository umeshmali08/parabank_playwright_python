from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class LoanPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.request_loan_link = page.get_by_role(
            "link",
            name="Request Loan"
        )

        self.amount_input = page.locator("#amount")
        self.down_payment_input = page.locator("#downPayment")
        self.from_account = page.locator("#fromAccountId")

        self.apply_button = page.get_by_role(
            "button",
            name="Apply Now"
        )

        self.loan_status = page.locator("#loanStatus")
        self.new_account_id = page.locator("#newAccountId")

    def open_page(self):

        self.request_loan_link.click()

        expect(
            self.page.get_by_text("Apply for a Loan")
        ).to_be_visible()

    def request_loan(
        self,
        amount: str,
        down_payment: str,
        account_id: str
    ) -> str:

        self.amount_input.fill(amount)
        self.down_payment_input.fill(down_payment)

        account_option = self.from_account.locator(
            f'option[value="{account_id}"]'
        )

        expect(
            account_option
        ).to_have_count(1)

        self.from_account.select_option(
            value=account_id
        )

        self.apply_button.click()

        expect(
            self.loan_status
        ).to_have_text("Approved")

        expect(
            self.new_account_id
        ).to_be_visible()

        return (
            self.new_account_id
            .inner_text()
            .strip()
        )