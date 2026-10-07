# SauceDemo E2E Automation Framework

UI and hybrid end-to-end tests for [SauceDemo](https://www.saucedemo.com/)
built with **Python 3.12, Playwright, pytest, Allure**.

## Stack

- Playwright (sync API) + pytest, Page Object Model with components
- Allure reports with steps, failure screenshots and Playwright traces
- pydantic-settings configuration via env vars / `.env`
- Ruff linting and formatting, pre-commit

## Quick start

```bash
poetry install
poetry run playwright install chromium
poetry run pytest -m smoke
```

Run headed in Firefox:

```bash
E2E_BROWSER=firefox E2E_HEADLESS=false poetry run pytest
```

Open the Allure report (requires Allure CLI):

```bash
allure serve allure-results
```

## Debugging a failure

Failed tests attach `playwright-trace.zip` to the Allure report and save it to `test-results/`.
Open it with:

```bash
poetry run playwright show-trace test-results/<test>.zip
```
