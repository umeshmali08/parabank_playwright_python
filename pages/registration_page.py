import pytest

from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class RegistrationPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.first_name = page.locator(
            'input[name="customer.firstName"]'
        )
        self.last_name = page.locator(
            'input[name="customer.lastName"]'
        )
        self.street = page.locator(
            'input[name="customer.address.street"]'
        )
        self.city = page.locator(
            'input[name="customer.address.city"]'
        )
        self.state = page.locator(
            'input[name="customer.address.state"]'
        )
        self.zip_code = page.locator(
            'input[name="customer.address.zipCode"]'
        )
        self.phone = page.locator(
            'input[name="customer.phoneNumber"]'
        )
        self.ssn = page.locator(
            'input[name="customer.ssn"]'
        )
        self.username = page.locator(
            'input[name="customer.username"]'
        )
        self.password = page.locator(
            'input[name="customer.password"]'
        )
        self.repeated_password = page.locator(
            'input[name="repeatedPassword"]'
        )
        self.register_button = page.locator(
            'input[value="Register"]'
        )
        self.right_panel = page.locator(
            "#rightPanel"
        )

    def _safe_body_text(self) -> str:
        """
        Safely read the current page body text.
        """

        try:
            return (
                self.page
                .locator("body")
                .inner_text(timeout=2000)
                .lower()
            )
        except Exception:
            return ""

    def _safe_title(self) -> str:
        """
        Safely read the current page title.
        """

        try:
            return self.page.title().lower()
        except Exception:
            return ""

    def _is_cloudflare_challenge(self) -> bool:
        """
        Detect a real Cloudflare security challenge.
        """

        body_text = self._safe_body_text()
        title = self._safe_title()

        strong_indicators = [
            "performing security verification",
            "security service to protect against malicious bots",
            "enable javascript and cookies to continue",
            "verify you are human",
        ]

        if any(
            indicator in body_text
            for indicator in strong_indicators
        ):
            return True

        if (
            "just a moment" in title
            and (
                "ray id" in body_text
                or "cloudflare" in body_text
            )
        ):
            return True

        try:
            challenge_script = self.page.locator(
                'script[src*="/cdn-cgi/challenge-platform/"]'
            )

            if (
                challenge_script.count() > 0
                and (
                    "ray id" in body_text
                    or "cloudflare" in body_text
                )
            ):
                return True

        except Exception:
            pass

        return False

    def _skip_if_cloudflare(self):
        """
        Skip only when the current page is confirmed
        to be a Cloudflare security challenge.
        """

        if self._is_cloudflare_challenge():
            pytest.skip(
                "ParaBank UI was blocked by Cloudflare. "
                "External public sandbox limitation."
            )

    def open(self):
        """
        Open ParaBank registration page.
        """

        self.page.goto(
            "register.htm",
            wait_until="domcontentloaded"
        )

        try:
            expect(
                self.register_button
            ).to_be_visible(
                timeout=10000
            )

        except AssertionError:
            self._skip_if_cloudflare()
            raise

    def register(self, user: dict):
        """
        Fill and submit the registration form.
        """

        self.first_name.fill(
            user["first_name"]
        )
        self.last_name.fill(
            user["last_name"]
        )
        self.street.fill(
            user["street"]
        )
        self.city.fill(
            user["city"]
        )
        self.state.fill(
            user["state"]
        )
        self.zip_code.fill(
            user["zip_code"]
        )
        self.phone.fill(
            user["phone"]
        )
        self.ssn.fill(
            user["ssn"]
        )
        self.username.fill(
            user["username"]
        )
        self.password.fill(
            user["password"]
        )
        self.repeated_password.fill(
            user["password"]
        )

        self.register_button.click()

    def verify_registration(
        self,
        username: str
    ):
        """
        Verify successful registration.

        If the expected ParaBank result does not appear,
        check whether Cloudflare replaced the application page.
        """

        try:
            expect(
                self.right_panel
            ).to_contain_text(
                f"Welcome {username}",
                timeout=10000
            )

            return

        except AssertionError:

            self._skip_if_cloudflare()

            body_text = self._safe_body_text()

            if (
                "this username already exists"
                in body_text
            ):
                raise AssertionError(
                    f"Registration failed because username "
                    f"already exists: {username}"
                )

            raise