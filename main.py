import time
from typing import Generator

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

BASE_URL = "https://www.saucedemo.com/"

@pytest.fixture(scope="module")
def pre_settings(
    request: pytest.FixtureRequest,
) -> Generator[webdriver.Chrome | webdriver.Firefox, None, None]:
    browser = request.config.getoption("browser")
    browser_version = request.config.getoption("browser_version")
    match browser:
        case "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            if browser_version is not None:
                options.browser_version = browser_version
            driver = webdriver.Chrome(options=options)
            yield driver
            driver.quit()
        case "firefox":
            fire_options = webdriver.FirefoxOptions()
            fire_options.add_argument("--headless")
            if browser_version is not None:
                fire_options.browser_version = browser_version
            fire_driver = webdriver.Firefox(options=fire_options)
            yield fire_driver
            fire_driver.quit()
        case _:
            raise ValueError("Unsupported browser")


def test_site_available(pre_settings: webdriver.Chrome | webdriver.Firefox) -> None:
    pre_settings.get(BASE_URL)
    assert pre_settings.current_url == BASE_URL


def test_login(pre_settings: webdriver.Chrome | webdriver.Firefox) -> None:
    # pre_settings.get(BASE_URL)

    username = pre_settings.find_elements(
        By.CSS_SELECTOR, 'input[class="input_error form_input"]'
    )[0]
    username.send_keys("standard_user")
    password = pre_settings.find_elements(
        By.CSS_SELECTOR, 'input[class="input_error form_input"]'
    )[1]
    password.send_keys("secret_sauce")

    login_button = pre_settings.find_element(
        By.CSS_SELECTOR, 'input[class="submit-button btn_action"]'
    )
    login_button.click()

    assert pre_settings.current_url == "https://www.saucedemo.com/inventory.html"


def test_products_is_displayed(
    pre_settings: webdriver.Chrome | webdriver.Firefox,
) -> None:
    catalog = pre_settings.find_element(By.CSS_SELECTOR, 'div[class="inventory_list"]')
    assert catalog.is_displayed()


def test_logout(pre_settings: webdriver.Chrome | webdriver.Firefox) -> None:
    extend_button = pre_settings.find_element(
        By.CSS_SELECTOR, 'button[id="react-burger-menu-btn"]'
    )
    extend_button.click()
    time.sleep(0.5)  # присутствует анимация ==> необходимо подождать

    logout_button = pre_settings.find_element(
        By.CSS_SELECTOR, 'a[id="logout_sidebar_link"]'
    )
    logout_button.click()
    assert pre_settings.current_url == BASE_URL
