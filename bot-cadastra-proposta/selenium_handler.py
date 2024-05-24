from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time


def setup_selenium(config):
    chrome_options = Options()

    if config["mode_headless"]:
        chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )
    return driver


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


def select_category(driver, category_text):
    select_element = driver.find_element(By.ID, "proposal_category_id")
    select = Select(select_element)
    for option in select.options:
        if category_text in option.text:
            select.select_by_visible_text(option.text)
            break

    print(f"Category not found: {category_text}")
    input("Add the category manually and press Enter...")


def format_address(address, city, state):
    formatted_address = f"{address}, {city}, {state}".title()
    return formatted_address


def concatenate_description(initiative):
    formatted_address = format_address(
        initiative.address, initiative.city, initiative.state
    )
    full_description = (
        f"<p><strong>Nome/Organização Resposável:</strong> {initiative.responsible_organization}</p>"
        f"<p><strong>Email:</strong> {initiative.email}</p>"
        f"<p><strong>Telefone:</strong> {initiative.phone}</p>"
        f"<p><strong>Endereço:</strong> {formatted_address}</p>"
    )
    return full_description


def create_initiative(driver, config, initiative):
    driver.get(config["create_initiative_url"])

    # Title
    driver.find_element(By.ID, "proposal_title_pt__BR").send_keys(initiative.name)

    # Description
    full_description = concatenate_description(initiative)
    body_element = driver.find_element(
        By.CSS_SELECTOR, "div.ql-editor[contenteditable='true']"
    )
    driver.execute_script(
        f"arguments[0].innerHTML = `{full_description}`;", body_element
    )

    # Address
    address = ""
    if config["default_city"]:
        address = config["default_city"]
    else:
        address = format_address(initiative.address, initiative.city, initiative.state)

    driver.find_element(By.ID, "proposal_address").send_keys(address)

    # Category
    select_category(driver, initiative.category)

    # Submit
    submit_button = driver.find_element(
        By.XPATH,
        "//button[@type='submit' and @name='commit' and contains(@class, 'button')]",
    )
    submit_button.click()

    input("Press Enter after adding the initiative...")


def teardown_selenium(driver):
    driver.quit()
