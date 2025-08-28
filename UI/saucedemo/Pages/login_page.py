from UI.saucedemo.Pages.base_page import BasePage
from utils.logger import get_logger


class LoginPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self._endpoint = ""

    logger = get_logger("LoginPage")

    USERNAME_SELECTOR = "#user-name"
    PASSWORD_SELECTOR = "#password"
    LOGIN_BUTTON_SELECTOR = "#login-button"
    ERROR_INFO = "h3:has-test"

    def login(self, username, password):
        self.logger.info(
            f"Выполняем авторизацию заполняя логин и пароль: {username}, {password}"
        )
        self.navigate_to()
        self.wait_for_selector_and_fill(self.USERNAME_SELECTOR, username)
        self.wait_for_selector_and_fill(self.PASSWORD_SELECTOR, password)
        self.wait_for_selector_and_click(self.LOGIN_BUTTON_SELECTOR)
        self.assert_text_present_on_page("Products")
