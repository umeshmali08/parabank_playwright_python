import pytest

from api.parabank_api import ParaBankAPI
from pages.admin_page import AdminPage
from pages.registration_page import RegistrationPage
from pages.open_account_page import OpenAccountPage
from utils.data_factory import create_customer


@pytest.mark.destructive
@pytest.mark.ui
def test_scenario_a_setup(
    page,
    api_context
):

    # ---------------------------------
    # STEP 1 - API Database Cleanup
    # ---------------------------------

    api = ParaBankAPI(api_context)

    api.clean_database()

    print("Database cleaned successfully")

    # ---------------------------------
    # STEP 2 - Configure Loan Provider
    # ---------------------------------

    admin = AdminPage(page)

    admin.open()

    admin.set_loan_provider_web_service()

    print(
        "Loan Provider configured as Web Service"
    )

    # ---------------------------------
    # STEP 3 - Register Dynamic User
    # ---------------------------------

    customer = create_customer()

    registration = RegistrationPage(page)

    registration.open()

    registration.register(customer)

    registration.verify_registration(
        customer["username"]
    )

    print(
        f"Registered User: "
        f"{customer['username']}"
    )

    # ------------------------------------
    # Get Customer ID and Original Account
    # ------------------------------------

    customer_api = api.login(
        customer["username"],
        customer["password"]
    )

    customer_id = customer_api["id"]

    accounts = api.get_customer_accounts(
        customer_id
    )

    original_account_id = str(
        accounts[0]["id"]
    )

    print(
        f"Customer ID: "
        f"{customer_id}"
    )

    print(
        f"Original Account ID: "
        f"{original_account_id}"
    )

    print(
        f"Original Account Balance: "
        f"{accounts[0]['balance']}"
    )

    # ---------------------------------
    # STEP 4 - Open Checking Account
    # ---------------------------------

    account_page = OpenAccountPage(page)

    account_page.open_page()

    checking_account_id = (
        account_page.open_checking_account()
    )

    print(
        f"Checking Account ID: "
        f"{checking_account_id}"
    )

    # ---------------------------------
    # STEP 5 - Validate Account ID
    # ---------------------------------

    assert checking_account_id.isdigit()