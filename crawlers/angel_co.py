from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import configparser

ANGELCO_EMAIL = None
ANGELCO_PASSWORD = None


def config_parse_file():
    """
    Parse the dwh.cfg configuration file
    :return:
    """
    global ANGELCO_EMAIL, ANGELCO_PASSWORD

    print("Parsing the config file...")
    config = configparser.ConfigParser()
    with open('dwh.cfg') as configfile:
        config.read_file(configfile)

        ANGELCO_EMAIL = config.get('ANGELCO', 'EMAIL')
        ANGELCO_PASSWORD = config.get('ANGELCO', 'PASSWORD')


def main():
    config_parse_file()

    print("Email: " + ANGELCO_EMAIL)
    print("Password: " + ANGELCO_PASSWORD)


if __name__ == '__main__':
    main()
