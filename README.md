# 🎭 ExpandTesting-2 — UI Automation Test Suite

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-8.3.5-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-1.44+-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![HTML Report](https://img.shields.io/badge/Report-pytest--html-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![Status](https://img.shields.io/badge/Tests-Passing-brightgreen?style=for-the-badge&logo=checkmarx&logoColor=white)

> End-to-end UI automation suite targeting **[practice.expandtesting.com](https://practice.expandtesting.com)**. Built with Python, Pytest and Playwright, following the **Page Object Model** pattern for clean, scalable and maintainable test code.

---

## 📋 Table of Contents

- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Running the Tests](#-running-the-tests)
- [HTML Report](#-html-report)
- [CI/CD Pipeline](#-cicd-pipeline)
- [About Me](#-about-me)

---

## 🛠️ Tech Stack

| Tool | Version | Purpose |
|---|---|---|
| **Python** | 3.11+ | Primary language |
| **Pytest** | 8.3.5 | Test framework and runner |
| **Playwright** | 1.44+ | Browser automation engine |
| **pytest-playwright** | latest | Playwright integration for Pytest |
| **pytest-html** | 4.1.1 | Automatic HTML report generation |
| **Faker** | 37.1.0 | Dynamic test data generation |

---

## 📁 Project Structure

```
ExpandTesting-2/
│
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions pipeline
│
├── pages/                      # Page Object Model (POM) classes
│   ├── __init__.py
│   ├── base_page.py            # Shared locators and browser actions
│   ├── login_page.py           # Login page interactions
│   └── notes_page.py           # Notes dashboard interactions
│
├── tests/
│   ├── conftest.py             # Shared fixtures: browser, page, test data
│   ├── __init__.py
│   └── ui/
│       ├── __init__.py
│       ├── test_login_ui.py    # Login flow test suite
│       └── test_notes_ui.py    # Notes CRUD test suite
│
├── reports/
│   └── report.html             # Auto-generated HTML report
│
├── pytest.ini                  # Pytest config: markers, paths, report output
├── requirements.txt            # Project dependencies
└── README.md
```

**Key files explained:**

- **`pages/`** — Each file maps to a real page on the site. Locators and interactions live here, keeping tests free from implementation details.
- **`conftest.py`** — Provides shared Pytest fixtures: browser setup/teardown, page instances, and Faker-generated user payloads reused across test modules.
- **`pytest.ini`** — Configures test discovery, custom markers (`smoke`, `regression`) and enables the HTML report automatically on every run.
- **`.github/workflows/ci.yml`** — Runs the full test suite on every push and pull request to `main`.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ExpandTesting-2.git
cd ExpandTesting-2
```

### 2. Create and activate a virtual environment

```bash
# Create virtual environment
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

### 4. Install Playwright browsers

```bash
playwright install
```

> This downloads the Chromium, Firefox and WebKit browser binaries required by Playwright.

---

## ▶️ Running the Tests

### Run the full suite (headless by default)

```bash
pytest
```

### Run in headed mode (watch the browser)

```bash
pytest --headed
```

### Run only smoke tests

```bash
pytest -m smoke
```

### Run only regression tests

```bash
pytest -m regression
```

### Run a specific test file

```bash
pytest tests/ui/test_login_ui.py
```

### Run a specific test

```bash
pytest tests/ui/test_login_ui.py::TestLogin::test_login_successful
```

### Run with a specific browser

```bash
pytest --browser firefox
pytest --browser webkit
```

### Run with verbose output

```bash
pytest -v
```

> **Note:** The HTML report is generated automatically on every run — no extra flags needed.

---

## 📊 HTML Report

After any test run, a self-contained HTML report is saved to:

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
- Full tracebacks for any failure
- Environment metadata (Python version, platform, plugins)
- Screenshots on failure *(when configured)*

---

## 🚀 CI/CD Pipeline

This project uses **GitHub Actions** to run the full test suite automatically on every push and pull request to `main`.

![CI](https://img.shields.io/github/actions/workflow/status/your-username/ExpandTesting-2/ci.yml?branch=main&style=for-the-badge&logo=githubactions&logoColor=white&label=CI%20Pipeline&color=brightgreen)

**Pipeline steps:**

1. 🐍 Set up Python 3.11
2. 📦 Install dependencies from `requirements.txt`
3. 🎭 Install Playwright browser binaries
4. ▶️ Run the full test suite with `pytest`
5. 📊 Upload the HTML report as a build artifact

**Example workflow** (`.github/workflows/ci.yml`):

```yaml
name: UI Test Suite

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Install Playwright browsers
        run: playwright install --with-deps

      - name: Run tests
        run: pytest

      - name: Upload HTML report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: html-report
          path: reports/report.html
```

---

## 👤 About Me

Hi! I'm **Miguel**, a **QA Automation Engineer** passionate about building robust and maintainable test frameworks that catch real bugs before they reach production.

I specialize in UI and API test automation using Python-based stacks, with a focus on clean test design, meaningful assertions and the Page Object Model pattern for scalable browser automation. This project reflects my hands-on approach: readable tests, dynamic data, no hardcoded state, and clear reports.

I'm currently **open to new opportunities** — if you're looking for a QA Automation Engineer who cares deeply about test quality and developer experience, let's connect!

📫 Feel free to reach out:

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/your-profile)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/your-username)
[![Email](https://img.shields.io/badge/Email-Contact-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:miguelzod24@gmail.com)

---

<p align="center">Made with ❤️ and lots of <code>pytest --headed</code></p>
