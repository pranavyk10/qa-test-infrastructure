import pytest
from playwright.sync_api import sync_playwright
import json, os

AUTH_STATE_FILE = "phase3_frontend/auth_state.json"

@pytest.fixture(scope="session")
def browser_context_with_auth():
    """
    Saves auth storageState once per session so login is skipped in 90% of tests.
    Replace the login logic below with your app's actual login flow.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        if os.path.exists(AUTH_STATE_FILE):
            context = browser.new_context(storage_state=AUTH_STATE_FILE)
        else:
            context = browser.new_context()
            page = context.new_page()
            # Replace with real login steps:
            # page.goto("https://your-app.com/login")
            # page.fill("#email", "user@example.com")
            # page.fill("#password", "password")
            # page.click("button[type=submit]")
            context.storage_state(path=AUTH_STATE_FILE)
        yield context
        browser.close()

@pytest.fixture
def page(browser_context_with_auth):
    page = browser_context_with_auth.new_page()
    yield page
    page.close()
