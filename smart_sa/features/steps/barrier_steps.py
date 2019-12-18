import time

from aloe import world, step
from selenium.common.exceptions import NoSuchElementException, \
    TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui

from selenium.webdriver.support.expected_conditions \
    import visibility_of_element_located, element_to_be_clickable, \
    invisibility_of_element_located


@step(u'I toggle personal challenge')
def i_toggle_personal_challenge(step):
    selector = '.iphone-toggle-buttons input[type="checkbox"] + span'

    wait = ui.WebDriverWait(world.browser, 5)
    wait.until(
        element_to_be_clickable((By.CSS_SELECTOR, selector)))

    i = world.browser.find_element_by_css_selector(selector)
    i.click()


@step(u'When I click the Save Plan button')
def when_i_click_the_save_plan_button(step):
    selector = 'div#actionplan_form input[type="submit"]'
    wait = ui.WebDriverWait(world.browser, 5)
    wait.until(
        visibility_of_element_located((By.CSS_SELECTOR, selector)))

    elt = world.browser.find_element_by_css_selector(selector)

    ActionChains(world.browser).move_to_element(elt).perform()
    elt.click()


@step(r'I select barrier (\d+)')
def i_select_barrier(step, barrier):
    barrier_idx = int(barrier) - 1  # Assumes 1 based indexing
    elts = world.browser.find_elements_by_css_selector(
        'div.issue-selector div.issue-number')

    for idx, val in enumerate(elts):
        if idx == barrier_idx:
            try:
                val.click()
            except NoSuchElementException:
                pass


@step(r'Then barrier (\d+) has "([^"]*)"')
def then_barrier_number_has_state(step, number, state):
    barrier_idx = int(number) - 1
    elts = world.browser.find_elements_by_css_selector(
        'div.issue-selector div.issue-number')

    for idx, val in enumerate(elts):
        if idx == barrier_idx:
            clazz = val.get_attribute("class")
            assert state in clazz, clazz
            break


@step(r'Then barrier (\d+) does not have "([^"]*)"')
def then_barrier_number_does_not_have_state(step, number, state):
    barrier_idx = int(number) - 1
    elts = world.browser.find_elements_by_css_selector(
        'div.issue-selector div.issue-number')
    for idx, val in enumerate(elts):
        if idx == barrier_idx:
            clazz = val.get_attribute("class")
            assert state not in clazz, clazz
            break


@step(u'there is no issue selector')
def there_is_no_issue_selector(step):
    wait = ui.WebDriverWait(world.browser, 5)
    wait.until(
        invisibility_of_element_located((By.ID, 'issue-selector')))


@step(u'there is an issue selector')
def there_is_an_issue_selector(step):
    wait = ui.WebDriverWait(world.browser, 5)
    wait.until(
        visibility_of_element_located((By.ID, 'issue-selector')))


@step(u'i navigate "([^"]*)"')
def i_navigate_direction(step, direction):
    if direction == "left":
        i = world.browser.find_element_by_css_selector('#previous_issue')
    elif direction == "right":
        i = world.browser.find_element_by_css_selector('#next_issue')
    try:
        i.click()
    except NoSuchElementException:
        pass


@step(u'there is no left arrow')
def there_is_no_left_arrow(step):
    i = world.browser.find_element_by_css_selector('#previous_issue img')
    assert not i.is_displayed(), "Left arrow should be invisible now"


@step(u'there is a left arrow')
def there_is_a_left_arrow(step):
    i = world.browser.find_element_by_css_selector('#previous_issue img')
    assert i.is_displayed(), "Left arrow should be visible now"


@step(u'there is no right arrow')
def there_is_no_right_arrow(step):
    selector = '#next_issue img'
    wait = ui.WebDriverWait(world.browser, 5)
    wait.until(
        invisibility_of_element_located((By.CSS_SELECTOR, selector)))


@step(u'there is a right arrow')
def there_is_a_right_arrow(step):
    selector = '#next_issue img'
    wait = ui.WebDriverWait(world.browser, 5)
    wait.until(
        visibility_of_element_located((By.CSS_SELECTOR, selector)))


@step(u'there is no action plan button')
def there_is_no_action_plan_button(step):
    selector = '#actionplan a'
    wait = ui.WebDriverWait(world.browser, 5)
    wait.until(
        invisibility_of_element_located((By.CSS_SELECTOR, selector)))


@step(u'Then there is a Make Plan button')
def then_there_is_a_make_plan_button(step):
    selector = '#actionplan a'
    wait = ui.WebDriverWait(world.browser, 5)
    wait.until(
        visibility_of_element_located((By.CSS_SELECTOR, selector)))


@step(u'Then there is an Edit Plan button')
def then_there_is_an_edit_plan_button(step):
    selector = '#actionplan a'
    wait = ui.WebDriverWait(world.browser, 5)
    wait.until(
        visibility_of_element_located((By.CSS_SELECTOR, selector)))


@step(u'there is no Action Plan form')
def then_there_is_no_action_plan_form(step):
    try:
        wait = ui.WebDriverWait(world.browser, 5)
        wait.until(
            invisibility_of_element_located((By.ID, 'actionplan_form')))
        time.sleep(1)
    except TimeoutException:
        pass


@step(u'Then there is an Action Plan form')
def then_there_is_an_action_plan_form(step):
    wait = ui.WebDriverWait(world.browser, 5)
    wait.until(
        visibility_of_element_located((By.ID, 'actionplan_form')))
    time.sleep(1)


@step(u'When I type "([^"]*)" in "([^"]*)"')
def when_i_type_text_in_elementId(step, text, elementId):
    elt = world.browser.find_element_by_id(elementId)
    elt.send_keys(text)


@step(u'Then "([^"]*)" reads "([^"]*)"')
def then_elementId_reads_text(step, elementId, text):
    elt = world.browser.find_element_by_id(elementId)
    elt_text = elt.get_attribute("value")
    assert elt_text == text, elt_text


@step(u'Then I can specify my issue')
def then_i_can_specify_my_issue(step):
    elt = world.browser.find_element_by_css_selector(
        'div.issue-subtext textarea')
    assert elt.is_displayed(), (
        "element div.issue-subtext textarea should be visible")


@step(u'Then I cannot specify my issue')
def then_i_cannot_specify_my_issue(step):
    elt = world.browser.find_element_by_css_selector(
        'div.issue-subtext textarea')
    assert not elt.is_displayed(), (
        "element div.issue-subtext textarea should be invisible")


@step(u'Then I specify my issue as "([^"]*)"')
def then_i_specify_my_issue(step, text):
    elt = world.browser.find_element_by_css_selector(
        'div.issue-subtext textarea')
    elt.send_keys(text)


@step(u'my issue is "([^"]*)"')
def my_issue_is(step, text):
    elt = world.browser.find_element_by_css_selector(
        'div.issue-subtext textarea')
    elt_text = elt.get_attribute("value")
    assert elt_text == text, elt_text
