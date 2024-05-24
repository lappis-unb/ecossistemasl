from selenium.webdriver.common.by import By
import time
import re


def extract_hrefs_from_table(driver):
    table = driver.find_element(By.CLASS_NAME, "table-list")
    rows = table.find_elements(By.TAG_NAME, "tr")

    hrefs = []
    for row in rows:
        links = row.find_elements(By.TAG_NAME, "a")
        for link in links:
            href = link.get_attribute("href")
            if href and href.endswith("edit"):
                hrefs.append(href)

    return hrefs


def get_last_page_href(driver):
    try:
        last_page_button = driver.find_element(By.CLASS_NAME, "pagination-last")
    except:
        last_page_button = None

    if last_page_button:
        last_page_href = last_page_button.get_attribute("href")
        return last_page_href
    return None


def generate_all_page_hrefs(last_page_href):
    match = re.search(r"(.*?page=)(\d+)(.*)", last_page_href)
    if match:
        base_url = match.group(1)
        total_pages = int(match.group(2))
        suffix = match.group(3)

        return [f"{base_url}{page}{suffix}" for page in range(1, total_pages + 1)]
    return []


def extract_all_hrefs(driver, initial_url):
    driver.get(initial_url)
    all_hrefs = []

    try:
        last_page_href = get_last_page_href(driver)

        all_page_hrefs = []

        if last_page_href is None:
            all_page_hrefs.append(initial_url)
        else:
            all_page_hrefs = generate_all_page_hrefs(last_page_href)

        for page_href in all_page_hrefs:
            driver.get(page_href)
            time.sleep(2)
            hrefs = extract_hrefs_from_table(driver)
            all_hrefs.extend(hrefs)
    except Exception as e:
        print(f"An error occurred: {e}")

    return all_hrefs
