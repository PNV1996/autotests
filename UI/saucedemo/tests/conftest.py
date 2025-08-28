import pytest
from playwright.sync_api import sync_playwright
import os
import allure


@pytest.fixture(scope="session")
def browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()
    playwright.stop()


@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


import pytest
import os
import allure


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Выполняем тест
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        if page:
            # 🔥 Снимаем скриншот в байтах и прикрепляем к Allure напрямую
            screenshot_bytes = page.screenshot()
            allure.attach(
                screenshot_bytes,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
