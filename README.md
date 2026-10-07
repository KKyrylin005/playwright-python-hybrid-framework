# SauceDemo E2E Automation Framework

[![tests](https://github.com/KKyrylin005/playwright-python-hybrid-framework/actions/workflows/tests.yml/badge.svg)](https://github.com/KKyrylin005/playwright-python-hybrid-framework/actions/workflows/tests.yml)
[![Allure report](https://img.shields.io/badge/Allure-report-orange)](https://kkyrylin005.github.io/playwright-python-hybrid-framework/)

UI, hybrid and API end-to-end tests for [SauceDemo](https://www.saucedemo.com/) and
[Restful-Booker](https://restful-booker.herokuapp.com/), built with
**Python 3.12, Playwright, pytest, Allure**.

**Live report:** https://kkyrylin005.github.io/playwright-python-hybrid-framework/

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

Run headed in Firefox (or put the variables into `.env`, see `.env.example`):

```bash
E2E_BROWSER=firefox E2E_HEADLESS=false poetry run pytest
```

```powershell
$env:E2E_BROWSER="firefox"; $env:E2E_HEADLESS="false"; poetry run pytest
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

## CI/CD (GitHub Actions)

| Job | What it does |
|---|---|
| Lint | `poetry check --lock`, ruff lint and format check |
| E2E | UI + hybrid tests in a Chromium / Firefox / WebKit matrix, parallel via xdist |
| API | Restful-Booker tests (separate job: an outage of the public sandbox stays visible but isolated) |
| Docker | Builds the image and runs the smoke suite inside it |
| Allure report | Merges all results, restores trend history from the live site, deploys to GitHub Pages |

The report is published from `main` even when tests fail, which is when it is needed most.
Each browser run appears separately in Allure thanks to the `browser` parameter.

## Docker

The image is based on `mcr.microsoft.com/playwright/python` (browsers preinstalled). Its tag
must match the `playwright` version in `poetry.lock`; the build fails fast if they diverge.
Dependencies are exported from `poetry.lock`, so the image uses exactly the locked versions.

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

> Traces record typed values, including passwords. SauceDemo's credentials are public demo
> values, so publishing traces is fine here; for a real product, authenticate via
> `storage_state` instead of the login form, or keep traces out of public reports.
