"""Root fixtures: Playwright lifecycle, isolated contexts, failure artifacts, Page Objects."""

import contextlib
import re
import sys
from collections.abc import Generator
from pathlib import Path
from typing import Any

import allure
import pytest
from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    sync_playwright,
)
from playwright.sync_api import (
    Error as PlaywrightError,
)

from saucedemo.config import Settings, get_settings
from saucedemo.data import load_users, make_customer
from saucedemo.models import Customer, User
from saucedemo.pages import LoginPage

PHASE_REPORTS = pytest.StashKey[dict[str, pytest.TestReport]]()


# ---------- hooks ----------


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """Store setup/call reports on the item so fixtures can see the outcome in teardown."""
    report = yield
    item.stash.setdefault(PHASE_REPORTS, {})[report.when] = report
    return report


def pytest_sessionfinish(session: pytest.Session) -> None:
    """Write Allure environment info (controller process only under xdist)."""
    if hasattr(session.config, "workerinput"):
        return
    allure_dir = session.config.getoption("allure_report_dir", default=None)
    if not allure_dir:
        return

    settings = get_settings()
    env = {
        "Browser": settings.browser,
        "BaseURL": settings.base_url,
        "Headless": settings.headless,
        "Python": sys.version.split()[0],
    }
    Path(allure_dir).mkdir(parents=True, exist_ok=True)
    Path(allure_dir, "environment.properties").write_text(
        "\n".join(f"{key}={value}" for key, value in env.items()), encoding="utf-8"
    )


# ---------- helpers ----------


def _test_failed(request: pytest.FixtureRequest) -> bool:
    reports = request.node.stash.get(PHASE_REPORTS, {})
    return any(report.failed for report in reports.values())


def _artifact_name(node_id: str) -> str:
    # Trimmed to stay under the Windows MAX_PATH limit
    return re.sub(r"[^\w.-]+", "_", node_id)[-150:]


# ---------- infrastructure fixtures ----------


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    with sync_playwright() as playwright:
        # SauceDemo marks elements with data-test, enabling page.get_by_test_id(...)
        playwright.selectors.set_test_id_attribute("data-test")
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright, settings: Settings) -> Generator[Browser, None, None]:
    browser_type = getattr(playwright_instance, settings.browser)
    browser = browser_type.launch(headless=settings.headless, slow_mo=settings.slow_mo)
    yield browser
    browser.close()


@pytest.fixture
def context_options(settings: Settings) -> dict[str, Any]:
    """Extension point: override in a nested conftest to add storage_state, locale, etc."""
    return {
        "base_url": settings.base_url,
        "viewport": {"width": settings.viewport_width, "height": settings.viewport_height},
    }


@pytest.fixture
def context(
    browser: Browser,
    settings: Settings,
    context_options: dict[str, Any],
    request: pytest.FixtureRequest,
) -> Generator[BrowserContext, None, None]:
    """Fresh, isolated context per test, with optional Playwright tracing."""
    context = browser.new_context(**context_options)
    context.set_default_timeout(settings.timeout_ms)

    tracing_enabled = settings.trace_mode != "off"
    if tracing_enabled:
        context.tracing.start(
            title=request.node.nodeid, screenshots=True, snapshots=True, sources=True
        )

    yield context

    if tracing_enabled:
        keep_trace = settings.trace_mode == "on" or _test_failed(request)
        if keep_trace:
            trace_path = settings.artifacts_dir / f"{_artifact_name(request.node.nodeid)}.zip"
            trace_path.parent.mkdir(parents=True, exist_ok=True)
            context.tracing.stop(path=trace_path)
            allure.attach.file(str(trace_path), name="playwright-trace", extension="zip")
        else:
            context.tracing.stop()
    context.close()


@pytest.fixture
def page(
    context: BrowserContext, settings: Settings, request: pytest.FixtureRequest
) -> Generator[Page, None, None]:
    """Page torn down before its context, so the screenshot is taken while the page is alive."""
    page = context.new_page()
    yield page

    if settings.screenshot_on_failure and _test_failed(request):
        # A crashed/closed page must not mask the original test failure
        with contextlib.suppress(PlaywrightError):
            allure.attach(
                page.screenshot(full_page=True),
                name="failure-screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
            allure.attach(page.url, name="url", attachment_type=allure.attachment_type.TEXT)
    page.close()


# ---------- test data ----------


@pytest.fixture(scope="session")
def users(settings: Settings) -> dict[str, User]:
    return load_users(settings.password.get_secret_value())


@pytest.fixture(scope="session")
def standard_user(users: dict[str, User]) -> User:
    return users["standard"]


@pytest.fixture
def customer() -> Customer:
    return make_customer()


# ---------- page objects ----------


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page).open()
