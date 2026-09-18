from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class FindTransactionsPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.find_transactions_link = page.get_by_role(
            "link",
            name="Find Transactions"
        )

        self.account_select = page.locator("#accountId")
        self.amount_input = page.locator("#amount")
        self.find_by_amount_button = page.locator("#findByAmount")
        self.transaction_table = page.locator("#transactionTable")

    def open_page(self):

        self.find_transactions_link.click()

        expect(
            self.page.get_by_text(
                "Find Transactions"
            ).first
        ).to_be_visible()

    def find_by_amount(
        self,
        account_id: str,
        amount: str
    ):

        account_option = self.account_select.locator(
            f'option[value="{account_id}"]'
        )

        expect(
            account_option
        ).to_have_count(1)

        self.account_select.select_option(
            value=account_id
        )

        self.amount_input.fill(amount)

        self.find_by_amount_button.click()

        expect(
            self.transaction_table
        ).to_be_visible()

    def get_transaction_rows(self):

        return self.transaction_table.locator(
            "tbody tr"
        )

    def get_debit_amount(self) -> str:

        rows = self.get_transaction_rows()

        expect(
            rows
        ).not_to_have_count(0)

        first_row = rows.first

        expect(
            first_row
        ).to_contain_text(
            "Funds Transfer Sent"
        )

        debit_amount = (
            first_row
            .locator("td")
            .nth(2)
            .inner_text()
            .strip()
        )

        return debit_amount