import time

from behave import fixture, use_fixture
from selenium.webdriver import Chrome, Firefox, Edge
from librapage.config import BASE_URL
import logging


@fixture
def driver(context, *args, **kwargs):
    context.driver = Chrome()
    context.driver.maximize_window()
    context.driver.get(BASE_URL)

    yield context.driver
    time.sleep(5)
    context.driver.quit()


def before_scenario(context, scenario):
    use_fixture(driver, context)


def before_all(context):
    if not context.config.log_capture:
        logging.basicConfig(level=logging.INFO)
