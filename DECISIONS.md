# Architectural Decision Record

This document records the key architectural and testing decisions made while building the ParaBank Playwright Python automation framework.

---

## 1. State Contention

### Problem

ParaBank is a shared, stateful public sandbox.

The framework performs operations such as:

- customer registration
- account creation
- fund transfers
- loan requests
- database cleanup through `cleanDB`

Generating a unique username prevents one test run from registering the same user as another run, but it does not solve global-state contention.

The main risk is `cleanDB`.

If two CI workers execute against the same ParaBank instance:

```text
Worker A
Creates User A
        ↓
Starts Scenario A

Worker B
Calls cleanDB
        ↓
User A is removed
        ↓
Worker A fails

Decision

To reduce state contention, the framework uses the following controls:

Generate unique customer data for every run using Faker and unique identifiers.
Do not use hardcoded usernames.
Mark tests that call global reset operations as destructive.
Keep reset-bearing tests serial.
Use a GitHub Actions concurrency group so multiple CI runs from the same repository do not reset the public environment at the same time.
Avoid parallel execution against the shared public ParaBank sandbox.
Use isolated ParaBank environments if true parallel execution is required.
Why Unique Data Alone Is Not Enough

Unique customer data protects against collisions such as:

username already exists

but it cannot protect a test from another process calling:

cleanDB

because that operation affects the shared database globally.

Limitation

The framework can reduce collisions within its own test suite and CI pipeline, but it cannot prevent an external user of the public ParaBank sandbox from resetting the environment.

Therefore, the public ParaBank environment is treated as an external test-environment limitation.

For reliable parallel execution in a real project, each CI worker should use its own isolated ParaBank environment.

2. Currency Handling
Problem

Scenario B requires the framework to perform three fund transfers:

$150.00
$25.50
$8.99

The framework must parse the transaction values from the UI, calculate the total transferred amount, and verify that the account balance deduction matches the same amount.

The expected total is:

$184.49

Using normal binary floating-point values for exact financial assertions can introduce precision issues.

For example, decimal values may internally be represented approximately rather than exactly.

This makes direct financial equality checks unreliable.

Decision

The framework uses Python Decimal and integer cents for financial validation.

Currency values are normalized to two decimal places and converted into integer cents before aggregation.

Example:

$150.00 → 15000 cents
$25.50  →  2550 cents
$8.99   →   899 cents

The calculation becomes:

15000
+2550
+ 899
------
18449 cents

which represents:

$184.49

The framework then compares integer values:

assert total_debit_cents == expected_total_cents

instead of relying on floating-point equality.

Additional Validation

The framework also captures the source account balance immediately before the transfers and retrieves the balance again after the transfers.

Example:

Balance Before: 41550 cents
Balance After:  23101 cents

Actual Deduction:
41550 - 23101 = 18449 cents

The framework validates that:

Expected transfer total
=
UI transaction total
=
Actual account balance deduction

This provides stronger validation than checking only the transaction table.

Note on Assignment Wording

The assignment mentions floating-point precision handling in JavaScript/TypeScript.

Because this solution uses the permitted Playwright Python stack, the equivalent issue is handled using Python Decimal and integer cents.

3. API vs UI Boundary
Goal

The framework separates:

Environment setup
Server-side operations
Backend validation
User-visible business journeys

The intention is to use APIs where they improve speed and determinism, while keeping required user-facing flows in the UI.

API Responsibilities

Playwright APIRequestContext is used for operations such as:

database cleanup
customer login
customer account retrieval
account lookup
deposits
transfers in API-focused scenarios
loan-related backend validation
transaction history retrieval
server-side state validation
Scenario C execution

Examples:

api.clean_database()
api.login(...)
api.get_customer_accounts(...)
api.get_account(...)
api.deposit(...)
api.get_transactions(...)

APIs are preferred for:

setup
teardown
backend verification
direct server operations
API-only scenarios

because they are faster and less dependent on UI rendering.

UI Responsibilities

Page Objects are used for user-visible workflows such as:

customer registration
opening a new Checking account
configuring the Loan Provider through the Admin UI
requesting a loan
performing fund transfers
searching for transactions
validating visible loan status
reading the HTML transaction table

These remain UI actions because they represent the user journeys required by the assignment.

Scenario A Boundary

Scenario A uses a hybrid API + UI approach.

API
Clean Database
        ↓
UI
Configure Loan Provider = Web Service
        ↓
UI
Register Dynamic Customer
        ↓
UI
Open New Checking Account
        ↓
UI
Request Loan
        ↓
UI
Verify Loan Approved
        ↓
API
Retrieve Loan Account
        ↓
API
Verify Loan Balance

The UI is used for the business workflow, while the API is used for deterministic environment setup and backend verification.

This keeps the test meaningful from an end-user perspective while avoiding unnecessary UI-only validation.

Scenario B Boundary

Scenario B uses the UI for the business flow:

UI
Perform Fund Transfers
        ↓
UI
Open Find Transactions
        ↓
UI
Read HTML Transaction Table
        ↓
Parse Currency Values
        ↓
Calculate $184.49

The API is then used to retrieve the account balance:

API
Get Source Account
        ↓
Compare Balance Before and After
        ↓
Verify Deduction = $184.49

This provides both UI validation and backend-state verification.

Scenario C Boundary

Scenario C is intentionally browserless.

ParaBank's documented REST API does not expose a customer registration endpoint.

To keep the scenario headless, the framework submits the registration form through Playwright APIRequestContext without launching a browser.

The remaining flow uses REST APIs.

HTTP Customer Registration
        ↓
REST Login
        ↓
REST Account Retrieval
        ↓
REST Deposit
        ↓
REST Transaction History
        ↓
Pydantic Schema Validation

This keeps Scenario C fully headless while still allowing it to create its own dynamic test data.

Final Design Principle

The framework follows this rule:

API
→ setup
→ direct server operations
→ backend verification
→ API-only scenarios

UI
→ user behavior
→ visible workflows
→ rendering-dependent checks
→ HTML table extraction

This boundary keeps the framework maintainable, reduces unnecessary UI dependency, and preserves meaningful end-to-end coverage.
