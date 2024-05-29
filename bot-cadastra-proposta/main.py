from spreadsheet_reader import (
    read_csv_to_initiative_list,
    add_text_to_initiative_attribute,
)
from selenium_handlers.setup import setup_selenium, teardown_selenium
from selenium_handlers.login import login
from selenium_handlers.initiatives_manager import create_initiative, format_title
from selenium_handlers.extract_hrefs import extract_all_hrefs
from config_loader import load_config
from enum import Enum


class Environment(Enum):
    PRODUCTION = "prod"
    DEVELOPMENT = "dev"


class Action(Enum):
    CREATE_INITIATIVES = "1"
    FORMAT_TITLE = "2"


def print_decorator(func):
    def wrapper(*args, **kwargs):
        print("----------------------------------")
        result = func(*args, **kwargs)
        print("----------------------------------")
        return result

    return wrapper


@print_decorator
def get_environment_choice():
    choices = {env.value: env for env in Environment}
    choice = None
    while choice not in choices:
        print("Choose the environment:")
        for key in choices:
            print(f"{key} - {choices[key].name.capitalize()}")
        choice = input("Enter your choice: ").strip().lower()
        if choice not in choices:
            print("Invalid choice.")
    return choices[choice]


@print_decorator
def get_action_choice():
    choices = {action.value: action for action in Action}
    choice = None
    while choice not in choices:
        print("Choose the action:")
        for key in choices:
            print(f"{key} - {choices[key].name.capitalize()}")
        choice = input("Enter your choice (create/extract): ").strip().lower()
        if choice not in choices:
            print("Invalid choice.")
    return choices[choice]


@print_decorator
def get_start_row():
    start_row = input("Enter the start row: ")
    try:
        return int(start_row)
    except:
        print("Invalid row number.")
        return get_start_row()


def main():
    env_choice = get_environment_choice()
    config_file = f"config_{env_choice.value}.json"
    config = load_config(config_file)

    action_choice = get_action_choice()

    driver = setup_selenium(config)

    try:
        login(driver, config)

        if action_choice == Action.CREATE_INITIATIVES:
            filename = config["csv_filename"]
            initiatives = read_csv_to_initiative_list(filename)
            start_row = get_start_row()

            for initiative in initiatives[start_row - 2 :]:
                try:
                    if "não" not in initiative.status:
                        continue

                    input(f"Press Enter to create initiative: {initiative.name}")

                    for i in range(0, 4):
                        wait_to_submit = False
                        if i == 3:
                            print(f"Failed to create initiative: {initiative.name}")
                            wait_to_submit = True

                        response = create_initiative(
                            driver, config, initiative, wait_to_submit=wait_to_submit
                        )
                        if response:
                            add_text_to_initiative_attribute(
                                filename, initiative.name, "Status", "feito"
                            )
                            break
                except Exception as e:
                    print(f"Failed to create initiative: {initiative.name}")
                    print(e)
                    input("Press Enter to continue...")

        elif action_choice == Action.FORMAT_TITLE:
            initial_url = config["initial_page_url"]
            all_hrefs = extract_all_hrefs(driver, initial_url)
            format_title(driver, all_hrefs)

    finally:
        teardown_selenium(driver)


if __name__ == "__main__":
    main()
