from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
import pytest
import os


def test_pipeline_is_working():
    """Smoke test - proves CI pipeline runs successfully."""
    assert 1 + 1 == 2


def test_page_object_model_structure():
    """Proves LoginPage class is importable and structured correctly."""
    assert hasattr(LoginPage, 'enter_email')
    assert hasattr(LoginPage, 'enter_password')
    assert hasattr(LoginPage, 'tap_login')
    assert hasattr(LoginPage, 'login')
    assert hasattr(LoginPage, 'get_error_message')

# -------------------------------------------------------
# PAGE OBJECT MODEL - LoginPage class
# -------------------------------------------------------

class LoginPage:

    def __init__(self, driver):
        self.driver = driver

    def enter_email(self, email):
        self.driver.find_element(
            AppiumBy.ID, "com.example.app:id/email"
        ).send_keys(email)

    def clear_email(self):
        self.driver.find_element(
            AppiumBy.ID, "com.example.app:id/email"
        ).clear()

    def enter_password(self, password):
        self.driver.find_element(
            AppiumBy.ID, "com.example.app:id/password"
        ).send_keys(password)

    def tap_login(self):
        self.driver.find_element(
            AppiumBy.ID, "com.example.app:id/btn_login"
        ).click()

    def get_error_message(self):
        return self.driver.find_element(
            AppiumBy.ID, "com.example.app:id/error_text"
        ).text

    def is_error_message_displayed(self):
        try:
            element = self.driver.find_element(
                AppiumBy.ID, "com.example.app:id/error_text"
            )
            return element.is_displayed()
        except Exception:
            return False

    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.tap_login()


# -------------------------------------------------------
# SMOKE TEST - proves pipeline works
# Does not need a device or LambdaTest
# -------------------------------------------------------

def test_pipeline_is_working():
    """Smoke test - proves CI pipeline runs successfully."""
    assert 1 + 1 == 2


def test_page_object_model_structure():
    """Proves LoginPage class is importable and structured correctly."""
    assert hasattr(LoginPage, 'enter_email')
    assert hasattr(LoginPage, 'enter_password')
    assert hasattr(LoginPage, 'tap_login')
    assert hasattr(LoginPage, 'login')
    assert hasattr(LoginPage, 'get_error_message')


# -------------------------------------------------------
# TEST CLASS - requires LambdaTest connection
# These run when a real app is connected
# -------------------------------------------------------

class TestLogin:

    def setup_method(self):
        # Read credentials from environment variables
        lt_username = os.environ.get("LT_USERNAME", "")
        lt_access_key = os.environ.get("LT_ACCESS_KEY", "")

        # NEW: Use AppiumOptions - required for Appium v3
        options = UiAutomator2Options()
       

        # LambdaTest capabilities
        options.set_capability("deviceName", "Samsung Galaxy S23")
        options.set_capability("platformVersion", "13")
        options.set_capability("appPackage", "com.example.app")
        options.set_capability("appActivity", ".LoginActivity")
        options.set_capability("automationName", "UiAutomator2")
        options.set_capability("isRealMobile", True)
        options.set_capability("build", "Banking App - Login Tests")
        options.set_capability("name", "Login Screen Regression")
        options.set_capability("video", True)
        options.set_capability("visual", True)
        options.set_capability("network", True)

        # LambdaTest remote URL
        remote_url = (
            f"https://{lt_username}:{lt_access_key}"
            f"@mobile-hub.lambdatest.com/wd/hub"
        )

        self.driver = webdriver.Remote(
            remote_url,
            options=options
        )
        self.driver.implicitly_wait(10)
        self.login_page = LoginPage(self.driver)

    def teardown_method(self):
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

    def test_valid_login_navigates_to_home(self):
        """TC_01 - valid email and password navigates to home."""
        self.login_page.login(
            email="testuser@example.com",
            password="ValidPass123!"
        )
        current_activity = self.driver.current_activity.lower()
        assert "home" in current_activity, (
            f"Expected home screen but got: {current_activity}"
        )

    def test_wrong_password_shows_error_message(self):
        """TC_02 - incorrect password shows error message."""
        self.login_page.login(
            email="testuser@example.com",
            password="WrongPassword!"
        )
        assert self.login_page.is_error_message_displayed(), (
            "Error message should be displayed but was not found"
        )
        actual_error = self.login_page.get_error_message()
        expected_error = "Incorrect password"
        assert actual_error == expected_error, (
            f"Expected: '{expected_error}' "
            f"but got: '{actual_error}'"
        )

    def test_unregistered_email_shows_account_not_found(self):
        """TC_03 - unregistered email shows account not found."""
        self.login_page.login(
            email="nobody@nowhere.com",
            password="AnyPassword123!"
        )
        assert self.login_page.is_error_message_displayed(), (
            "Error message should be displayed but was not found"
        )
        actual_error = self.login_page.get_error_message()
        expected_error = "Account not found"
        assert actual_error == expected_error, (
            f"Expected: '{expected_error}' "
            f"but got: '{actual_error}'"
        )