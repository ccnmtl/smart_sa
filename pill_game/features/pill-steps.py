import sys, time
from lettuce import before, after, world, step
from pill_game.models import PillGame
from selenium.webdriver import ActionChains

def find_pill(name):
    a = world.firefox.find_elements_by_css_selector('div.pill')
    for pill in a:
        span = pill.find_element_by_css_selector('div.pill-text span')
        if span.text.startswith(name):
            return pill 

    return None

@step(u'There is a "([^"]*)" title')
def there_is_a_group1_title(step, group1):
    i = world.firefox.find_element_by_css_selector('#pill-list h4')
    assert i.text == group1, i.text

@step(u'There are (\d+) pills')
def there_are_n_pills(step, n):
    a = world.firefox.find_elements_by_css_selector('#pill-list div.pill')
    assert len(a) == int(n), "Expecting %s pills, but see %s" % (n, len(a))

@step(u'There is a pill named "([^"]*)"')
def there_is_a_pill_named_name(step, name):
    pill = find_pill(name)
    assert pill != None, "No pill named %s found" % name
    
@step(u'There is not an Add Pill button')
def there_is_not_an_add_pill_button(step):
    try:
        i = world.firefox.find_element_by_id('add-a-pill')
        assert False, 'The Add Pill button should not be displayed in this mode'
    except:
        pass

@step(u'There is an Add Pill button')
def there_is_an_add_pill_button(step):
    i = world.firefox.find_element_by_id('add-a-pill')
    assert i != None
    
@step(u'Drop "([^"]*)" into the "([^"]*)" slot')
def drop_pill_into_the_time_slot(step, pill, time):
    pill = find_pill(pill)
    assert pill != None, "No pill named %s found." % pill
    
    # get the draggable span within
    draggable = pill.find_element_by_css_selector("div.pill-image span.draggable")
    assert draggable != None, "This pill is not constructed properly" % pill
    
    bucket = None
    if time == "day":
        bucket = world.firefox.find_element_by_id("day")
    elif time == "evening":
        bucket = world.firefox.find_element_by_id("night")
    assert bucket != None, "Time slot must be specified as day or evening. No time slot called %s found" % time
    
    action_chains = ActionChains(world.firefox)
    action_chains.drag_and_drop(draggable, bucket).perform()

@step(u'There is (\d+) "([^"]*)" in the "([^"]*)" slot')
def there_is_count_pill_in_the_time_slot(step, count, pill, time):
    pill = find_pill(pill)
    assert pill != None, "No pill named %s found." % pill
    
    # get the draggable span within
    draggable = pill.find_element_by_css_selector("div.pill-image span.draggable")
    assert draggable != None, "This pill is not constructed properly" % pill
    
    # get the data-id
    data_id = draggable.get_attribute("data_id")
    
    bucket = None
    if time == "day":
        bucket = world.firefox.find_element_by_id("day")
    elif time == "evening":
        bucket = world.firefox.find_element_by_id("night")
    assert bucket != None, "Time slot must be specified as day or evening. No time slot called %s found" % time

    n = 0
    a = bucket.find_elements_by_css_selector('span.trashable')
    for dropped in a:
        if (data_id == dropped.get_attribute("data_id")):
            n = n + 1
    
    assert n == int(count), "Expected %s elements in the %s timeslot, instead it contains %s" % (count, time, n)
    
    
    
    