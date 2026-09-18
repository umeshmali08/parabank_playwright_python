import pytest

from api.parabank_api import ParaBankAPI
from pages.admin_page import AdminPage
from pages.registration_page import RegistrationPage
from pages.open_account_page import OpenAccountPage
from pages.loan_page import LoanPage
from utils.data_factory import create_customer


@pytest.mark.destructive
@pytest.mark.ui
def test_scenario_a_loan_orchestration(
    page,
    api_context
):

    api = ParaBankAPI(api_context)

    # ------------------------------------
    # 1. Database pre-condition
    # ------------------------------------

    api.clean_database()

    print(
        "Database cleaned successfully"
    )

    # ------------------------------------
    # 2. Loan Provider configuration
    # ------------------------------------

    admin = AdminPage(page)

    admin.open()

    admin.set_loan_provider_web_service()

    print(
        "Loan Provider = Web Service"
    )

    # ------------------------------------
    # 3. Dynamic customer registration
    # ------------------------------------

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
    # 4. Open new Checking account
    # ------------------------------------

    account_page = OpenAccountPage(page)

    account_page.open_page()

    checking_account_id = (
        account_page.open_checking_account()
    )

    print(
        f"Checking Account ID: "
        f"{checking_account_id}"
    )

    assert checking_account_id.isdigit()

    # ------------------------------------
    # 5. Request loan
    # ------------------------------------

    loan_page = LoanPage(page)

    loan_page.open_page()

    loan_account_id = (
        loan_page.request_loan(
            amount="100",
            down_payment="10",
            account_id=checking_account_id
        )
    )

    print(
        f"Loan Account ID: "
        f"{loan_account_id}"
    )

    assert loan_account_id.isdigit()

    # ------------------------------------
    # 6. API balance verification
    # ------------------------------------

    loan_account = api.get_account(
        int(loan_account_id)
    )

    print(
        f"Loan Account Balance: "
        f"{loan_account['balance']}"
    )

    assert float(
        loan_account["balance"]
    ) == 100.0
    