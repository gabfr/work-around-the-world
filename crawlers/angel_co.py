from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import configparser

import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

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


def selenium_create_driver(executable_path=r'/usr/local/bin/chromedriver', options=None):
    if options is None:
        options = Options()

    return webdriver.Chrome(options=options, executable_path=executable_path)


def lazy_get_element(driver, css_selector, timeout=30):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))


def accept_cookies(driver):
    driver.implicitly_wait(5)

    accept_cookies_button = lazy_get_element(driver, '.c-button.c-button--blue')
    accept_cookies_btn_is_interactable = accept_cookies_button.is_displayed() and accept_cookies_button.is_enabled()
    if accept_cookies_button is not None and accept_cookies_btn_is_interactable:
        accept_cookies_button.click()


def do_login(driver):
    login_button = lazy_get_element(driver, 'a.auth.login')
    if login_button is not None:
        login_button.click()
    else:
        print('Cant follow to the login page')
        return

    driver.implicitly_wait(1)

    email_input = lazy_get_element(driver, '#user_email')
    password_input = lazy_get_element(driver, '#user_password')

    if email_input is None or password_input is None:
        print('Cant follow to type the email/password')
        return

    email_input.send_keys(ANGELCO_EMAIL)
    password_input.send_keys(ANGELCO_PASSWORD)

    login_form_button = lazy_get_element(driver, '.s-form input[type="submit"]')
    if login_form_button is None:
        print('Cant find the login form button? Cant follow with the script')
    login_form_button.click()


def clean_all_filters(driver, selector):
    """
    Had to go to a recursive approach to clean all filters as our element tree changes each time we delete
    a filter
    :param driver:
    :param selector:
    :return:
    """
    filters_buttons = driver.find_elements_by_css_selector(selector)

    if not filters_buttons:
        return

    filters_buttons[0].click()
    driver.implicitly_wait(1)

    if len(filters_buttons) > 1:
        clean_all_filters(driver, selector)


def main():
    global ANGELCO_EMAIL, ANGELCO_PASSWORD

    config_parse_file()

    print("Email: " + ANGELCO_EMAIL)
    print("Password: " + ANGELCO_PASSWORD)

    incognito_mode = Options()
    incognito_mode.add_argument('--incognito')

    driver = selenium_create_driver(options=incognito_mode)

    driver.get('https://angel.co')

    driver.implicitly_wait(5)

    accept_cookies(driver)

    do_login(driver)

    lazy_get_element(driver, '.remove-filter.delete')  # wait until the remove filter buttons appear
    # then, find all remove filter buttons

    clean_all_filters(driver, '.remove-filter.delete')

    # after cleaning all filter's

    # Waiting for the startup div that holds the jobs listing
    lazy_get_element(
        driver,
        '#startups_content > .job_listings.browse_startups > .find.g-module.startup-container > div'
    )


    input('prompt')


if __name__ == '__main__':
    main()
