from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def select_category(driver, category_text, force_id):
    select_element = driver.find_element(By.ID, "proposal_category_id")
    select = Select(select_element)

    for option in select.options:
        if force_id and force_id == option.get_attribute("value"):
            select.select_by_value(force_id)
            return
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
        f"<p><strong>Endereço:</strong> {formatted_address}</p>"
    )
    return full_description


def format_title(driver, hrefs):
    for href in hrefs:
        driver.get(href)

        title_element = driver.find_element(By.ID, "proposal_title_pt__BR")
        original_title = title_element.get_attribute("value")
        formatted_title = original_title.title()

        if original_title != formatted_title:
            title_element.clear()
            title_element.send_keys(formatted_title)

            save_button = driver.find_element(
                By.XPATH,
                "//button[@type='submit' and @name='commit' and contains(@class, 'button')]",
            )
            save_button.click()


def check_response(driver):
    try:
        response = driver.find_element(
            By.CSS_SELECTOR, "div.callout.success.callout--full"
        )
    except:
        response = None

    if response:
        print(response.text)
        return True
    return False


def create_initiative(driver, config, initiative, wait_to_submit=False):
    driver.get(config["create_initiative_url"])

    # Title
    driver.find_element(By.ID, "proposal_title_pt__BR").send_keys(
        f"{initiative.name}".title()
    )

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
    force_id = config["force_category_id"]
    select_category(driver, initiative.category, force_id)

    # Submit
    submit_button = driver.find_element(
        By.XPATH,
        "//button[@type='submit' and @name='commit' and contains(@class, 'button')]",
    )
    if wait_to_submit:
        print("Choose your action: ")
        print("1 - Complete form again")
        print("2 - Go to next iniciative and change status to 'Feito' in the CSV file")
        print("3 - Go to next iniciative and not change status in the CSV file")
        input_choice = input("Enter your choice: ")
        if input_choice == "1":
            return create_initiative(driver, config, initiative, wait_to_submit=True)
        elif input_choice == "2":
            return True
        elif input_choice == "3":
            return False
        else:
            print("Invalid choice.")
            return create_initiative(driver, config, initiative, wait_to_submit=True)
    else:
        submit_button.click()

    return check_response(driver)
