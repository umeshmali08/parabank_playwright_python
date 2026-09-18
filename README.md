# ParaBank Playwright Python Automation

Automation framework developed for the **Senior QA Automation Engineer assignment** using **Playwright, Python, and Pytest**.

The framework demonstrates UI automation, API testing, dynamic test-data management, transactional validation, API schema validation, custom HTML reporting, and CI/CD execution against the ParaBank application.

---

## Tech Stack

- Python 3.12
- Playwright
- Pytest
- Pytest-Playwright
- Faker
- Pydantic
- GitHub Actions

---

## Framework Design

The framework follows the **Page Object Model (POM)** design pattern.

Responsibilities are separated across:

- Page Objects for UI workflows
- API client for backend operations and validation
- Utility modules for test data and currency handling
- Pydantic schemas for API contract validation
- TypeScript contract definitions
- Pytest fixtures for reusable test state
- Custom Pytest HTML reporting
- GitHub Actions for CI execution

### Project Structure

```text
parabank_playwright_python/
│
├── api/
│   └── parabank_api.py
│
├── config/
│   └── config.py
│
├── contracts/
│   └── transaction.ts
│
├── pages/
│   ├── base_page.py
│   ├── registration_page.py
│   ├── admin_page.py
│   ├── open_account_page.py
│   ├── loan_page.py
│   ├── transfer_funds_page.py
│   └── find_transactions_page.py
│
├── reporters/
│   └── custom_reporter.py
│
├── schemas/
│   └── transaction.py
│
├── tests/
│   ├── test_api_smoke.py
│   ├── test_currency.py
│   ├── test_registration.py
│   ├── test_open_account.py
│   ├── test_scenario_a.py
│   ├── test_scenario_b.py
│   └── test_scenario_c.py
│
├── utils/
│   ├── currency.py
│   └── data_factory.py
│
├── .github/
│   └── workflows/
│       └── playwright.yml
│
├── conftest.py
├── pytest.ini
├── requirements.txt
├── DECISIONS.md
└── README.md

The reports/ directory is generated automatically during test execution.

Prerequisites

Install:

Python 3.12+
Git
Chromium through Playwright

Verify Python:

python --version
Setup

Clone the repository:

git clone https://github.com/umeshmali08/parabank_playwright_python.git

Move into the project:

cd parabank_playwright_python

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.\.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Install Playwright Chromium:

playwright install chromium
Running the Tests
Run the Complete Test Suite
pytest -v -s
Run the Primary Assignment Suite
pytest tests/test_currency.py tests/test_api_smoke.py tests/test_registration.py tests/test_open_account.py tests/test_scenario_a.py tests/test_scenario_b.py tests/test_scenario_c.py -v -s
Run Scenario A and Scenario B Together
pytest tests/test_scenario_a.py tests/test_scenario_b.py -v -s

This confirms that Scenario B continues with the same customer and account state created for Scenario A.

Run Scenario C Only
pytest tests/test_scenario_c.py -v -s
Assignment Scenarios
Scenario A - Global State and Loan Orchestration

Scenario A performs the following flow:

Cleans the ParaBank database.
Configures the Loan Provider as Web Service.
Generates and registers a dynamic customer.
Retrieves the customer's original account.
Opens a new Checking account.
Requests a loan using the dynamically generated account ID.
Verifies that the loan is approved.
Captures the generated Loan Account ID.
Uses the API to verify the loan-account balance.

Dynamic Playwright waits and assertions are used instead of static sleeps.

Scenario B - Transaction Aggregation and Currency Parsing

Scenario B continues with the same customer created during Scenario A.

It performs three fund transfers:

$150.00
$25.50
$8.99

The framework then:

Navigates to Find Transactions.
Extracts debit values from the HTML transaction table.
Parses currency strings.
Converts monetary values into integer cents.
Calculates the total transferred amount.
Verifies the UI transaction total.
Verifies the actual source-account balance deduction through the API.

Expected total:

15000 + 2550 + 899 = 18449 cents

Equivalent to:

$184.49

The following values are validated to match:

Expected Transfer Total
=
UI Transaction Total
=
Actual Account Balance Deduction
Scenario C - API Parity Validation

Scenario C is intentionally browserless.

Playwright APIRequestContext is used to:

Create a dynamic customer through ParaBank's HTTP registration flow.
Authenticate the customer through the REST API.
Retrieve the customer's accounts.
Deposit funds.
Retrieve transaction history.
Validate transaction data against a strict Pydantic schema.

A predefined TypeScript contract is also included:

contracts/transaction.ts

The runtime Python schema is located at:

schemas/transaction.py

Unexpected fields are rejected during schema validation.

Dynamic Test Data

Test users are generated dynamically using Faker and unique identifiers.

Hardcoded usernames are not used because ParaBank is a shared, stateful public environment.

Example generated username:

qa030820000acc

This helps reduce username collisions between test runs.

Currency Handling

Financial comparisons do not rely on normal binary floating-point equality.

Currency strings are normalized and converted to integer cents.

Example:

$150.00 → 15000 cents
$25.50  → 2550 cents
$8.99   → 899 cents

This provides deterministic monetary assertions.

API and UI Strategy

The framework uses a hybrid API/UI approach.

API Responsibilities

APIs are used for:

Database cleanup
Backend account validation
Customer authentication
Account retrieval
Deposits
Transaction retrieval
Loan balance validation
API-focused scenarios
UI Responsibilities

The UI is used for:

Customer registration
Loan Provider configuration
Opening accounts
Loan requests
Fund transfers
Find Transactions
User-visible business validations

This keeps UI tests focused on actual user behavior while using APIs for efficient backend verification.

Shared Scenario State

Scenario A and Scenario B use a shared session-scoped fixture:

scenario_ab_state

The fixture creates the customer and account state once.

Scenario A validates the loan workflow, while Scenario B continues using the same customer and account IDs.

This avoids:

Re-registering a second customer for Scenario B
Resetting the database between Scenario A and Scenario B
Test-data inconsistency between the two workflows
Custom HTML Reporter

The project includes a custom Pytest HTML reporter:

reporters/custom_reporter.py

It generates:

reports/index.html

The dashboard includes:

Total test count
Passed tests
Failed tests
Skipped tests
Execution duration
Individual test results
Glassmorphism-style summary cards
Required accent color #F48031

The project does not rely on the default Playwright HTML report or Allure for the assignment dashboard.

View the Report on Windows

After running the tests:

start reports\index.html

Example successful local execution:

Total:   7
Passed:  7
Failed:  0
Skipped: 0
Cloudflare / Public Sandbox Handling

ParaBank is a public shared environment and may occasionally display a Cloudflare security-verification page, especially when requests originate from hosted CI infrastructure.

The framework detects confirmed Cloudflare challenge responses separately from application failures.

When a genuine Cloudflare challenge is detected, the affected test can be reported as skipped because the condition is external to the application under test.

The framework does not convert normal application failures into skips.

Examples that continue to fail normally include:

Invalid application responses
Missing expected UI elements
Duplicate usernames
ParaBank form validation errors
Unexpected HTTP failures
Incorrect transaction values
Schema validation failures
Custom Report Output

After test execution:

reports/index.html

is automatically generated by the custom reporter.

The report can also be uploaded as a CI artifact by GitHub Actions.

CI/CD - GitHub Actions

The GitHub Actions workflow is located at:

.github/workflows/playwright.yml

The CI pipeline:

Checks out the repository.
Sets up Python 3.12.
Installs project dependencies.
Installs Playwright Chromium and required system dependencies.
Executes the assignment test suite.
Generates the custom HTML report.
Uploads the report as a workflow artifact.

CI concurrency is configured to reduce collisions caused by destructive database-reset operations against the shared ParaBank environment.

Running in CI

The workflow runs automatically on:

push
pull_request

The custom report is uploaded as:

parabank-custom-report
Architectural Decisions

Detailed architectural decisions are documented in:

DECISIONS.md

The document covers:

State contention in the shared ParaBank environment.
Currency and floating-point precision handling.
API versus UI testing boundaries.
Key Framework Features
Page Object Model
Dynamic test-data generation
API and UI hybrid testing
Shared Scenario A/B test state
REST API validation
Strict API schema validation
TypeScript transaction contract
Currency parsing using integer cents
No static sleeps for dynamic account selection
Custom HTML dashboard
Glassmorphism UI
Required #F48031 branding
GitHub Actions CI/CD
CI report artifacts
Public-sandbox contention handling
Repository

GitHub:

https://github.com/umeshmali08/parabank_playwright_python
Final Validation

The framework has been validated locally with the complete assignment suite.

A successful local execution produces:

7 passed

When the public ParaBank environment triggers a confirmed Cloudflare challenge, the affected test may be reported as skipped instead of incorrectly reporting an application failure.

Author

Umesh Mali

QA Automation Engineer


Before pushing this README, remove the old `[svg](...)` lines entirely. They are not needed in the Markdown file