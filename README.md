# 🧪 ExpandTesting API — Automated Test Suite

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-8.3.5-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-2.32.3-FF6F00?style=for-the-badge&logo=python&logoColor=white)
![Faker](https://img.shields.io/badge/Faker-37.1.0-00C897?style=for-the-badge)
![HTML Report](https://img.shields.io/badge/Report-pytest--html-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-19%20passing-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

> A professional API test automation suite targeting the [ExpandTesting Notes API](https://practice.expandtesting.com/notes/api). Covers health checks, user registration, and authentication flows with auto-generated test data and a full HTML report.

---

## 📋 Table of Contents

- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Running the Tests](#-running-the-tests)
- [HTML Report](#-html-report)
- [Test Suites](#-test-suites)
- [About Me](#-about-me)

---

## 🛠️ Tech Stack

| Tool | Version | Purpose |
|---|---|---|
| **Python** | 3.11+ | Core language |
| **Pytest** | 8.3.5 | Test framework & test runner |
| **Requests** | 2.32.3 | HTTP client for API calls |
| **Faker** | 37.1.0 | Dynamic test data generation |
| **pytest-html** | 4.1.1 | Automatic HTML report generation |
| **python-dotenv** | 1.1.0 | Environment variable management |

---

## 📁 Project Structure

```
ExpandTesting-API/
│
├── tests/
│   ├── conftest.py            # Shared fixtures: base URL, HTTP session, Faker, payloads
│   └── api/
│       └── test_notes_api.py  # All test suites (Health, Register, Login)
│
├── reports/
│   └── report.html            # Auto-generated HTML test report
│
├── pytest.ini                 # Pytest configuration: markers, paths, report output
├── requirements.txt           # Project dependencies
└── README.md
```

**Key files explained:**

- **`conftest.py`** — Defines reusable fixtures shared across all tests: the base URL, a persistent `requests.Session`, a `Faker` instance, user payloads, and a `registered_user` fixture that pre-registers a user in the API before a test runs.
- **`test_notes_api.py`** — Contains the three test classes (`TestHealth`, `TestUserRegister`, `TestUserLogin`) with 19 tests in total.
- **`pytest.ini`** — Configures test discovery, custom markers (`smoke`, `regression`), and enables automatic HTML reporting on every run.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ExpandTesting-API.git
cd ExpandTesting-API
```

### 2. Create and activate a virtual environment

```bash
# Create the virtual environment
python -m venv venv

# Activate — macOS / Linux
source venv/bin/activate

# Activate — Windows (PowerShell)
venv\Scripts\Activate.ps1

# Activate — Windows (CMD)
venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Tests

### Run the full suite

```bash
pytest
```

### Run only smoke tests (health check)

```bash
pytest -m smoke
```

### Run only regression tests (register + login)

```bash
pytest -m regression
```

### Run a specific test class

```bash
pytest tests/api/test_notes_api.py::TestUserLogin
```

### Run a single test

```bash
pytest tests/api/test_notes_api.py::TestUserRegister::test_register_successful_returns_201
```

### Run with verbose output

```bash
pytest -v
```

> **Note:** The HTML report is generated automatically on every run (configured in `pytest.ini`). No extra flags needed.

---

## 📊 HTML Report

After any test run, a self-contained HTML report is generated at:

```
reports/report.html
```

Open it in any browser:

```bash
# macOS
open reports/report.html

# Linux
xdg-open reports/report.html

# Windows
start reports/report.html
```

The report includes:
- ✅ Pass / ❌ Fail status per test
- Execution time per test and total duration
- Full traceback for any failures
- Environment metadata (Python version, platform, plugins)

---

## 🧩 Test Suites

### 🟢 `TestHealth` — `@pytest.mark.smoke` (4 tests)

Validates that the API is up and responding correctly. These are the fastest tests and run first.

| Test | What it verifies |
|---|---|
| `test_health_status_code_is_200` | `GET /health-check` returns HTTP 200 |
| `test_health_response_is_json` | Response body is a valid JSON object |
| `test_health_response_contains_success_true` | JSON body contains `"success": true` |
| `test_health_response_contains_message` | JSON body contains a non-empty `"message"` string |

---

### 🟡 `TestUserRegister` — `@pytest.mark.regression` (8 tests)

Covers the full registration flow including happy path, data validation, security checks, and error handling. Each test uses Faker to generate a unique user, avoiding conflicts.

| Test | What it verifies |
|---|---|
| `test_register_successful_returns_201` | `POST /users/register` returns HTTP 201 |
| `test_register_response_is_json` | Response is a valid JSON object |
| `test_register_response_contains_success_true` | Response includes `"success": true` |
| `test_register_response_contains_user_data` | Response `data` includes correct `email` and `name` |
| `test_register_response_does_not_expose_password` | Password is **not** present anywhere in the response (security check) |
| `test_register_duplicate_email_returns_409` | Re-registering the same email returns HTTP 409 Conflict |
| `test_register_missing_email_returns_400` | Payload without `email` returns HTTP 400 Bad Request |
| `test_register_missing_password_returns_400` | Payload without `password` returns HTTP 400 Bad Request |

---

### 🔵 `TestUserLogin` — `@pytest.mark.regression` (7 tests)

Validates the authentication flow. Relies on the `registered_user` fixture to ensure a valid user exists before login tests execute.

| Test | What it verifies |
|---|---|
| `test_login_successful_returns_200` | `POST /users/login` with valid credentials returns HTTP 200 |
| `test_login_response_contains_token` | Successful login returns a non-empty auth `token` |
| `test_login_response_contains_user_info` | Response `data` contains the authenticated user's `email` |
| `test_login_wrong_password_returns_401` | Correct email + wrong password returns HTTP 401 Unauthorized |
| `test_login_nonexistent_email_returns_401` | Login with an unregistered email returns HTTP 401 |
| `test_login_missing_email_returns_400` | Payload without `email` returns HTTP 400 Bad Request |
| `test_login_missing_password_returns_400` | Payload without `password` returns HTTP 400 Bad Request |

---

## 👤 About Me

Hi! I'm **Miguel**, a **QA Automation Engineer** passionate about building robust, maintainable test frameworks that catch real bugs before they reach production.

I specialize in API test automation using Python-based stacks, with a focus on clean test design, meaningful assertions, and reliable test data strategies. This project reflects my approach to API testing: isolated tests, dynamic data, zero hardcoded state, and clear reporting.

📫 Feel free to connect or reach out!

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/your-profile)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/your-username)

---

<p align="center">Made with ❤️ and lots of <code>pytest -v</code></p>
