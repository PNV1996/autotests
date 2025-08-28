from UI.saucedemo.Pages.base_page import BasePage
from utils.logger import get_logger

class CheckoutPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self._endpoint = "/checkout-step-one.html"

    logger = get_logger("CheckoutPage")

    CHECKOUT_BUTTON_SELECTOR= "[id='checkout']"
    FIRST_NAME_SELECTOR='#first-name'
    LAST_NAME_SELECTOR = '#last-name'
    POSTAL_CODE_SELECTOR= "input[name='postalCode']"



    def start_checkout(self):
        self.wait_for_selector_and_click(self.CHECKOUT_BUTTON_SELECTOR)
        self.assert_element_is_visible(self.FIRST_NAME_SELECTOR)

    def fill_checkout_for(self,first_name, last_name, postal_code):
        self.logger.info(f"Заполняем чек-аут: {first_name}, {last_name}, {postal_code}")
        self.wait_for_selector_and_type(self.FIRST_NAME_SELECTOR, first_name, 100)
        self.wait_for_selector_and_type(self.LAST_NAME_SELECTOR, last_name, 100)
        self.wait_for_selector_and_type(self.POSTAL_CODE_SELECTOR, postal_code, 100)
        self.assert_input_value(self.POSTAL_CODE_SELECTOR, postal_code)