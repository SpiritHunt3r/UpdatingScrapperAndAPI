import random
from datetime import datetime

import requests

from constans import (
    __API_URL__,
    __USER__,
    __PASS__
)


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

    return "".join(random.choices("0123456789", k=length))


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

    Args:
        number (str): Numeric string used to calculate the check digit.

    Returns:
        int: Luhn check digit.
    """
    digits = [int(d) for d in number]

    total = 0

    for i, digit in enumerate(reversed(digits)):
        if i % 2 == 0:
            digit *= 2

            if digit > 9:
                digit -= 9

        total += digit

    return (10 - (total % 10)) % 10


def generate_luhn_number(length: int = 16) -> str:
    """
    Generates a valid card number that passes the Luhn algorithm.

    Args:
        length (int, optional): Total length including check digit.
            Defaults to 16.

    Returns:
        str: Luhn-valid card number.

    Raises:
        ValueError: If length is less than 2.
    """
    if length < 2:
        raise ValueError(
            "Length must be at least 2."
        )

    prefix = "".join(
        str(random.randint(0, 9))
        for _ in range(length - 1)
    )

    return prefix + str(
        calculate_luhn_check_digit(prefix)
    )


def handle_error(
    response: requests.Response
) -> None:
    """
    Prints a user-friendly error message based on the API response.

    Args:
        response (requests.Response): HTTP response object.

    Returns:
        None
    """
    if response.status_code == 400:
        print(
            f"Validation error: {response.text}"
        )

    elif response.status_code == 401:
        print(
            f"Authentication failed: {response.text}"
        )

    elif response.status_code == 429:
        print(
            "Rate limit exceeded "
            "(30 requests per minute)."
        )

    else:
        print(
            f"Request failed. "
            f"Status: {response.status_code} "
            f"Response: {response.text}"
        )


def get_access_token(
    email: str,
    password: str
) -> str | None:
    """
    Performs the two-step authentication flow and returns a bearer token.

    Authentication flow:
        1. POST /auth/token
        2. POST /auth/mfa/verify

    Args:
        email (str): User email.
        password (str): User password.

    Returns:
        str | None: Access token if authentication succeeds,
        otherwise None.
    """
    try:
        auth_response = requests.post(
            f"{__API_URL__}/auth/token",
            json={
                "email": email,
                "password": password
            },
            timeout=30
        )

        if auth_response.status_code != 200:
            handle_error(auth_response)
            return None

        auth_data = auth_response.json()

        mfa_token = auth_data["mfa_token"]

        mfa_response = requests.post(
            f"{__API_URL__}/auth/mfa/verify",
            json={
                "mfa_token": mfa_token,
                "code": "1234"
            },
            timeout=30
        )

        if mfa_response.status_code != 200:
            handle_error(mfa_response)
            return None

        return mfa_response.json()["access_token"]

    except requests.exceptions.RequestException as e:
        print(
            f"Authentication request failed: {e}"
        )
        return None


def update_banking(
    token: str,
    routing_number: str,
    account_number: str
) -> bool:
    """
    Updates the user's banking information.

    Args:
        token (str): Bearer token.
        routing_number (str): Routing number.
        account_number (str): Account number.

    Returns:
        bool: True if the update succeeds,
        otherwise False.
    """
    try:
        response = requests.put(
            f"{__API_URL__}/account/banking",
            headers={
                "Authorization": f"Bearer {token}"
            },
            json={
                "routing_number": routing_number,
                "account_number": account_number
            },
            timeout=30
        )

        if response.status_code != 200:
            handle_error(response)
            return False

        result = response.json()

        print(
            f"Banking Updated: "
            f"{result['routing_masked']} | "
            f"{result['account_masked']}"
        )

        return True

    except requests.exceptions.RequestException as e:
        print(
            f"Banking update failed: {e}"
        )
        return False


def update_payment(
    token: str,
    cardholder_name: str,
    card_number: str,
    exp_month: int,
    exp_year: int,
    cvc: str
) -> bool:
    """
    Updates the user's payment method.

    Args:
        token (str): Bearer token.
        cardholder_name (str): Name displayed on the card.
        card_number (str): Card number.
        exp_month (int): Expiration month.
        exp_year (int): Expiration year.
        cvc (str): Card security code.

    Returns:
        bool: True if the update succeeds,
        otherwise False.
    """
    try:
        response = requests.put(
            f"{__API_URL__}/account/payment",
            headers={
                "Authorization": f"Bearer {token}"
            },
            json={
                "cardholder_name": cardholder_name,
                "card_number": card_number,
                "exp_month": exp_month,
                "exp_year": exp_year,
                "cvc": cvc
            },
            timeout=30
        )

        if response.status_code != 200:
            handle_error(response)
            return False

        result = response.json()

        print(
            f"Payment Updated: "
            f"{result['card_brand']} "
            f"****{result['last4']} "
            f"{result['exp_month']}/{result['exp_year']}"
        )

        return True

    except requests.exceptions.RequestException as e:
        print(
            f"Payment update failed: {e}"
        )
        return False


def main() -> None:
    """
    Executes the complete API workflow.

    Workflow:
        1. Authenticate using configured credentials.
        2. Complete MFA verification.
        3. Generate randomized banking data.
        4. Generate randomized payment data.
        5. Update banking information.
        6. Update payment information.

    Returns:
        None
    """
    token = get_access_token(
        email=__USER__,
        password=__PASS__
    )

    if not token:
        return

    routing_number = generate_random_number(9)

    account_number = generate_random_number(
        generate_random_number_between(4, 17)
    )

    card_number = generate_luhn_number()

    exp_month = generate_random_number_between(
        1,
        12
    )

    exp_year = (
        datetime.now().year +
        generate_random_number_between(
            1,
            5
        )
    )

    cvc = generate_random_number(
        generate_random_number_between(
            3,
            4
        )
    )

    update_banking(
        token=token,
        routing_number=routing_number,
        account_number=account_number
    )

    update_payment(
        token=token,
        cardholder_name="Test User",
        card_number=card_number,
        exp_month=exp_month,
        exp_year=exp_year,
        cvc=cvc
    )


if __name__ == "__main__":
    main()

