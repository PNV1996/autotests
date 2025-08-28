import pytest
import time
from playwright.sync_api import sync_playwright


from UI.saucedemo.Pages.checkout_page import CheckoutPage
from UI.saucedemo.Pages.inventory_page import InventoryPage
from UI.saucedemo.Pages.login_page import LoginPage
from utils.logger import get_logger

logger = get_logger("TestCheckout")


@pytest.mark.parametrize(
    "username, password, first_name, last_name, postal_code",
    [
        ("standard_user", "secret_sauce", "Jon", "Doe", "234235"),
        ("standard_user", "secret_sauce1", "Brad", "Smith", "435345"),
        ("locked_out_user", "secret_sauce", "Senen", "Hill", "345"),
        # ("problem_user", "secret_sauce", "Niko", "Smith", "345"),
        # ("performance_glitch_user", "secret_sauce", "Brad", "Smith", "123456"),
        # ("error_user", "secret_sauce", "Alice", "Smith", "123456"),
        # ("visual_user", "secret_sauce", "Alice", "Smith", "123456"),
    ],
)
@pytest.mark.smoke
def test_add_items_and_checkout(
    page, username, password, first_name, last_name, postal_code
):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    checkout_page = CheckoutPage(page)

    logger.info("Начинаем логин")
    try:
        login_page.login(username, password)
        if page.locator(".error-message-container").is_visible():
            error_text = page.locator(".error-message-container").inner_text()
            logger.warning(f"Ошибка при авторизации: {error_text}")
            pytest.fail(f"Ошибка авторизации: {error_text}")
    except Exception as e:
        logger.error(f"Ошибка при авторизации: {str(e)}")
        pytest.fail("Логин завершился с ошибкой")

    inventory_page.add_first_item_to_cart()
    checkout_page.start_checkout()
    checkout_page.fill_checkout_for(first_name, last_name, postal_code)
    logger.info("Тест завершён успешно")
