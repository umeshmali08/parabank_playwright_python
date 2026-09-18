import pytest

from api.parabank_api import ParaBankAPI
from schemas.transaction import Transaction
from utils.data_factory import create_customer


@pytest.mark.destructive
@pytest.mark.api
def test_scenario_c_api_parity(
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
    # STEP 2 - Generate dynamic customer
    # ---------------------------------

    customer = create_customer()

    print(
        f"Generated User: "
        f"{customer['username']}"
    )

    # ---------------------------------
    # STEP 3 - Register via HTTP only
    # ---------------------------------

    api.register_customer(
        customer
    )

    print(
        "Customer registered through "
        "HTTP request"
    )

    # ---------------------------------
    # STEP 4 - Login via REST API
    # ---------------------------------

    customer_api = api.login(
        customer["username"],
        customer["password"]
    )

    customer_id = customer_api["id"]

    print(
        f"Customer ID: "
        f"{customer_id}"
    )

    # ---------------------------------
    # STEP 5 - Get customer account
    # ---------------------------------

    accounts = api.get_customer_accounts(
        customer_id
    )

    assert len(accounts) >= 1

    account_id = accounts[0]["id"]

    print(
        f"Account ID: "
        f"{account_id}"
    )

    # ---------------------------------
    # STEP 6 - Deposit funds
    # ---------------------------------

    deposit_amount = 250.75

    api.deposit(
        account_id,
        deposit_amount
    )

    print(
        f"Deposited: "
        f"${deposit_amount}"
    )

    # ---------------------------------
    # STEP 7 - Get transactions
    # ---------------------------------

    transactions = api.get_transactions(
        account_id
    )

    assert len(transactions) >= 1

    print(
        f"Transaction Count: "
        f"{len(transactions)}"
    )

    # ---------------------------------
    # STEP 8 - Schema validation
    # ---------------------------------

    validated_transactions = []

    for transaction in transactions:

        validated = (
            Transaction.model_validate(
                transaction
            )
        )

        validated_transactions.append(
            validated
        )

    print(
        "All transaction schemas "
        "validated successfully"
    )

    # ---------------------------------
    # STEP 9 - Validate deposit exists
    # ---------------------------------

    matching_deposits = [
        transaction
        for transaction in validated_transactions
        if (
            transaction.type == "Credit"
            and float(
                transaction.amount
            ) == deposit_amount
        )
    ]

    assert len(
        matching_deposits
    ) >= 1

    print(
        f"Deposit transaction found: "
        f"${deposit_amount}"
    )