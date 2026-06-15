# Account Update Automation Challenge

Python automation project combining Selenium UI automation and REST API testing to update and validate banking and payment account information through MFA-secured workflows.

---

## Overview

This project implements the same business workflow using two different automation approaches:

### UI Automation

Built with Selenium WebDriver to simulate real user interactions through the web application.

### API Automation

Built with Python Requests to directly interact with the published REST API.

Both implementations:

* Authenticate the user
* Complete MFA verification
* Generate randomized banking information
* Generate randomized payment information
* Submit updates
* Validate successful execution
* Handle common error scenarios

---

## Environment

This solution was developed and tested using:

| Component        | Version                   |
| ---------------- | ------------------------- |
| Operating System | Windows 11                |
| Python           | 3.14                      |
| Browser          | Google Chrome             |
| Selenium         | Latest Compatible Version |
| Requests         | Latest Compatible Version |

---

## Project Structure

```text
.
├── WebScrepping.py      # Selenium UI automation
├── ApiClient.py         # REST API automation
├── constans.py          # Configuration and locators
├── requirements.txt
└── README.md
```

---

## Features

### Selenium UI Automation

The UI automation performs the following workflow:

1. Open the login page.
2. Authenticate using configured credentials.
3. Complete MFA verification.
4. Navigate to the account settings page.
5. Update banking information.
6. Update payment information.
7. Validate that updates were successfully applied.
8. Display validation results.

---

### REST API Automation

The API automation performs the following workflow:

1. Authenticate through the API.
2. Complete MFA verification.
3. Generate random banking information.
4. Generate random payment information.
5. Update banking details.
6. Update payment details.
7. Print masked confirmation values returned by the API.
8. Handle common API errors.

---

## Authentication Flow

The application uses a two-step authentication process.

### Step 1

Request:

```http
POST /auth/token
```

Response:

```json
{
  "mfa_required": true,
  "mfa_token": "mfa_xxxxx"
}
```

### Step 2

Request:

```http
POST /auth/mfa/verify
```

Response:

```json
{
  "access_token": "xxxxx"
}
```

The access token is then used as:

```http
Authorization: Bearer <token>
```

for all protected endpoints.

---

## Installation

### Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the virtual environment

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### Install dependencies

```bash
pip install selenium && pip install requests
```

---

## Requirements

The project requires:

```txt
selenium
requests
```

---

## Configuration

Before executing the automation, update the values in `constans.py`.

### Credentials

```python
__USER__ = ""  # Fill before executing
__PASS__ = ""  # Fill before executing
```

### Application URLs

```python
__URL__ = "https://marketplace.dev-challenge.com/login"
__API_URL__ = "https://zvyhufnwclhcvmgtqxwp.supabase.co/functions/v1/api-v1"
```

### User Information

```python
__USER_NAME__ = "JUAN JOSE ARAYA CASTRO"
```

### Selenium Locators

The file also contains all XPath locators used by the UI automation.

Examples:

```python
__USER_INPUT__ = '//*[@id="email"]'
__PASS_INPUT__ = '//*[@id="password"]'
__LOGIN_BTN__ = '//*[@id="root"]/div[2]/div/form/button'
```

Centralizing locators allows updates to the UI without modifying the automation logic.

---

## Running the Selenium Automation

Execute:

```bash
python WebScrepping.py
```

The script will:

* Open the browser
* Authenticate
* Complete MFA
* Update banking information
* Update payment information
* Validate updates
* Display results

---

## Running the API Automation

Execute:

```bash
python ApiClient.py
```

The script will:

* Authenticate through the API
* Complete MFA verification
* Generate random test data
* Update banking details
* Update payment details
* Display confirmation values returned by the API

---

## Example Output

### Banking Update

```text
Banking Updated: •••••0021 | ••••••7890
```

### Payment Update

```text
Payment Updated: visa ****4242 12/2027
```

---

## Error Handling

The API implementation handles:

### Authentication Errors

```text
Authentication failed.
```

### Validation Errors

```text
Validation error.
```

### Rate Limiting

```text
Rate limit exceeded (30 requests per minute).
```

### Network Failures

```text
Authentication request failed: <error details>
```

---

## Test Data Generation

The project generates randomized data for every execution.

### Banking Data

* Routing Number
* Account Number

### Payment Data

* Card Number (Luhn Valid)
* Expiration Month
* Expiration Year
* CVC

Helper functions include:

* Random numeric generation
* Random range generation
* Luhn card generation
* Dynamic expiration date generation

---

## Design Decisions

### Why Selenium?

Selenium was used to validate the complete user journey through the browser and verify that UI updates are reflected correctly.

### Why API Testing?

API automation is significantly faster, more reliable, and less dependent on UI changes.

Testing both approaches demonstrates validation of the same workflow at different layers of the application.

---

## Potential Improvements

The current implementation contains utility methods duplicated across both automation scripts.

Examples:

* Random number generation
* Random range generation
* Luhn card generation
* Validation helpers
* Error handling helpers

A better architecture would be:

```text
.
├── utils/
│   ├── data_generator.py
│   ├── api_helpers.py
│   ├── selenium_helpers.py
│   └── validators.py
├── constans.py
├── WebScrepping.py
├── ApiClient.py
```

Benefits:

* Reduced code duplication
* Easier maintenance
* Better readability
* Improved testability
* Easier future enhancements

---

## Future Enhancements

Possible improvements include:

* Environment variable support for credentials
* Structured logging
* Unit tests
* Retry logic for transient failures
* Configuration management
* Page Object Model implementation for Selenium
* Shared utility package

---

## Notes

This project was created as an automation challenge solution demonstrating both UI automation and API automation against the same application workflow.

The API implementation is the preferred approach when API access is available because it provides faster execution, greater reliability, and easier maintenance compared to UI automation.
