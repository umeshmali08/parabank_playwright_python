import pytest

from pages.find_transactions_page import FindTransactionsPage
from utils.currency import currency_to_cents
from api.parabank_api import ParaBankAPI
from pages.admin_page import AdminPage
from pages.registration_page import RegistrationPage
from pages.open_account_page import OpenAccountPage
from pages.transfer_funds_page import TransferFundsPage
from utils.data_factory import create_customer


@pytest.mark.destructive
@pytest.mark.ui
def test_scenario_b_transaction_transfers(
    page,
    api_context
):

    api = ParaBankAPI(api_context)

    # ---------------------------------
    # STEP 1 - Clean database
    # ---------------------------------

    api.clean_database()

    print(
        "Database cleaned successfully"
    )

    # ---------------------------------
    # STEP 2 - Configure environment
    # ---------------------------------

    admin = AdminPage(page)

    admin.open()

    admin.set_loan_provider_web_service()

    # ---------------------------------
    # STEP 3 - Register dynamic user
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

    # ---------------------------------
    # STEP 4 - Get original account
    # ---------------------------------

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
        f"Original Account ID: "
        f"{original_account_id}"
    )

    print(
        f"Original Balance: "
        f"{accounts[0]['balance']}"
    )

    # ---------------------------------
    # STEP 5 - Open second account
    # ---------------------------------

    account_page = OpenAccountPage(page)

    account_page.open_page()

    checking_account_id = (
        account_page.open_checking_account()
    )

    print(
        f"Destination Account ID: "
        f"{checking_account_id}"
    )

        # ---------------------------------
    # Capture balance before transfers
    # ---------------------------------

    account_before = api.get_account(
        int(original_account_id)
    )

    balance_before_cents = currency_to_cents(
        f"${account_before['balance']}"
    )

    print(
        f"Balance Before Transfers: "
        f"${account_before['balance']}"
    )

    # ---------------------------------
    # STEP 6 - Perform transfers
    # ---------------------------------

    transfers = [
        "150.00",
        "25.50",
        "8.99"
    ]

    transfer_page = TransferFundsPage(page)

    for amount in transfers:

        transfer_page.open_page()

        transfer_page.transfer(
            amount=amount,
            from_account_id=original_account_id,
            to_account_id=checking_account_id
        )

        print(
            f"Transferred ${amount}"
        )

    # ---------------------------------
    # STEP 7 - API transaction check
    # ---------------------------------

    transactions = api.get_transactions(
        int(original_account_id)
    )

    print(
        f"Transaction count: "
        f"{len(transactions)}"
    )

    assert len(transactions) >= 3

    # ---------------------------------
    # STEP 8 - Find Transactions via UI
    # ---------------------------------

    find_page = FindTransactionsPage(page)

    expected_amounts = [
        "150.00",
        "25.50",
        "8.99"
    ]

    total_debit_cents = 0

    for amount in expected_amounts:

        find_page.open_page()

        find_page.find_by_amount(
            account_id=original_account_id,
            amount=amount
        )

        debit_text = find_page.get_debit_amount()

        debit_cents = currency_to_cents(
            debit_text
        )

        total_debit_cents += debit_cents

        print(
            f"Parsed Debit: "
            f"{debit_text} "
            f"= {debit_cents} cents"
        )

    # ---------------------------------
    # STEP 9 - Validate total transfers
    # ---------------------------------

    expected_total_cents = sum(
        currency_to_cents(
            f"${amount}"
        )
        for amount in expected_amounts
    )

    print(
        f"Expected Total: "
        f"{expected_total_cents} cents"
    )

    print(
        f"Actual UI Total: "
        f"{total_debit_cents} cents"
    )

    assert total_debit_cents == expected_total_cents

    assert expected_total_cents == 18449

    # ---------------------------------
    # STEP 10 - Validate balance deduction
    # ---------------------------------

    account_after = api.get_account(
        int(original_account_id)
    )

    balance_after_cents = currency_to_cents(
        f"${account_after['balance']}"
    )

    actual_deduction_cents = (
        balance_before_cents
        - balance_after_cents
    )

    print(
        f"Balance Before: "
        f"{balance_before_cents} cents"
    )

    print(
        f"Balance After: "
        f"{balance_after_cents} cents"
    )

    print(
        f"Actual Deduction: "
        f"{actual_deduction_cents} cents"
    )

    assert (
        actual_deduction_cents
        == expected_total_cents
    )