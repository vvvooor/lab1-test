import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager


@pytest.fixture
def driver():

    options = FirefoxOptions()
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


def test_login_demoblaze(driver):

    driver.get("https://www.demoblaze.com/")
    driver.maximize_window()

    login_button = driver.find_element(By.ID, "login2")
    login_button.click()

    time.sleep(1)

    username_input = driver.find_element(By.ID, "loginusername")
    password_input = driver.find_element(By.ID, "loginpassword")

    username_input.send_keys("test")
    time.sleep(1)

    password_input.send_keys("test")
    driver.find_element(By.XPATH, "//button[text()='Log in']").click()
    time.sleep(5)

    welcome_text = driver.find_element(By.ID, "nameofuser")
    assert welcome_text.is_displayed(), " Тест не пройден: 'Welcome' не найден."
    assert "Welcome" in welcome_text.text, " Тест не пройден: текст приветствия некорректный."

    print(" Тест пройден успешно: вход выполнен. ")