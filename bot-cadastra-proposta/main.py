from spreadsheet_reader import read_csv_to_initiative_list
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
            for initiative in initiatives[start_row - 1 :]:
                create_initiative(driver, config, initiative)

        elif action_choice == Action.FORMAT_TITLE:
            initial_url = config["initial_page_url"]
            all_hrefs = extract_all_hrefs(driver, initial_url)
            format_title(driver, all_hrefs)

    finally:
        teardown_selenium(driver)


if __name__ == "__main__":
    main()
