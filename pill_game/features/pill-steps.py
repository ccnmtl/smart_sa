import sys, time
from lettuce import before, after, world, step
from pill_game.models import PillGame
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select

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
    
@step(u'When I drop "([^"]*)" into the "([^"]*)" slot')
def when_i_drop_pill_into_the_time_slot(step, pill, time):
    pill = find_pill(pill)
    assert pill != None, "No pill named %s found." % pill
    
    # get the draggable span within
    draggable = pill.find_element_by_css_selector("div.pill-image span.draggable")
    assert draggable != None, "This pill is not constructed properly" % pill
    
    bucket = None
    if time == "daytime":
        bucket = world.firefox.find_element_by_id("day")
    elif time == "evening":
        bucket = world.firefox.find_element_by_id("night")
    assert bucket != None, "Time slot must be specified as day or evening. No time slot called %s found" % time
    
    action_chains = ActionChains(world.firefox)
    action_chains.drag_and_drop(draggable, bucket).perform()

@step(u'Then there is (\d+) "([^"]*)" in the "([^"]*)" slot')
def then_there_is_count_pill_in_the_time_slot(step, count, pill, time):
    pill = find_pill(pill)
    assert pill != None, "No pill named %s found. %s" % (pill, count)
    
    # get the draggable span within
    draggable = pill.find_element_by_css_selector("div.pill-image span.draggable")
    assert draggable != None, "This pill is not constructed properly" % pill
    
    # get the data-id
    data_id = draggable.get_attribute("data-id")
    
    bucket = None
    if time == "daytime":
        bucket = world.firefox.find_element_by_id("day")
    elif time == "evening":
        bucket = world.firefox.find_element_by_id("night")
    assert bucket != None, "Time slot must be specified as day or evening. No time slot called %s found" % time

    n = 0
    a = bucket.find_elements_by_css_selector('span.trashable')
    for dropped in a:
        if (data_id == dropped.get_attribute("data-id")):
            n = n + 1
    
    assert n == int(count), "Expected %s elements in the %s timeslot, instead it contains %s" % (count, time, n)

    
@step(u'Then there are no pills in the "([^"]*)" slot')
def then_there_are_no_pills_in_the_timeslot_slot(step, timeslot):
    bucket = None
    if timeslot == "daytime":
        bucket = world.firefox.find_element_by_id("day")
    elif timeslot == "evening":
        bucket = world.firefox.find_element_by_id("night")
    assert bucket != None, "Time slot must be specified as day or evening. No time slot called %s found" % time

    a = bucket.find_elements_by_css_selector('span.trashable')
    assert len(a) == 0, "Expected no pills in bucket %s, instead it contains %s pills" % (bucket, len(a))
    


@step(u'When I drag "([^"]*)" from the "([^"]*)" slot into the "([^"]*)" slot')
def when_i_drag_pill_from_the_time1_slot_into_the_time2_slot(step, pill, time1, time2):
    # get the data id for this pill
    pill = find_pill(pill)
    assert pill != None, "No pill named %s found. %s" % (pill, count)
    draggable = pill.find_element_by_css_selector("div.pill-image span.draggable")
    assert draggable != None, "This pill is not constructed properly" % pill
    data_id = draggable.get_attribute("data-id")

    # Verify there's a dropped pill in bucket 1
    bucket = None
    if time1 == "daytime":
        bucket = world.firefox.find_element_by_id("day")
    elif time1 == "evening":
        bucket = world.firefox.find_element_by_id("night")
    assert bucket != None, "Source time slot must be specified as day or evening. No time slot called %s found" % time
    
    dest = None
    if time2 == "daytime":
        dest = world.firefox.find_element_by_id("day")
    elif time2 == "evening":
        dest = world.firefox.find_element_by_id("night")
    assert dest != None, "Destination time slot must be specified as day or evening. No time slot called %s found" % time

    a = bucket.find_elements_by_css_selector('span.trashable')
    assert len(a) > 0, "Expected at least 1 pill in bucket %s, instead it contains %s pills" % (bucket, len(a))
    
    action = False
    for dropped in a:
        if (data_id == dropped.get_attribute("data-id")):
            # found it, now, drag it to the second bucket
            action_chains = ActionChains(world.firefox)
            action_chains.drag_and_drop(dropped, dest).perform()
            action = True
            
    assert action, "No dropped pills named %s found in %s slot" % (pill, time1)    
    
@step(u'Specify "([^"]*)" schedule as "([^"]*)"')
def specify_timeslot_schedule_as_time(step, timeslot, time):
    id = None
    if timeslot == "daytime":
        id = "day_pills_time"
    elif timeslot == "evening":
        id = "night_pills_time"
    assert id != None, "Time slot must be specified as day or evening. No time slot called %s found" % timeslot
        
    elt = world.firefox.find_element_by_id(id)
    assert elt != None, "Select element not found %s" % id
    
    select = Select(elt)
    select.select_by_visible_text(time)    
    
@step(u'Then the "([^"]*)" schedule is "([^"]*)"')
def then_the_timeslot_schedule_is_time(step, timeslot, time):
    id = None
    if timeslot == "daytime":
        id = "day_pills_time"
    elif timeslot == "evening":
        id = "night_pills_time"
    assert id != None, "Time slot must be specified as day or evening. No time slot called %s found" % timeslot
        
    elt = world.firefox.find_element_by_id(id)
    assert elt != None, "Select element not found %s" % id
    
    value = elt.get_attribute("value")
    assert time == value, "%s time expected %s, actual %s" % (timeslot, time, value)




    
    