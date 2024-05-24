from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def login(driver, config):
    driver.get(config["login_url"])

    if (
        config["login_credentials"]["username"]
        and config["login_credentials"]["password"]
    ):
        driver.find_element(By.ID, "session_user_email").send_keys(
            config["login_credentials"]["username"]
        )
        driver.find_element(By.ID, "session_user_password").send_keys(
            config["login_credentials"]["password"]
        )
        driver.find_element(By.ID, "session_user_password").send_keys(Keys.ENTER)
        time.sleep(2)
    else:
        print("No login credentials provided. Please log in manually.")
        input("Press Enter after logging in...")

    print("Logged in.")
