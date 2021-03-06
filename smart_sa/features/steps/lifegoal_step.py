import time

from aloe import world, step
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
from selenium.webdriver.support.expected_conditions import \
    text_to_be_present_in_element_value, visibility_of_element_located


def get_css_selector(name):
    if name == "Step 2":
        return "div#step2 input"
    elif name == "Step 3":
        return "div#step3 input"
    elif name == "Step 4":
        return "div#step4 input"
    elif name == "Goal":
        return "div#goal input"


def get_input(name):
    selector = get_css_selector(name)
    wait = ui.WebDriverWait(world.browser, 5)
    wait.until(
        visibility_of_element_located((By.CSS_SELECTOR, selector)))
    return world.browser.find_element_by_css_selector(selector)


@step(u'When I enter "([^"]*)" for "([^"]*)"')
def when_i_enter_value_for_input(step, value, input):
    elt = get_input(input)
    elt.clear()
    for c in value:
        elt.send_keys(c)
        time.sleep(1)


@step(u'Then "([^"]*)" is "([^"]*)"')
def then_input_is_value(step, input, value):
    wait = ui.WebDriverWait(world.browser, 5)
    wait.until(text_to_be_present_in_element_value(
        (By.CSS_SELECTOR, get_css_selector(input)), value))
