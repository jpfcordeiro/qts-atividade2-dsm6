from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time


def get_headless_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(options=options)


def test_create_user_with_age_e2e():
    driver = get_headless_driver()
    wait = WebDriverWait(driver, 5)
    try:
        driver.get("http://localhost:5000")

        driver.find_element(By.ID, "name").send_keys("Bruno Idade")
        driver.find_element(By.ID, "email").send_keys("bruno@gmail.com")
        driver.find_element(By.ID, "age").send_keys("45")
        driver.find_element(By.ID, "submit").click()

        wait.until(lambda d: "Bruno Idade" in d.find_element(By.ID, "users").text)
        assert "45 anos" in driver.find_element(By.ID, "users").text
    finally:
        driver.quit()


def test_invalid_age_error_e2e():
    driver = get_headless_driver()
    try:
        driver.get("http://localhost:5000")

        driver.find_element(By.ID, "name").send_keys("Fernanda Erro")
        driver.find_element(By.ID, "email").send_keys("fernanda@gmail.com")
        driver.find_element(By.ID, "age").send_keys("200")
        driver.find_element(By.ID, "submit").click()

        time.sleep(2)
        assert "Fernanda Erro" not in driver.find_element(By.ID, "users").text
    finally:
        driver.quit()
