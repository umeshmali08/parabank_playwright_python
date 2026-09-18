import pytest

from playwright.sync_api import Playwright

from api.parabank_api import ParaBankAPI
from config.config import UI_BASE_URL, API_BASE_URL
from pages.admin_page import AdminPage
from pages.registration_page import RegistrationPage
from pages.open_account_page import OpenAccountPage
from pages.loan_page import LoanPage
from utils.data_factory import create_customer


pytest_plugins = [
    "reporters.custom_reporter"
]


@pytest.fixture(scope="session")
def browser_context_args(
    browser_context_args
):
    return {
        **browser_context_args,
        "base_url": UI_BASE_URL,
    }


@pytest.fixture(scope="session")
def api_context(
    playwright: Playwright
):
    context = playwright.request.new_context(
        base_url=API_BASE_URL,
        extra_http_headers={
            "Accept": "application/json"
        },
    )

    yield context

    context.dispose()


@pytest.fixture
def customer_data():
    return create_customer()


@pytest.fixture(scope="session")
def scenario_ab_state(
    browser,
    api_context,
    browser_context_args
):
    """
    Shared state for Scenario A and Scenario B.

    Scenario A creates the customer, accounts,
    and loan once.

    Scenario B continues with the exact same
    customer and account IDs.
    """

    context = browser.new_context(
        **browser_context_args
    )

    page = context.new_page()

    api = ParaBankAPI(
        api_context
    )

    # ---------------------------------
    # STEP 1 - Clean database
    # ---------------------------------

    api.clean_database()

    # ---------------------------------
    # STEP 2 - Configure Loan Provider
    # ---------------------------------

    admin = AdminPage(
        page
    )

    admin.open()

    admin.set_loan_provider_web_service()

    # ---------------------------------
    # STEP 3 - Register dynamic user
    # ---------------------------------

    customer = create_customer()

    registration = RegistrationPage(
        page
    )

    registration.open()

    registration.register(
        customer
    )

    registration.verify_registration(
        customer["username"]
    )

    # ---------------------------------
    # STEP 4 - Get original account
    # ---------------------------------

    customer_api = api.login(
        customer["username"],
        customer["password"]
    )

    customer_id = int(
        customer_api["id"]
    )

    accounts = api.get_customer_accounts(
        customer_id
    )

    original_account_id = str(
        accounts[0]["id"]
    )

    # ---------------------------------
    # STEP 5 - Open Checking account
    # ---------------------------------

    account_page = OpenAccountPage(
        page
    )

    account_page.open_page()

    checking_account_id = (
        account_page.open_checking_account()
    )

    # ---------------------------------
    # STEP 6 - Request Loan
    # ---------------------------------

    loan_page = LoanPage(
        page
    )

    loan_page.open_page()

    loan_account_id = (
        loan_page.request_loan(
            amount="100",
            down_payment="10",
            account_id=checking_account_id
        )
    )

    # ---------------------------------
    # STEP 7 - Loan backend validation
    # ---------------------------------

    loan_account = api.get_account(
        int(loan_account_id)
    )

    # ---------------------------------
    # STEP 8 - Store shared state
    # ---------------------------------

    state = {
        "page": page,
        "api": api,
        "customer": customer,
        "customer_id": customer_id,
        "original_account_id": original_account_id,
        "checking_account_id": checking_account_id,
        "loan_account_id": loan_account_id,
        "loan_balance": loan_account["balance"],
    }

    yield state

    # ---------------------------------
    # Cleanup browser context
    # ---------------------------------

    context.close()