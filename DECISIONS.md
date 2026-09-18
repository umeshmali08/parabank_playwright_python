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

The framework uses the following controls:

Generate unique customer data for every run using Faker and unique identifiers.
Do not use hardcoded usernames.
Keep global reset operations serial.
Use a GitHub Actions concurrency group so multiple CI runs from the same repository do not reset the shared ParaBank environment at the same time.
Avoid parallel execution of reset-bearing scenarios against the public sandbox.
Use isolated ParaBank environments if true parallel execution is required.
Shared Scenario A/B State

Scenario B is required to continue using the customer created for Scenario A.

To avoid creating a second customer or resetting the database between the two scenarios, the framework uses the session-scoped fixture:

scenario_ab_state

The fixture performs the shared setup once and stores:

customer
customer_id
original_account_id
checking_account_id
loan_account_id
loan_balance

Scenario A validates the loan workflow using this state.

Scenario B then continues with the same customer and account IDs to perform the transaction workflow.

This avoids:

re-registering another customer for Scenario B
resetting Scenario A data before Scenario B
relying on separate duplicated setup logic
inconsistent account state between the scenarios
Why Unique Data Alone Is Not Enough

Unique customer data protects against collisions such as:

username already exists

but it cannot protect a test from another process calling:

cleanDB

because that operation affects the shared database globally.

Limitation

The framework can reduce collisions within its own test suite and CI pipeline, but it cannot prevent another external user of the public ParaBank sandbox from resetting the environment.

Therefore, the public ParaBank instance is treated as an external test-environment limitation.

For reliable parallel execution in a real project, each CI worker should use an isolated environment.

2. Currency Handling
Problem

Scenario B performs three fund transfers:

$150.00
$25.50
$8.99

The framework must parse transaction values from the UI, calculate the total transferred amount, and verify that the source-account balance deduction matches the same amount.

The expected total is:

$184.49

Using normal binary floating-point values for exact financial assertions can introduce precision issues.

Decimal values may internally be represented approximately rather than exactly, making direct financial equality checks unreliable.

Decision

The framework uses Python Decimal and integer cents for financial validation.

Currency values are normalized to two decimal places and converted into integer cents before aggregation.

Example:

$150.00 → 15000 cents
$25.50  → 2550 cents
$8.99   → 899 cents

The calculation becomes:

15000
+2550
+ 899
------
18449 cents

which represents:

$184.49

The framework compares integer values:

assert total_debit_cents == expected_total_cents

instead of relying on floating-point equality.

Additional Validation

The source-account balance is captured immediately before the transfers and retrieved again after the transfers.

Example:

Balance Before: 41550 cents
Balance After:  23101 cents

Actual Deduction:
41550 - 23101 = 18449 cents

The framework validates that:

Expected Transfer Total
=
UI Transaction Total
=
Actual Account Balance Deduction

This provides stronger validation than checking only the transaction table.

Note on Assignment Wording

The assignment refers to floating-point handling in JavaScript/TypeScript.

Because this solution uses the permitted Playwright Python stack, the equivalent precision issue is handled using Python Decimal and integer cents.

3. Design Pattern and API vs UI Boundary
Design Pattern

The framework follows the Page Object Model pattern.

UI behavior is encapsulated in dedicated Page Objects such as:

RegistrationPage
AdminPage
OpenAccountPage
LoanPage
TransferFundsPage
FindTransactionsPage

Backend operations are encapsulated in:

ParaBankAPI

Reusable test data, currency handling, schemas, and shared state are separated into dedicated utility and fixture layers.

This keeps test cases focused on business workflows rather than implementation details.

API Responsibilities

Playwright APIRequestContext is used for:

database cleanup
customer authentication
customer account retrieval
account lookup
deposits
transaction-history retrieval
backend balance validation
API-focused scenarios
Scenario C execution

Examples:

api.clean_database()
api.login(...)
api.get_customer_accounts(...)
api.get_account(...)
api.deposit(...)
api.get_transactions(...)

APIs are preferred for setup and backend verification where UI interaction would add unnecessary overhead.

UI Responsibilities

Page Objects are used for user-visible workflows such as:

customer registration
configuring the Loan Provider through the Admin UI
opening a Checking account
requesting a loan
performing fund transfers
searching for transactions
validating visible loan status
extracting transaction values from the HTML table

These actions remain UI-based because they represent the user journeys required by the assignment.

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
Open Checking Account
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

Scenario B Boundary

Scenario B continues using the same customer and account state created for Scenario A.

Scenario A Shared State
        ↓
Same Customer
Same Original Account
Same Checking Account
        ↓
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
        ↓
API
Get Source Account
        ↓
Compare Balance Before and After
        ↓
Verify Deduction = $184.49

This provides both UI validation and backend-state verification while satisfying the requirement that Scenario B use the user created for Scenario A.

Scenario C Boundary

Scenario C is intentionally browserless.

ParaBank's banking REST API does not expose customer registration as a direct REST operation.

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

A predefined TypeScript transaction contract is included in:

contracts/transaction.ts

and runtime response validation is performed using the strict Python schema in:

schemas/transaction.py
Final Design Principle

The framework follows this boundary:

API
→ environment setup
→ direct server operations
→ backend verification
→ API-focused scenarios

UI
→ user behavior
→ visible workflows
→ rendering-dependent validation
→ HTML table extraction

This design keeps the framework maintainable, reduces unnecessary UI dependency, preserves meaningful end-to-end coverage, and keeps the test implementation aligned with the assignment requirements.


This version now matches your final implementation much better, especially the **shared Scenario A/B user state**, which the assignment explicitly requires for Scenario B. :contentReference[oaicite:1]{index=1}

Before pushing, replace the old `DECISIONS.md` completely with this version so none of the escaped characters like `\---` or `2\.` remain.