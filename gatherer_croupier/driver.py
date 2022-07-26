from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

# Implicit wait in seconds
IMPLICIT_WAIT = 0


def initialize_driver(headless=False, install=False):
    mozilla_options = Options()
    if headless:
        mozilla_options.add_argument("--headless")

    if install:
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=mozilla_options)
    else:
        driver = webdriver.Firefox(options=mozilla_options)

    driver.implicitly_wait(IMPLICIT_WAIT)
    return driver
