from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class RegistrationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name = page.locator('input[name="customer.firstName"]')
        self.last_name = page.locator('input[name="customer.lastName"]')
        self.street = page.locator('input[name="customer.address.street"]')
        self.city = page.locator('input[name="customer.address.city"]')
        self.state = page.locator('input[name="customer.address.state"]')
        self.zip_code = page.locator('input[name="customer.address.zipCode"]')
        self.phone = page.locator('input[name="customer.phoneNumber"]')
        self.ssn = page.locator('input[name="customer.ssn"]')
        self.username = page.locator('input[name="customer.username"]')
        self.password = page.locator('input[name="customer.password"]')
        self.repeated_password = page.locator('input[name="repeatedPassword"]')
        self.register_button = page.locator('input[value="Register"]')
        self.right_panel = page.locator("#rightPanel")

    def open(self):
        self.page.goto("register.htm")

    def register(self, user: dict):
        self.first_name.fill(user["first_name"])
        self.last_name.fill(user["last_name"])
        self.street.fill(user["street"])
        self.city.fill(user["city"])
        self.state.fill(user["state"])
        self.zip_code.fill(user["zip_code"])
        self.phone.fill(user["phone"])
        self.ssn.fill(user["ssn"])
        self.username.fill(user["username"])
        self.password.fill(user["password"])
        self.repeated_password.fill(user["password"])
        self.register_button.click()

    def verify_registration(self, username: str):
        expect(self.right_panel).to_contain_text(f"Welcome {username}")
