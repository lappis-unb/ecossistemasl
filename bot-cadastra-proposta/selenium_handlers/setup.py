from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def setup_selenium(config):
    chrome_options = Options()

    if config["mode_headless"]:
        chrome_options.add_argument("--headless")

    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument(f"--user-data-dir={config['chrome_user_data_dir']}")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )
    return driver


def teardown_selenium(driver):
    driver.quit()
