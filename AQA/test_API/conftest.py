import pytest
import requests
from faker import Faker
from Constant import HEADERS, BASE_URL
faker = Faker()

@pytest.fixture(scope="session")
def auth_session():
    session = requests.Session()
    session.headers.update(HEADERS)

    response = requests.post(f"{BASE_URL}/auth", headers=HEADERS, json={"username" : "admin","password" : "password123"})
    assert response.status_code == 200, "Ошибка авторизации"
    token = response.json().get('token')
    assert token is not None, "В ответе не оказалось токена"

    session.headers.update({"Cookie" : f'token={token}'})
    return session

@pytest.fixture()
def booking_data():
    return {
        "firstname" : faker.first_name(),
        "lastname" : faker.last_name(),
        "totalprice" : faker.random_int(min=100,max=5000),
        "depositpaid" : True,
        "bookingdates" : {
            "checkin" : "2018-01-01",
            "checkout" : "2019-01-01"
        },
        "additionalneeds" : "Breakfast"}

@pytest.fixture()
def put_data():
    return {
    "firstname" : "James",
    "lastname" : "Brown",
    "totalprice" : 111,
    "depositpaid" : True,
    "bookingdates" : {
        "checkin" : "2018-01-01",
        "checkout" : "2019-01-01"
    },
    "additionalneeds" : "Breakfast"
}



import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    yield browser
    browser.close()
    playwright.stop()


