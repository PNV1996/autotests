from playwright.sync_api import sync_playwright, expect

playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False, slow_mo=500)
page = browser.new_page()

def safe_click(page,selector):
    expect(page.locator(selector)).to_be_visible(), f"{selector} не виден"
    expect(page.locator(selector)).to_be_enabled(), f"{selector} не доступен"
    page.click(selector)

def wait_url(page, url):
    expect(page).to_have_url(url)

#Авторизация
page.goto("https://www.saucedemo.com/")
page.fill('[id="user-name"]', "standard_user")
page.fill('[id="password"]', "secret_sauce")
safe_click(page, '#login-button')

#Добавление товаров в корзину
wait_url(page, 'https://www.saucedemo.com/inventory.html')
safe_click(page,'#add-to-cart-sauce-labs-fleece-jacket')
safe_click(page, '[data-test="add-to-cart-test.allthethings()-t-shirt-(red)"]')
safe_click(page, '.inventory_item_description:has-text("Sauce Labs Bike Light") button:has-text("Add to cart")')
                           # класс карточки товара с текстом Sauce Labs Bike Light   кнопка внутри карточки товара с текстом Add to cart
safe_click(page, '#shopping_cart_container')


#Просмотр товаров в корзине
wait_url(page, 'https://www.saucedemo.com/cart.html')
safe_click(page,'#checkout')

#Заполнение данных для оформления заказа
wait_url(page, 'https://www.saucedemo.com/checkout-step-one.html')
page.fill('[id="first-name"]', 'Bobr')
page.fill('[id="last-name"]', 'Kurwa')
page.fill('[id="postal-code"]', '7575')
safe_click(page, '#continue')

#Завершение оформления заказа
wait_url(page, 'https://www.saucedemo.com/checkout-step-two.html')
safe_click(page, '#finish')

#Выход
page.click('[id="react-burger-menu-btn"]')
page.click('[id="logout_sidebar_link"]')

browser.close()
playwright.stop()

