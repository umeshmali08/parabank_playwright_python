import pytest

from pages.registration_page import RegistrationPage
from pages.open_account_page import OpenAccountPage
from utils.data_factory import create_customer


@pytest.mark.ui
def test_register_and_open_checking_account(page):

    # Step 1 - Create dynamic user
    customer = create_customer()

    registration = RegistrationPage(page)

    registration.open()
    registration.register(customer)
    registration.verify_registration(
        customer["username"]
    )

    print(
        f"Registered user: "
        f"{customer['username']}"
    )

    # Step 2 - Open Checking account
    open_account = OpenAccountPage(page)

    open_account.open_page()

    new_account_id = (
        open_account.open_checking_account()
    )

    print(
        f"New Checking Account ID: "
        f"{new_account_id}"
    )

    # Basic validation
    assert new_account_id.isdigit()