import pytest


@pytest.mark.destructive
@pytest.mark.ui
def test_scenario_a_loan_orchestration(
    scenario_ab_state
):

    state = scenario_ab_state

    customer = state["customer"]

    checking_account_id = (
        state["checking_account_id"]
    )

    loan_account_id = (
        state["loan_account_id"]
    )

    loan_balance = (
        state["loan_balance"]
    )

    print(
        "Database cleaned successfully"
    )

    print(
        "Loan Provider = Web Service"
    )

    print(
        f"Registered User: "
        f"{customer['username']}"
    )

    print(
        f"Checking Account ID: "
        f"{checking_account_id}"
    )

    assert checking_account_id.isdigit()

    print(
        f"Loan Account ID: "
        f"{loan_account_id}"
    )

    assert loan_account_id.isdigit()

    print(
        f"Loan Account Balance: "
        f"{loan_balance}"
    )

    assert float(
        loan_balance
    ) == 100.0