from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class TransferFundsPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.transfer_link = page.get_by_role(
            "link",
            name="Transfer Funds"
        )

        self.amount_input = page.locator("#amount")

        self.from_account = page.locator(
            "#fromAccountId"
        )

        self.to_account = page.locator(
            "#toAccountId"
        )

        self.transfer_button = page.get_by_role(
            "button",
            name="Transfer"
        )

        self.result_panel = page.locator(
            "#showResult"
        )

    def open_page(self):

        self.transfer_link.click()

        expect(
            self.page.get_by_text(
                "Transfer Funds"
            ).first
        ).to_be_visible()

    def transfer(
        self,
        amount: str,
        from_account_id: str,
        to_account_id: str
    ):

        # Wait for source account
        from_option = self.from_account.locator(
            f'option[value="{from_account_id}"]'
        )

        expect(
            from_option
        ).to_have_count(1)

        # Wait for destination account
        to_option = self.to_account.locator(
            f'option[value="{to_account_id}"]'
        )

        expect(
            to_option
        ).to_have_count(1)

        self.amount_input.fill(amount)

        self.from_account.select_option(
            value=from_account_id
        )

        self.to_account.select_option(
            value=to_account_id
        )

        self.transfer_button.click()

        expect(
            self.result_panel
        ).to_contain_text(
            "Transfer Complete!"
        )