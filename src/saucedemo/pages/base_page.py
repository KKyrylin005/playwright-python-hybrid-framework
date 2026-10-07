"""Base class for all Page Objects: thin, Allure-reported wrappers over Playwright."""

from abc import ABC, abstractmethod
from typing import Self

import allure
from playwright.sync_api import Locator, Page, expect


class BasePage(ABC):
    """Common page behaviour.

    Rules for subclasses:
    - declare locators in ``__init__`` as public attributes (tests may ``expect()`` on them);
    - return ``self`` or the next Page Object from actions (fluent interface);
    - no business assertions here: ``expect`` is used only to synchronise on page load.
    """

    path: str = "/"

    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    @abstractmethod
    def loaded_marker(self) -> Locator:
        """Element whose visibility means the page is ready for interaction."""

    # ---------- navigation ----------

    def open(self) -> Self:
        with allure.step(f"Open {type(self).__name__} ({self.path})"):
            self.page.goto(self.path)
        return self.wait_until_loaded()

    def wait_until_loaded(self) -> Self:
        expect(self.loaded_marker).to_be_visible()
        return self

    # ---------- element wrappers ----------

    @staticmethod
    def click(locator: Locator, name: str) -> None:
        with allure.step(f"Click '{name}'"):
            locator.click()

    @staticmethod
    def fill(locator: Locator, value: str, name: str, *, secret: bool = False) -> None:
        shown = "*****" if secret else value
        with allure.step(f"Fill '{name}' with '{shown}'"):
            locator.fill(value)

    @staticmethod
    def get_text(locator: Locator) -> str:
        return locator.inner_text().strip()

    @staticmethod
    def expect_visible(locator: Locator, name: str) -> None:
        with allure.step(f"Wait for '{name}' to be visible"):
            expect(locator).to_be_visible()
