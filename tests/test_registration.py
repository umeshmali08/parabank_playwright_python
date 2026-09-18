import pytest

from pages.registration_page import RegistrationPage
from utils.data_factory import create_customer


@pytest.mark.ui
def test_register_dynamic_customer(page):

    registration = RegistrationPage(page)
    registration.open()

    max_attempts = 3

    for attempt in range(max_attempts):

        customer = create_customer()

        registration.register(customer)

        duplicate_error = page.get_by_text(
            "This username already exists."
        )

        if duplicate_error.is_visible():

            print(
                f"Username collision detected: "
                f"{customer['username']}. Retrying..."
            )

            continue

        registration.verify_registration(
            customer["username"]
        )

        print(
            f"Successfully registered: "
            f"{customer['username']}"
        )

        return

    pytest.fail(
        "Unable to register a unique ParaBank user "
        f"after {max_attempts} attempts."
    )