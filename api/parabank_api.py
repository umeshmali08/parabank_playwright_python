from playwright.sync_api import APIRequestContext, APIResponse
from config.config import UI_BASE_URL


class ParaBankAPI:

    def __init__(self, request: APIRequestContext):
        self.request = request

    @staticmethod
    def _assert_ok(response: APIResponse, action: str):
        if not response.ok:
            raise AssertionError(
                f"{action} failed: HTTP {response.status}. "
                f"Response: {response.text()}"
            )

    def get_openapi(self) -> dict:
        response = self.request.get("openapi.json")
        self._assert_ok(
            response,
            "Get OpenAPI document"
        )
        return response.json()

    def register_customer(self, customer: dict):

        register_url = (
            f"{UI_BASE_URL}register.htm"
        )

        # First GET registration page
        # so ParaBank can establish session/cookies.
        get_response = self.request.get(
            register_url,
            headers={
                "Accept": "text/html"
            }
        )

        self._assert_ok(
            get_response,
            "Open registration page"
        )

        # Submit registration form
        response = self.request.post(
            register_url,
            form={
                "customer.firstName":
                    customer["first_name"],

                "customer.lastName":
                    customer["last_name"],

                "customer.address.street":
                    customer["street"],

                "customer.address.city":
                    customer["city"],

                "customer.address.state":
                    customer["state"],

                "customer.address.zipCode":
                    customer["zip_code"],

                "customer.phoneNumber":
                    customer["phone"],

                "customer.ssn":
                    customer["ssn"],

                "customer.username":
                    customer["username"],

                "customer.password":
                    customer["password"],

                "repeatedPassword":
                    customer["password"],
            },
            headers={
                "Accept": "text/html",
                "Referer": register_url,
            }
        )

        self._assert_ok(
            response,
            "Register customer"
        )

        response_body = response.text()

        if "This username already exists." in response_body:
            raise AssertionError(
                f"Username already exists: "
                f"{customer['username']}"
            )

        if (
            f"Welcome {customer['username']}"
            not in response_body
        ):
            raise AssertionError(
                "Customer registration did not "
                "return expected welcome message."
            )

        return response

    def clean_database(self):
        response = self.request.post(
            "cleanDB"
        )

        self._assert_ok(
            response,
            "Clean database"
        )

        return response

    def initialize_database(self):
        response = self.request.post(
            "initializeDB"
        )

        self._assert_ok(
            response,
            "Initialize database"
        )

        return response

    def set_parameter(
        self,
        name: str,
        value: str
    ):

        response = self.request.post(
            f"setParameter/{name}/{value}"
        )

        self._assert_ok(
            response,
            f"Set parameter {name}"
        )

        return response

    def login(
        self,
        username: str,
        password: str
    ) -> dict:

        response = self.request.get(
            f"login/{username}/{password}"
        )

        self._assert_ok(
            response,
            "API login"
        )

        return response.json()

    def get_customer_accounts(
        self,
        customer_id: int
    ) -> list:

        response = self.request.get(
            f"customers/{customer_id}/accounts"
        )

        self._assert_ok(
            response,
            "Get customer accounts"
        )

        return response.json()

    def get_account(
        self,
        account_id: int
    ) -> dict:

        response = self.request.get(
            f"accounts/{account_id}"
        )

        self._assert_ok(
            response,
            "Get account"
        )

        return response.json()

    def create_account(
        self,
        customer_id: int,
        account_type: int,
        from_account_id: int
    ) -> dict:

        response = self.request.post(
            "createAccount",
            params={
                "customerId":
                    customer_id,

                "newAccountType":
                    account_type,

                "fromAccountId":
                    from_account_id,
            },
        )

        self._assert_ok(
            response,
            "Create account"
        )

        return response.json()

    def deposit(
        self,
        account_id: int,
        amount
    ):

        response = self.request.post(
            "deposit",
            params={
                "accountId": account_id,
                "amount": amount
            },
        )

        self._assert_ok(
            response,
            "Deposit"
        )

        return response

    def transfer(
        self,
        from_account_id: int,
        to_account_id: int,
        amount
    ):

        response = self.request.post(
            "transfer",
            params={
                "fromAccountId":
                    from_account_id,

                "toAccountId":
                    to_account_id,

                "amount":
                    amount,
            },
        )

        self._assert_ok(
            response,
            "Transfer"
        )

        return response

    def request_loan(
        self,
        customer_id: int,
        amount,
        down_payment,
        from_account_id: int
    ) -> dict:

        response = self.request.post(
            "requestLoan",
            params={
                "customerId":
                    customer_id,

                "amount":
                    amount,

                "downPayment":
                    down_payment,

                "fromAccountId":
                    from_account_id,
            },
        )

        self._assert_ok(
            response,
            "Request loan"
        )

        return response.json()

    def get_transactions(
        self,
        account_id: int
    ) -> list:

        response = self.request.get(
            f"accounts/{account_id}/transactions"
        )

        self._assert_ok(
            response,
            "Get transactions"
        )

        return response.json()