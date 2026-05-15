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


def test_create_user_e2e():
    driver = get_headless_driver()
    driver.get("http://localhost:5000")

    input_name = driver.find_element(By.ID, "name")
    input_name.send_keys("Joao")

    input_email = driver.find_element(By.ID, "email")
    input_email.send_keys("joao@gmail.com")

    driver.find_element(By.ID, "submit").click()

    wait = WebDriverWait(driver, 5)
    wait.until(lambda d: any("Joao" in el.text for el in d.find_elements(By.TAG_NAME, "li")))

    users = driver.find_elements(By.TAG_NAME, "li")
    assert any("Joao" in user.text for user in users)
    driver.quit()


def test_exercicio_passo_a_passo_e2e():
    driver = get_headless_driver()
    wait = WebDriverWait(driver, 5)

    try:
        driver.get("http://localhost:5000")
        assert driver.title == "Users"

        input_name = driver.find_element(By.ID, "name")
        input_name.clear()
        input_name.send_keys("Maria Silva")

        input_email = driver.find_element(By.ID, "email")
        input_email.clear()
        input_email.send_keys("maria@gmail.com")

        driver.find_element(By.ID, "submit").click()

        wait.until(lambda d: "Maria Silva" in d.find_element(By.ID, "users").text)

        assert "Maria Silva" in driver.find_element(By.ID, "users").text

        input_name = driver.find_element(By.ID, "name")
        input_name.clear()
        input_name.send_keys("Jose Oliveira")

        input_email = driver.find_element(By.ID, "email")
        input_email.clear()
        input_email.send_keys("jose@gmail.com")

        driver.find_element(By.ID, "submit").click()

        wait.until(lambda d: "Jose Oliveira" in d.find_element(By.ID, "users").text)

        users_list = driver.find_elements(By.TAG_NAME, "li")
        users_texts = [user.text for user in users_list]
        assert "Maria Silva" in str(users_texts)
        assert "Jose Oliveira" in str(users_texts)

    finally:
        driver.quit()


def test_register_user_with_email_e2e():
    driver = get_headless_driver()
    wait = WebDriverWait(driver, 5)
    try:
        driver.get("http://localhost:5000")

        input_name = driver.find_element(By.ID, "name")
        input_name.clear()
        input_name.send_keys("Carlos Santos")

        input_email = driver.find_element(By.ID, "email")
        input_email.clear()
        input_email.send_keys("carlos@gmail.com")

        driver.find_element(By.ID, "submit").click()

        wait.until(lambda d: "Carlos Santos" in d.find_element(By.ID, "users").text)

        assert "Carlos Santos" in driver.find_element(By.ID, "users").text
    finally:
        driver.quit()


def test_validation_error_duplicate_email_e2e():
    driver = get_headless_driver()
    wait = WebDriverWait(driver, 5)
    try:
        driver.get("http://localhost:5000")

        input_name = driver.find_element(By.ID, "name")
        input_name.clear()
        input_name.send_keys("Ana Duplicada 1")

        input_email = driver.find_element(By.ID, "email")
        input_email.clear()
        input_email.send_keys("duplicada@gmail.com")

        driver.find_element(By.ID, "submit").click()

        wait.until(lambda d: "Ana Duplicada 1" in d.find_element(By.ID, "users").text)

        input_name = driver.find_element(By.ID, "name")
        input_name.clear()
        input_name.send_keys("Ana Duplicada 2")

        input_email = driver.find_element(By.ID, "email")
        input_email.clear()
        input_email.send_keys("duplicada@gmail.com")

        driver.find_element(By.ID, "submit").click()

        time.sleep(2)
        users_text = driver.find_element(By.ID, "users").text
        assert "Ana Duplicada 2" not in users_text

    finally:
        driver.quit()
