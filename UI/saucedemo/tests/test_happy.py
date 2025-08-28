import pytest
from playwright.sync_api import sync_playwright

from UI.saucedemo.Pages.checkout_page import CheckoutPage
from UI.saucedemo.Pages.inventory_page import InventoryPage
from UI.saucedemo.Pages.login_page import LoginPage
from utils.logger import get_logger

logger = get_logger("TestCheckout")


@pytest.mark.parametrize(
    "username, password, first_name, last_name, postal_code, expect_success",
    [
        ("standard_user", "secret_sauce", "Jon", "Doe", "234235", True),
        ("standard_user", "secret_sauce1", "Brad", "Smith", "435345", False),
        ("locked_out_user", "secret_sauce", "Senen", "Hill", "345", False),
    ],
)
@pytest.mark.smoke
def test_add_items_and_checkout(
    page, username, password, first_name, last_name, postal_code, expect_success
):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    checkout_page = CheckoutPage(page)

    logger.info("Начинаем логин")
    error_text = ""  # <-- инициализация переменной

    try:
        login_page.login(username, password)

        # Проверяем, есть ли сообщение об ошибке
        if page.locator(".error-message-container").is_visible():
            error_text = page.locator(".error-message-container").inner_text()
            logger.warning(f"Ошибка при авторизации: {error_text}")
            if expect_success:
                pytest.fail(f"Ожидался успешный логин, но ошибка: {error_text}")

    except Exception as e:
        logger.error(f"Ошибка при авторизации: {str(e)}")
        if expect_success:
            pytest.fail("Логин завершился с ошибкой")
        else:
            logger.warning("Негативный кейс — продолжаем тест")

    # Только для успешного логина выполняем дальнейшие шаги
    if expect_success:
        inventory_page.add_first_item_to_cart()
        checkout_page.start_checkout()
        checkout_page.fill_checkout_for(first_name, last_name, postal_code)
        logger.info("Тест завершён успешно")
    else:
        logger.info("Негативный кейс — логин не удался, тест завершён")
