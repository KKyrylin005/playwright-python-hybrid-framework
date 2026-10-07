# SauceDemo E2E Automation Framework

UI and hybrid end-to-end tests for [SauceDemo](https://www.saucedemo.com/)
built with **Python 3.12, Playwright, pytest, Allure**.

## Stack

- Playwright (sync API) + pytest, Page Object Model with components
- Allure reports with steps, failure screenshots and Playwright traces
- pydantic-settings configuration via env vars / `.env`
- Ruff linting and formatting, pre-commit

## Test layers

| Folder | Marker | What it shows |
|---|---|---|
| `tests/ui` | `ui` | Pure UI journeys through the real forms (login, sorting, checkout) |
| `tests/hybrid` | `hybrid` | Session cookie + cart injected via `storage_state`, UI used only for verification |
| `tests/api` | `api` | Restful-Booker CRUD via `playwright.request`, pydantic schema validation |

Pre-fill the cart in a hybrid test with a marker:

```python
@pytest.mark.cart("Sauce Labs Backpack", "Sauce Labs Bike Light")
def test_checkout(page): ...
```

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
