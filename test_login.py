# -------------------------------------------------------
# FILE: test_login.py
# PURPOSE: Automated tests for the mobile banking app
#          login screen using Appium + Pytest
#          UPDATED: Now runs on LambdaTest cloud
#          instead of a local emulator
# -------------------------------------------------------

# Import the Appium driver - this is what controls the phone
from appium import webdriver

# Import AppiumBy - this is how we find elements on screen
from appium.webdriver.common.appiumby import AppiumBy

# Import pytest - the test framework that runs our tests
import pytest

# NEW: Import os - this lets us read environment variables
# Environment variables are how we store secrets safely
# Your LambdaTest username and key live here, not in the code
import os


# -------------------------------------------------------
# PAGE OBJECT MODEL - LoginPage class
# -------------------------------------------------------
# UNCHANGED - this is exactly as before
# This is why Page Object Model is powerful -
# the page class never needs to change when you
# switch from local to cloud
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
        except:
            return False

    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.tap_login()


# -------------------------------------------------------
# TEST CLASS
# -------------------------------------------------------

class TestLogin:

    def setup_method(self):
        # -----------------------------------------------
        # CHANGED: This is the only section that changed
        # Everything below replaces the local emulator
        # setup with LambdaTest cloud setup
        # -----------------------------------------------

        # CHANGE 1: Read credentials from environment variables
        # os.environ["LT_USERNAME"] reads a variable you set
        # on your computer or in GitHub Secrets
        # It is NEVER written directly in the code
        # If someone sees your code, they cannot steal your key
        lt_username = os.environ["LT_USERNAME"]
        lt_access_key = os.environ["LT_ACCESS_KEY"]

        # CHANGE 2: LambdaTest capabilities
        # These tell LambdaTest which real device to use
        # and how to set up the test session
        caps = {
            # --- Device settings ---
            "platformName": "Android",
            "deviceName": "Samsung Galaxy S23",  # Real physical device
            "platformVersion": "13",             # Android 13

            # --- App settings (unchanged from before) ---
            "appPackage": "com.example.app",
            "appActivity": ".LoginActivity",
            "automationName": "UiAutomator2",

            # --- LambdaTest specific settings ---
            # NEW: tells LambdaTest to use a real device
            # not a simulator
            "isRealMobile": True,

            # NEW: groups your test runs in the dashboard
            # so you can find them easily
            "build": "Banking App - Login Tests",
            "name": "Login Screen Regression Suite",

            # NEW: enables extra logging and media capture
            # you can watch your test run as a video
            "network": True,    # Captures network logs
            "visual": True,     # Takes screenshots on failure
            "video": True,      # Records full video of the run
            "console": True     # Captures browser console logs
        }

        # CHANGE 3: Remote URL now points to LambdaTest
        # instead of localhost on your machine
        # Your credentials are embedded in the URL securely
        # using f-string formatting
        remote_url = (
            f"https://{lt_username}:{lt_access_key}"
            f"@mobile-hub.lambdatest.com/wd/hub"
        )

        # CHANGE 4: webdriver.Remote now uses LambdaTest URL
        # instead of "http://localhost:4723/wd/hub"
        # Everything else is the same
        self.driver = webdriver.Remote(
            remote_url,
            caps
        )

        # Unchanged - wait up to 10 seconds for elements
        self.driver.implicitly_wait(10)

        # Unchanged - create the LoginPage object
        self.login_page = LoginPage(self.driver)

    def teardown_method(self):
        # UNCHANGED - still closes the session after each test
        # LambdaTest will mark the session as complete
        if self.driver:
            self.driver.quit()


    # -----------------------------------------------
    # ALL 3 TESTS BELOW ARE 100% UNCHANGED
    # This proves the power of Page Object Model -
    # switch from local to cloud by changing only
    # setup_method above, nothing else
    # -----------------------------------------------

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