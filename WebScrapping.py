from constans import (
    __URL__,
    __USER__,
    __USER_INPUT__,
    __PASS__,
    __PASS_INPUT__,
    __LOGIN_BTN__,
    __MFA_INPUT__,
    __MFA_BTN__,
    __ACCOUNT_BTN__,
    __USER_NAME__,
    __ROUTING_INPUT__,
    __ACCOUNT_NUM_INPUT__ ,
    __CARD_HOLDER_INPUT__,
    __CARD_NUMBER_INPUT__ ,
    __MONTH_INPUT__ ,
    __YEAR_INPUT__,
    __CVC_INPUT__,
    __BACKING_BTN__,
    __PAYMENT_BTN__,
    __BANKING_TXT__,
    __PAYMENT_TXT__
)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from datetime import datetime
import time


def send_keys_to_element(
    driver: WebDriver,
    xpath: str,
    text: str
) -> bool:
    """
    Sends a string to an element identified by an XPath locator.

    Args:
        driver (WebDriver): Active Selenium WebDriver instance.
        xpath (str): XPath locator of the target element.
        text (str): Text to send.

    Returns:
        bool: True if the text was sent successfully, otherwise False.
    """
    try:
        driver.find_element(By.XPATH, xpath).send_keys(text)
        return True

    except Exception as e:
        print(f"Failed to send keys: {e}")
        return False

def wait_and_click(
    driver: WebDriver,
    xpath: str,
    timeout: int = 10
) -> bool:
    """
    Waits until an element is clickable and performs a click.

    Args:
        driver (WebDriver): Active Selenium WebDriver instance.
        xpath (str): XPath locator of the clickable element.
        timeout (int, optional): Maximum wait time in seconds.

    Returns:
        bool: True if the element was clicked successfully,
        otherwise False.
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.click()
        return True

    except Exception as e:
        print(f"Failed to click element: {e}")
        return False


def open_browser(url: str) -> WebDriver:
    """
    Opens a Chrome browser instance and navigates to the specified URL.

    Args:
        url (str): The URL to open in the browser.

    Returns:
        WebDriver: An initialized Selenium WebDriver instance.

    Raises:
        No exceptions are propagated. Any exception should be handled by
        the caller if browser initialization fails.
    """
    driver = webdriver.Chrome()
    driver.get(url)
    return driver


def ingest_vals_inputs(
    driver: WebDriver,
    value: str,
    xpath: str
) -> bool:
    """
    Locates an input element using an XPath expression and enters a value.

    The target element is cleared before the provided value is entered.

    Args:
        driver (WebDriver): Active Selenium WebDriver instance.
        value (str): Value to enter into the input field.
        xpath (str): XPath locator of the target input element.

    Returns:
        bool: True if the value was entered successfully, otherwise False.
    """
    try:
        element = driver.find_element(By.XPATH, xpath)
        element.clear()
        element.send_keys(value)
        return True

    except Exception as e:
        print(f"Failed to enter value: {e}")
        return False


def click_button(
    driver: WebDriver,
    xpath: str
) -> bool:
    """
    Locates a clickable element using an XPath expression and performs a click.

    Args:
        driver (WebDriver): Active Selenium WebDriver instance.
        xpath (str): XPath locator of the button or clickable element.

    Returns:
        bool: True if the click action was successful, otherwise False.
    """
    try:
        element = driver.find_element(By.XPATH, xpath)
        element.click()
        return True

    except Exception as e:
        print(f"Failed to click element: {e}")
        return False
    

def generate_random_number(length: int) -> str:
    """
    Generates a random numeric string of the specified length.

    Args:
        length (int): Number of digits to generate.

    Returns:
        str: A random numeric string of the requested length.

    Raises:
        ValueError: If length is less than 1.
    """
    if length < 1:
        raise ValueError("Length must be greater than 0.")

    return ''.join(random.choices('0123456789', k=length))


def generate_random_number_between(
    min_value: int,
    max_value: int
) -> int:
    """
    Generates a random integer within the specified range.

    Args:
        min_value (int): Minimum value (inclusive).
        max_value (int): Maximum value (inclusive).

    Returns:
        int: A random integer between min_value and max_value.

    Raises:
        ValueError: If min_value is greater than max_value.
    """
    if min_value > max_value:
        raise ValueError(
            "min_value must be less than or equal to max_value."
        )

    return random.randint(min_value, max_value)

def calculate_luhn_check_digit(number: str) -> int:
    """
    Calculates the Luhn check digit for a numeric string.
    """
    digits = [int(d) for d in number]

    total = 0
    reverse_digits = digits[::-1]

    for i, digit in enumerate(reverse_digits):
        if i % 2 == 0:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit

    return (10 - (total % 10)) % 10

def generate_luhn_number(length: int = 16) -> str:
    """
    Generates a random number that passes the Luhn check.

    Args:
        length (int): Total length including check digit.

    Returns:
        str: A Luhn-valid number.
    """
    if length < 2:
        raise ValueError("Length must be at least 2.")

    prefix = ''.join(
        str(random.randint(0, 9))
        for _ in range(length - 1)
    )

    check_digit = calculate_luhn_check_digit(prefix)

    return prefix + str(check_digit)

def get_text(
    driver: WebDriver,
    xpath: str
) -> str | None:
    """
    Retrieves the visible text from an element identified by an XPath expression.

    Args:
        driver (WebDriver): Active Selenium WebDriver instance.
        xpath (str): XPath locator of the target element.

    Returns:
        str | None: The element's text if found, otherwise None.
    """
    try:
        element = driver.find_element(By.XPATH, xpath)
        return element.text.strip()

    except Exception as e:
        print(f"Failed to get text from element: {e}")
        return None
    

def __main__():
    """
    Executes the end-to-end account update automation workflow.

    Workflow:
        1. Open the application.
        2. Authenticate using username, password, and MFA.
        3. Navigate to the account settings page.
        4. Generate randomized banking and payment information.
        5. Update and save banking details.
        6. Update and save payment details.
        7. Validate that the updates were successfully applied.
        8. Display validation results and close the browser.

    Returns:
        None
    """
    # Launch browser and navigate to the target application
    driver = open_browser(__URL__)

    # Populate login credentials
    ingest_vals_inputs(driver, __USER__, __USER_INPUT__)
    ingest_vals_inputs(driver, __PASS__, __PASS_INPUT__)

    # Submit login request
    click_button(driver, __LOGIN_BTN__)

    # Wait for the MFA field to become available
    wait_and_click(driver, __MFA_INPUT__)

    # Generate and enter a random MFA code
    send_keys_to_element(driver, __MFA_INPUT__, generate_random_number(4))

    # Submit MFA verification
    click_button(driver, __MFA_BTN__)

    # Navigate to the account management section
    click_button(driver, __ACCOUNT_BTN__)

    # Generate randomized banking and payment information
    routing_number = generate_random_number(9)
    account_number = generate_random_number(generate_random_number_between(4,17))
    card_holder = __USER_NAME__
    card_number = generate_luhn_number()
    month = generate_random_number_between(1,12)
    year  = datetime.now().year + generate_random_number_between(1,5)
    cvc = generate_random_number(generate_random_number_between(3,4))

    # Update banking information
    ingest_vals_inputs(driver, routing_number,__ROUTING_INPUT__)
    ingest_vals_inputs(driver, account_number,__ACCOUNT_NUM_INPUT__)

    # Save banking information
    click_button(driver, __BACKING_BTN__)

    # Update payment card information
    ingest_vals_inputs(driver, card_holder,__CARD_HOLDER_INPUT__)
    ingest_vals_inputs(driver, card_number,__CARD_NUMBER_INPUT__)
    ingest_vals_inputs(driver, month,__MONTH_INPUT__)
    ingest_vals_inputs(driver, year,__YEAR_INPUT__)
    ingest_vals_inputs(driver, cvc,__CVC_INPUT__)

    # Save payment information
    click_button(driver, __PAYMENT_BTN__)

    # Build expected validation values for verification
    routing_validator = str(routing_number)[-4:]
    account_validator = str(account_number)[-4:]
    card_validator = str(card_number)[-4:]
    expired_validator = f'{month}/{year}'

    # Allow the application time to persist and display updates
    time.sleep(2)

    # Retrieve the most recently displayed banking and payment details
    last_banking = get_text(driver, __BANKING_TXT__)
    last_payment = get_text(driver, __PAYMENT_TXT__)

    # Verify that the banking information was updated successfully
    print(
        "Banking Details Updated Correctly"
        if routing_validator in last_banking and account_validator in last_banking
        else "Banking Details was not updated"
    )

    # Verify that the payment information was updated successfully
    print(
        "Payment Updated Correctly"
        if card_validator in last_payment and expired_validator in last_payment
        else "Payment was not updated"
    )

    # Pause execution so the user can visually inspect the browser
    input()

    # Close the browser session
    driver.quit()


__main__()