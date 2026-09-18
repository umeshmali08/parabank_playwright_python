import pytest
from playwright.sync_api import Playwright
from config.config import UI_BASE_URL, API_BASE_URL
from utils.data_factory import create_customer

pytest_plugins = ["reporters.custom_reporter"]


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "base_url": UI_BASE_URL,
    }


@pytest.fixture(scope="session")
def api_context(playwright: Playwright):
    context = playwright.request.new_context(
        base_url=API_BASE_URL,
        extra_http_headers={"Accept": "application/json"},
    )
    yield context
    context.dispose()


@pytest.fixture
def customer_data():
    return create_customer()
