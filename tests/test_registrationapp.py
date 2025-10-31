import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
import subprocess
import time
import requests
import os
import signal
import re

# ------------------------------------------------------------
# Fixture: Start Flask app before all tests and stop after
# ------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def start_flask_app():
    """Start the Flask app before running tests and stop it afterwards."""
    print("🚀 Starting Flask app...")

    process = subprocess.Popen(
        ["python", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP  # Windows compatible
    )

    # Wait for Flask to start
    for i in range(15):
        try:
            requests.get("http://127.0.0.1:5000")
            print("✅ Flask app is running.")
            break
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    else:
        stderr = process.stderr.read()
        print("❌ Flask failed to start.\nError Log:\n", stderr.decode())
        process.kill()
        pytest.fail("Flask app did not start properly.")

    yield  # Run the tests

    # Stop Flask app after tests
    print("🛑 Shutting down Flask app...")
    try:
        process.send_signal(signal.CTRL_BREAK_EVENT)
        time.sleep(2)
        process.kill()
        print("✅ Flask app stopped.")
    except Exception as e:
        print(f"⚠️ Error stopping Flask app: {e}")


# ------------------------------------------------------------
# Fixture: Selenium WebDriver setup/teardown
# ------------------------------------------------------------
@pytest.fixture
def setup_teardown():
    """Setup and teardown for Selenium WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # Try detecting Chrome version (optional for logging)
    try:
        result = subprocess.run(
            [
                "powershell",
                "-Command",
                '(Get-Item "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe").VersionInfo.ProductVersion'
            ],
            capture_output=True, text=True
        )
        chrome_version = re.match(r"(\d+)", result.stdout.strip()).group(1)
        print(f"🧩 Detected Chrome major version: {chrome_version}")
    except Exception as e:
        print(f"⚠️ Could not detect Chrome version: {e}")

    # ✅ Use auto-managed ChromeDriver (no version argument)
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()),
        options=chrome_options
    )

    yield driver
    driver.quit()


# ------------------------------------------------------------
# Helper: Handle alert safely
# ------------------------------------------------------------
def get_alert_text(driver):
    alert = Alert(driver)
    text = alert.text
    alert.accept()
    return text


# ------------------------------------------------------------
# Tests
# ------------------------------------------------------------

def test_empty_username(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "pwd").send_keys("Password123")
    driver.find_element(By.NAME, "sb").click()
    time.sleep(1)
    assert get_alert_text(driver) == "Username cannot be empty."


def test_empty_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "username").send_keys("John Doe")
    driver.find_element(By.NAME, "pwd").clear()
    driver.find_element(By.NAME, "sb").click()
    time.sleep(1)
    assert get_alert_text(driver) == "Password cannot be empty."


def test_short_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "username").send_keys("Jane")
    driver.find_element(By.NAME, "pwd").send_keys("abc1")
    driver.find_element(By.NAME, "sb").click()
    time.sleep(1)
    assert get_alert_text(driver) == "Password must be atleast 6 characters long."


def test_valid_input(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "username").send_keys("Alice")
    driver.find_element(By.NAME, "pwd").send_keys("abc123")
    driver.find_element(By.NAME, "sb").click()
    time.sleep(2)
    assert "/submit" in driver.current_url
    assert "Hello, Alice! Welcome to the website" in driver.find_element(By.TAG_NAME, "body").text
