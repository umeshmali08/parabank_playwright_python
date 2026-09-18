# ParaBank Playwright Python Automation

Automation framework created for the Senior QA Automation Engineer assignment using Playwright, Python, and Pytest.

The framework covers UI automation, API testing, dynamic test-data generation, transaction validation, custom reporting, and CI/CD execution against the ParaBank application.

## Tech Stack

- Python 3.12
- Playwright
- Pytest
- Pytest-Playwright
- Faker
- Pydantic
- GitHub Actions

## Framework Design

The framework follows the Page Object Model (POM) pattern.

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
├── reports/
│   └── index.html
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