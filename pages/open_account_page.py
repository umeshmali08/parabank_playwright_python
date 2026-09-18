from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class OpenAccountPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.open_account_link = page.get_by_role(
            "link",
            name="Open New Account"
        )

        self.account_type = page.locator("#type")
        self.from_account = page.locator("#fromAccountId")

        self.open_account_button = page.get_by_role(
            "button",
            name="Open New Account"
        )

        self.new_account_id = page.locator("#newAccountId")
        self.right_panel = page.locator("#rightPanel")

    def open_page(self):

        self.open_account_link.click()

        expect(
            self.page.get_by_text(
                "What type of Account would you like to open?"
            )
        ).to_be_visible()

    def open_checking_account(self) -> str:

        self.account_type.select_option(
            label="CHECKING"
        )

        # ParaBank loads accounts dynamically.
        # Wait for at least one funding account instead of sleep.
        self.page.wait_for_function(
            """
            () => {
                const select =
                    document.querySelector('#fromAccountId');

                return select &&
                       select.options &&
                       select.options.length > 0;
            }
            """
        )

        self.open_account_button.click()

        expect(
            self.right_panel
        ).to_contain_text(
            "Account Opened!"
        )

        self.page.wait_for_function(
            """
            () => {
                const el =
                    document.querySelector('#newAccountId');

                return el &&
                       el.textContent &&
                       el.textContent.trim().length > 0;
            }
            """
        )

        return self.new_account_id.inner_text().strip()