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

## Parallel run and flaky test policy

```bash
poetry run pytest -n auto --reruns 1 --only-rerun TimeoutError
```

- Only Playwright `TimeoutError` (an action could not complete: slow network, element late)
  is retried, and only once. A failed `expect(...)` raises `AssertionError` and is **never**
  retried: that is a real bug signal, and blanket retries hide it.
- API tests against the shared public Restful-Booker sandbox carry
  `@pytest.mark.flaky(reruns=2)`: the dependency is outside our control.
- The trace of a failed first attempt is kept even if the retry passes, as evidence of flakiness.

## Docker

The image is based on `mcr.microsoft.com/playwright/python` (browsers preinstalled). Its tag
must match the `playwright` package version, set via the `PLAYWRIGHT_VERSION` build arg.

```bash
docker compose run --rm tests
```

Results land in `artifacts/allure-results` and `artifacts/test-results`. On a Linux host
create `artifacts/` before the first run so the container user (`pwuser`) can write to it.

## Debugging a failure

Failed tests attach `playwright-trace.zip` to the Allure report and save it to `test-results/`.
Open it with:

```bash
poetry run playwright show-trace test-results/<test>.zip
```
