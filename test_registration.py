import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

logging.basicConfig(filename="script.log", level=logging.INFO)


def wait_for_element(driver, by, value, timeout=150):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, value))
    )


def test_password_validation(password, expected_error_message):
    # Locate the password field and submit button
    password_field = driver.find_element(By.ID, "password")
    submit_button = driver.find_element(By.ID, "submit")

    # Input the password
    password_field.clear()
    password_field.send_keys(password)

    # Click the submit button
    submit_button.click()

    # Wait for the error message to be displayed
    error_message_element = wait_for_element(driver, By.ID, "passwordHelp", timeout=30)

    # Print the actual error message for debugging
    actual_error_message = error_message_element.text
    print(f"Actual Error Message: {actual_error_message}")

    # Assert the error message
    # Assert the error message
    assert (
        expected_error_message.strip() == actual_error_message.strip()
    ), f"Expected error message not found: {expected_error_message}"

    # Log the result
    if expected_error_message.strip() == actual_error_message.strip():
        logging.info(
            f"Test Passed: Password '{password}' - Expected Error: '{expected_error_message}'"
        )
    else:
        logging.error(
            f"Test Failed: Password '{password}' - Expected Error: '{expected_error_message}' - Actual Error: '{actual_error_message}'"
        )


# Set up WebDriver
service = Service("/Users/kritimathur/Desktop/REGISTRATION_FORM/chromedriver")
driver = webdriver.Chrome(service=service)

# Navigate to the registration page
driver.get("http://localhost:3000/")

# Switch to the newly opened window (if applicable)
if len(driver.window_handles) > 1:
    driver.switch_to.window(driver.window_handles[-1])

# Test cases for password validation:

# Test 1: Valid password
test_password_validation(
    "StrongPassword1#", "Please include at least one uppercase letter."
)

# Test 2: Invalid password (missing uppercase)
test_password_validation(
    "weakpassword1#", "Please include at least one uppercase letter."
)

# Add more test cases for different password scenarios

# Close the browser
driver.quit()
