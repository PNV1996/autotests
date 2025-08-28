from playwright.sync_api import sync_playwright, expect

playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False, slow_mo=500)
page = browser.new_page()
page.goto("https://www.saucedemo.com/")


page.fill('[id="user-name"]', "locked_out_user")
page.fill('[id="password"]', "secret_sauce")
page.click('[id="login-button"]')
expect(page.locator("body")).to_contain_text(
    "Epic sadface: Sorry, this user has been locked out."
)

page.fill('[id="user-name"]', "standard_user")
page.fill('[id="password"]', "secret_sauce1")
page.click('[id="login-button"]')
expect(page.locator("body")).to_contain_text(
    "Epic sadface: Username and password do not match any user in this service"
)
