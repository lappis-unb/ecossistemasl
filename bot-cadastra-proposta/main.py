from spreadsheet_reader import read_csv_to_initiative_list
from selenium_handler import setup_selenium, login, create_initiative, teardown_selenium
from config_loader import load_config
from enum import Enum


class Environment(Enum):
    PRODUCTION = "prod"
    DEVELOPMENT = "dev"


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

    filename = config["csv_filename"]
    initiatives = read_csv_to_initiative_list(filename)

    start_row = get_start_row()

    driver = setup_selenium(config)

    try:
        login(driver, config)
        for initiative in initiatives[start_row - 2 :]:
            create_initiative(driver, config, initiative)
    finally:
        teardown_selenium(driver)


if __name__ == "__main__":
    main()
