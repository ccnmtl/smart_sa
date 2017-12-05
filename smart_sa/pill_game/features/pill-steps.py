import time
from lettuce import world, step
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException


def find_pill(name):
    a = world.browser.find_elements_by_css_selector('div.pill')
    for pill in a:
        span = pill.find_element_by_css_selector('div.pill-text span')
        if span.text.startswith(name):
            return pill

    return None


def get_bucket(name):
    # Verify there's a dropped pill in bucket 1
    bucket = None
    if name == "daytime":
        bucket = world.browser.find_element_by_id("day")
    elif name == "evening":
        bucket = world.browser.find_element_by_id("night")
    return bucket


@step(u'I cannot edit "([^"]*)"')
def i_cannot_edit_pill(step, pill):
    pill = find_pill(pill)
    span = pill.find_element_by_css_selector('div.pill-text span')
    span.click()
    input = pill.find_element_by_css_selector('div.pill-text input')
    assert not input.is_displayed(), "Input element is visible"


@step(u'I can edit "([^"]*)"')
def i_can_edit_pill(step, pill):
    pill = find_pill(pill)
    span = pill.find_element_by_css_selector('div.pill-text span')
    span.click()
    input = pill.find_element_by_css_selector('div.pill-text input')
    assert input.is_displayed(), "Input element is visible"


@step(u'There is a "([^"]*)" title')
def there_is_a_group1_title(step, group1):
    i = world.browser.find_element_by_css_selector('#pill-list h4')
    assert i.text == group1, i.text


@step(u'There are (\d+) pills')
def there_are_n_pills(step, n):
    a = world.browser.find_elements_by_css_selector('#pill-list div.pill')
    assert len(a) == int(n), "Expecting %s pills, but see %s" % (n, len(a))


@step(u'There is a pill named "([^"]*)"')
def there_is_a_pill_named_name(step, name):
    pill = find_pill(name)
    assert pill is not None, "No pill named %s found" % name


@step(u'There is no pill named "([^"]*)"')
def there_is_no_pill_named_name(step, name):
    pill = find_pill(name)
    assert pill is None, "Pill named %s found" % name


@step(u'There is not an Add Pill button')
def there_is_not_an_add_pill_button(step):
    try:
        world.browser.find_element_by_id('add-a-pill')
        assert False, (
            'The Add Pill button should not be displayed in this mode')
    except NoSuchElementException:  # nosec
        pass


@step(u'There is an Add Pill button')
def there_is_an_add_pill_button(step):
    i = world.browser.find_element_by_id('add-a-pill')
    assert i is not None


@step(u'I click Add Pill')
def i_click_add_pill_button(step):
    i = world.browser.find_element_by_id('add-a-pill')
    assert i is not None
    i.click()


@step(u'When I drop "([^"]*)" onto "([^"]*)"')
def when_i_drop_pill_onto_time(step, pill, time):
    pill = find_pill(pill)
    assert pill is not None, "No pill named %s found." % pill

    # get the draggable span within
    draggable = pill.find_element_by_css_selector(
        "div.pill-image span.draggable")
    assert draggable is not None, (
        "This pill is not constructed properly: %s" % pill)

    bucket = get_bucket(time)
    assert bucket is not None, (
        "Time slot must be specified as day or evening. "
        "No time slot called %s found" % time)
    action_chains = ActionChains(world.browser)
    action_chains.drag_and_drop(draggable, bucket).perform()


@step(u'When I drop pill (\d+) onto "([^"]*)"')
def when_i_drop_pill_index_onto_time(step, index, time):
    idx = int(index) - 1
    a = world.browser.find_elements_by_css_selector('div.pill')
    assert len(a) > idx, (
        "Can't find pill %s as there are only %s pills in the list" % (
            index, len(a)))
    pill = a[idx]
    draggable = pill.find_element_by_css_selector(
        "div.pill-image span.draggable")
    assert draggable is not None, (
        "This pill is not constructed properly: %s" % pill)
    bucket = get_bucket(time)
    assert bucket is not None, (
        "Time slot must be specified as day or evening. "
        "No time slot called %s found" % time)
    action_chains = ActionChains(world.browser)
    action_chains.drag_and_drop(draggable, bucket).perform()


@step(u'Then there is (\d+) "([^"]*)" in "([^"]*)"')
def then_there_is_count_pill_in_time(step, count, pill, time):
    pill = find_pill(pill)
    assert pill is not None, "No pill named %s found. %s" % (pill, count)
    # get the draggable span within
    draggable = pill.find_element_by_css_selector(
        "div.pill-image span.draggable")
    assert draggable is not None, (
        "This pill is not constructed properly: %s" % pill)
    # get the data-id
    data_id = draggable.get_attribute("data-id")
    bucket = get_bucket(time)
    assert bucket is not None, (
        "Time slot must be specified as day or evening. "
        "No time slot called %s found" % time)

    n = 0
    a = bucket.find_elements_by_css_selector('span.trashable')
    for dropped in a:
        if (data_id == dropped.get_attribute("data-id")):
            n = n + 1
    assert n == int(count), (
        "Expected %s elements in the %s timeslot, instead it contains %s" % (
            count, time, n))


@step(u'Then there are no pills in "([^"]*)"')
def then_there_are_no_pills_in_timeslot(step, timeslot):
    bucket = get_bucket(timeslot)
    assert bucket is not None, (
        "Time slot must be specified as day or evening. "
        "No time slot called %s found" % time)

    a = bucket.find_elements_by_css_selector('span.trashable')
    assert len(a) == 0, (
        "Expected no pills in bucket %s, instead it contains %s pills" % (
            bucket, len(a)))


@step(u'Then there are (\d+) pills in "([^"]*)"')
def then_there_are_count_pills_in_timeslot(step, count, timeslot):
    bucket = get_bucket(timeslot)
    assert bucket is not None, (
        "Time slot must be specified as day or evening. No time slot "
        "called %s found" % time)

    a = bucket.find_elements_by_css_selector('span.trashable')
    assert len(a) == int(count), (
        "Expected %s pills in bucket %s, instead it contains %s pills" % (
            count, bucket, len(a)))


@step(u'When I drag "([^"]*)" from "([^"]*)" to "([^"]*)"')
def when_i_drag_pill_from_time1_to_time2(step, pill, time1, time2):
    # get the data id for this pill
    pill = find_pill(pill)
    assert pill is not None, "No pill named %s found." % pill
    draggable = pill.find_element_by_css_selector(
        "div.pill-image span.draggable")
    assert draggable is not None, (
        "This pill is not constructed properly: %s" % pill)
    data_id = draggable.get_attribute("data-id")
    bucket = get_bucket(time1)
    assert bucket is not None, (
        "Source time slot must be specified as day or evening. "
        "No time slot called %s found" % time)
    dest = get_bucket(time2)
    assert dest is not None, (
        "Destination time slot must be specified as day or evening. "
        "No time slot called %s found" % time)

    a = bucket.find_elements_by_css_selector('span.trashable')
    assert len(a) > 0, (
        "Expected at least 1 pill in bucket %s, instead it "
        "contains %s pills" % (bucket, len(a)))
    action = False
    for dropped in a:
        if (data_id == dropped.get_attribute("data-id")):
            # found it, now, drag it to the second bucket
            action_chains = ActionChains(world.browser)
            action_chains.drag_and_drop(dropped, dest).perform()
            action = True
    assert action, (
        "No dropped pills named %s found in %s slot" % (pill, time1))


@step(u'When I drag "([^"]*)" off "([^"]*)"')
def when_i_drag_pill_off_time(step, pill, time):
        # get the data id for this pill
    pill = find_pill(pill)
    assert pill is not None, "No pill named %s found." % (pill)
    draggable = pill.find_element_by_css_selector(
        "div.pill-image span.draggable")
    assert draggable is not None, (
        "This pill is not constructed properly: %s" % pill)
    data_id = draggable.get_attribute("data-id")

    bucket = get_bucket(time)
    assert bucket is not None, (
        "Source time slot must be specified as day or evening. "
        "No time slot called %s found" % time)

    dest = world.browser.find_element_by_id('pill-game-container')
    assert dest is not None, (
        "Destination time slot must be specified as day or evening. "
        "No time slot called %s found" % time)

    a = bucket.find_elements_by_css_selector('span.trashable')
    assert len(a) > 0, (
        "Expected at least 1 pill in bucket %s, "
        "instead it contains %s pills" % (
            bucket, len(a)))

    action = False
    for dropped in a:
        if (data_id == dropped.get_attribute("data-id")):
            # found it, now, drag it to the second bucket
            action_chains = ActionChains(world.browser)
            action_chains.drag_and_drop(dropped, dest).perform()
            action = True

    assert action, "No dropped pills named %s found in %s slot" % (
        pill, time)


@step(u'Specify "([^"]*)" time as "([^"]*)"')
def specify_timeslot_time_as_time(step, timeslot, time):
    id = None
    if timeslot == "daytime":
        id = "day_pills_time"
    elif timeslot == "evening":
        id = "night_pills_time"
    assert id is not None, (
        "Time slot must be specified as day or evening. "
        "No time slot called %s found" % timeslot)

    elt = world.browser.find_element_by_id(id)
    assert elt is not None, "Select element not found %s" % id

    then_i_wait_count_second(step, 1)
    select = Select(elt)
    try:
        select.select_by_visible_text(time)
    except NoSuchElementException:  # nosec
        pass


@step(u'Then the "([^"]*)" time is "([^"]*)"')
def then_the_timeslot_time_is_time(step, timeslot, time):
    id = None
    if timeslot == "daytime":
        id = "day_pills_time"
    elif timeslot == "evening":
        id = "night_pills_time"
    assert id is not None, (
        "Time slot must be specified as day or evening. "
        "No time slot called %s found" % timeslot)

    elt = world.browser.find_element_by_id(id)
    assert elt is not None, "Select element not found %s" % id

    value = elt.get_attribute("value")
    assert time == value, "%s time expected %s, actual %s" % (
        timeslot, time, value)


@step(u"Then I'm asked to enter a pill name")
def then_i_m_asked_to_enter_a_pill_name(step):
    alert = world.browser.switch_to_alert()
    assert alert.text.startswith(
        "Please enter a name for this medication"), "Alert text valid"
    alert.accept()


@step(u"Then I'm told I can only enter 10 pills")
def then_i_m_told_i_can_only_enter_10_pills(step):
    alert = world.browser.switch_to_alert()
    assert alert.text.startswith("You can only enter 10 pills"), (
        "Alert text valid")
    alert.accept()


@step(u"Then I dismiss second dialog")
def then_i_dismiss_second_dialog(step):
    alert = world.browser.switch_to_alert()
    alert.accept()


@step(u'When I name pill (\d+) "([^"]*)"')
def when_i_name_pill_index_name(step, index, name):
    idx = int(index) - 1
    a = world.browser.find_elements_by_css_selector('div.pill')
    assert len(a) > idx, (
        "Can't find pill %s as there are only %s pills in the list" % (
            index, len(a)))
    pill = a[idx]

    input = pill.find_element_by_css_selector('div.pill-text input')
    input.send_keys(name)

    # click outside the input box to force blur event
    elt = world.browser.find_element_by_id('pill-game-container')
    elt.click()


@step(u'Then I wait (\d+) second')
def then_i_wait_count_second(step, count):
    n = int(count)
    time.sleep(n)


@step(u'When I delete "([^"]*)"')
def when_i_delete_pill(step, pill):
    pill = find_pill(pill)
    delete_button = pill.find_element_by_css_selector(
        'input.pill-delete-image')
    delete_button.click()
