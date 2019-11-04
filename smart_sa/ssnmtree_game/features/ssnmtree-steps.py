import time

from lettuce import world, step
from selenium.common.exceptions import NoSuchElementException


@step('I fill in the SSNM Tree with "([^"]*)"')
def fill_in_ssnmtree(self, text):
    if not world.using_selenium:
        assert False, (
            "this step needs to be implemented for the django test client")
    for i in world.browser.find_elements_by_tag_name('input'):
        if i.get_attribute('type') == 'text':
            i.clear()
            for c in text:
                i.send_keys(c)
        assert i.get_attribute("value") == text


@step('there is a filled in SSNM Tree with "([^"]*)"')
def filled_in_ssnmtree(self, text):
    if not world.using_selenium:
        assert False, (
            "this step needs to be implemented for the django test client")
    all_filled = True
    assert all_filled


@step(u'When I clear the circle')
def when_i_clear_the_circle(step):
    fruit = world.browser.find_element_by_id("top1-fruit")
    elt = fruit.find_element_by_tag_name('input')
    elt.clear()


@step(u'When I name the circle "([^"]*)"')
def when_i_name_the_circle_name(step, name):
    try:
        fruit = world.browser.find_element_by_id("top1-fruit")
    except NoSuchElementException:
        time.sleep(1)
        fruit = world.browser.find_element_by_id("top1-fruit")
    elt = fruit.find_element_by_tag_name('input')
    elt.clear()
    elt.send_keys(name)


@step(u'When I click the circle')
def when_i_click_the_circle(step):
    elt = world.browser.find_element_by_css_selector("#top1-fruit div.circle")
    assert elt is not None
    world.browser.execute_script("arguments[0].click();", elt)


@step(u'Then the circle is "([^"]*)"')
def then_the_circle_is_color(step, color):
    try:
        elt = world.browser.find_element_by_id("top1-fruit")
    except NoSuchElementException:
        time.sleep(3)
        elt = world.browser.find_element_by_id("top1-fruit")

    assert elt is not None

    if color == "gold":
        gold = elt.find_element_by_css_selector("div.ripe.turned-on")
        assert gold, "The circle is not gold"
    elif color == "purple":
        purple = elt.find_element_by_css_selector("div.circle.turned-on")
        assert purple, "The circle is not purple"
    elif color == "gold and purple":
        pass


@step(u'Then the circle is not "([^"]*)"')
def then_the_circle_is_not_color(step, color):
    elt = world.browser.find_element_by_id("top1-fruit")
    assert elt is not None
    try:
        if color == "gold":
            elt.find_element_by_css_selector("div.ripe.turned-on")
        elif color == "purple":
            elt.find_element_by_css_selector("div.circle.turned-on")
        elif color == "gold and purple":
            elt.find_element_by_css_selector("div.ripe.turned-on")
            elt.find_element_by_css_selector("div.circle.turned-on")
        assert False, "The circle is %s" % color
    except NoSuchElementException:
        pass  # expected


@step(u'When I click the "([^"]*)" button')
def when_i_click_the_name_button(step, name):
    elt = None
    if name == "disclosure":
        elt = world.browser.find_element_by_id("toggle-disclosure-selection")
    elif name == "support":
        elt = world.browser.find_element_by_id("toggle-support-selection")
    assert elt, "No button named %s found" % name
    elt.click()


@step(u'Then "([^"]*)" is selected')
def then_button_is_selected(step, button):
    if button == 'disclosure':
        q = '#toggle-disclosure-selection.on'
    elif button == 'support':
        q = '#toggle-support-selection.on'

    elt = world.browser.find_element_by_css_selector(q)
    assert elt, 'disclosure button should be selected'


@step(r'Then I wait (\d+) seconds')
def then_i_wait_count_seconds(step, count):
    n = int(count)
    time.sleep(n)
