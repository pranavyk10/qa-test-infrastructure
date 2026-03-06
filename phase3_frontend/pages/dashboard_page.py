from playwright.sync_api import Page

class DashboardPage:
    """Page Object Model for the User Dashboard."""
    URL = "https://your-app.com/dashboard"  # Replace with your app URL

    def __init__(self, page: Page):
        self.page = page
        # All selectors are centralized here — change once, fixes all tests
        self.welcome_header = page.get_by_role("heading", name="Welcome")
        self.logout_button = page.get_by_role("button", name="Logout")
        self.profile_link = page.get_by_role("link", name="Profile")
        self.settings_link = page.get_by_role("link", name="Settings")

    def navigate(self):
        self.page.goto(self.URL)

    def logout(self):
        self.logout_button.click()

    def go_to_profile(self):
        self.profile_link.click()
