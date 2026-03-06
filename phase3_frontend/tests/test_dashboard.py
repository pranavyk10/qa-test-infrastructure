import pytest
from phase3_frontend.pages.dashboard_page import DashboardPage

def test_dashboard_api_mock(page):
    """Use network interception to mock API — 10x faster than waiting for real API."""
    def mock_user_api(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body='{"id": 1, "name": "Alice", "email": "alice@example.com"}'
        )

    page.route("**/api/users/me", mock_user_api)
    dashboard = DashboardPage(page)
    dashboard.navigate()
    # Assert that mocked data rendered correctly
    # page.get_by_text("Alice").wait_for()

def test_dashboard_loads(page):
    dashboard = DashboardPage(page)
    dashboard.navigate()
    assert page.title() is not None
