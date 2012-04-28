from lettuce.django import django_url
from lettuce import before, after, world, step
import sys, time

@step(u'I toggle personal challenge')
def i_toggle_personal_challenge(step):
    if not world.using_selenium:
        assert False, "this step needs to be implemented for the django test client"
    i = world.firefox.find_element_by_css_selector('input[type="checkbox"]')
    try:
        i.click()
        time.sleep(1)
    except:
        pass
    
@step(u'When I click the Save Plan button')
def when_i_click_the_save_plan_button(step):
    elt = world.firefox.find_element_by_css_selector('div#actionplan_form input[type="submit"]');
    try:
        elt.click()
    except:
        pass
    
@step(u'I select barrier (\d+)')
def i_select_barrier(step, barrier):
    if not world.using_selenium:
        assert False, "this step needs to be implemented for the django test client"

    barrier_idx = int(barrier) - 1 # Assumes 1 based indexing
    elts = world.firefox.find_elements_by_css_selector('div.issue-selector div.issue-number')

    for idx, val in enumerate(elts):
        if idx == barrier_idx:
            try:
                val.click()
            except:
                pass
            
@step(u'Then barrier (\d+) has "([^"]*)"')
def then_barrier_number_has_state(step, number, state):
    if not world.using_selenium:
        assert False, "this step needs to be implemented for the django test client"

    barrier_idx = int(number) - 1
    elts = world.firefox.find_elements_by_css_selector('div.issue-selector div.issue-number')
    
    for idx, val in enumerate(elts):
        if idx == barrier_idx:
            clazz = val.get_attribute("class")
            assert state in clazz, clazz
            break  


@step(u'Then barrier (\d+) does not have "([^"]*)"')
def then_barrier_number_does_not_have_state(step, number, state):
    if not world.using_selenium:
        assert False, "this step needs to be implemented for the django test client"

    barrier_idx = int(number) - 1
    elts = world.firefox.find_elements_by_css_selector('div.issue-selector div.issue-number')
    
    for idx, val in enumerate(elts):
        if idx == barrier_idx:
            clazz = val.get_attribute("class")
            assert state not in clazz, clazz
            break
        
@step(u'there is no issue selector')
def there_is_no_issue_selector(step):
    i = world.firefox.find_element_by_id('issue-selector')
    assert i.is_displayed() == False, "Issue selector should be invisible now"

@step(u'there is an issue selector')
def there_is_an_issue_selector(step):
    i = world.firefox.find_element_by_id('issue-selector')
    assert i.is_displayed() == True, "Issue selector should be visible now"

@step(u'i navigate "([^"]*)"')
def i_navigate_direction(step, direction):
    if direction == "left":
        i = world.firefox.find_element_by_css_selector('#previous_issue')
    elif direction == "right":
        i = world.firefox.find_element_by_css_selector('#next_issue')
    
    try:
        i.click()
    except:
        pass
    
@step(u'there is no left arrow')
def there_is_no_left_arrow(step):
    i = world.firefox.find_element_by_css_selector('#previous_issue img')
    assert i.is_displayed() == False, "Left arrow should be invisible now"

@step(u'there is a left arrow')
def there_is_a_left_arrow(step):
    i = world.firefox.find_element_by_css_selector('#previous_issue img')
    assert i.is_displayed() == True, "Left arrow should be visible now"

@step(u'there is no right arrow')
def there_is_no_right_arrow(step):
    i = world.firefox.find_element_by_css_selector('#next_issue img')
    assert i.is_displayed() == False, "right arrow should be invisible now"

@step(u'there is a right arrow')
def there_is_a_left_arrow(step):
    i = world.firefox.find_element_by_css_selector('#next_issue img')
    assert i.is_displayed() == True, "right arrow should be visible now"
                    
   
@step(u'there is no action plan button')
def there_is_no_action_plan_button(step):
    i = world.firefox.find_element_by_css_selector('#actionplan a')
    assert i.is_displayed() == False, "Make Plan should be invisible now"
      
@step(u'Then there is a Make Plan button')
def then_there_is_a_make_plan_button(step):
    i = world.firefox.find_element_by_css_selector('#actionplan a')
    assert i.is_displayed() == True, "element #actionplan a is visible"
    assert i.text == "Make Plan", i.text
    
@step(u'Then there is an Edit Plan button')
def then_there_is_an_edit_plan_button(step):
    i = world.firefox.find_element_by_css_selector('#actionplan a')
    assert i.is_displayed() == True, "element #actionplan a is visible"
    assert i.text == "Edit Plan", i.text

@step(u'there is no Action Plan form')
def then_there_is_no_action_plan_form(step):
    time.sleep(1)
    elt = world.firefox.find_element_by_id('actionplan_form')
    assert elt.is_displayed() == False, "element #actionplan_form should not be visible"
    
@step(u'Then there is an Action Plan form')
def then_there_is_an_action_plan_form(step):
    elt = world.firefox.find_element_by_id('actionplan_form')
    assert elt.is_displayed() == True, "element #actionplan_form should be visible"

@step(u'When I type "([^"]*)" in "([^"]*)"')
def when_i_type_text_in_elementId(step, text, elementId):
    elt = world.firefox.find_element_by_id(elementId)
    elt.send_keys(text)
    
@step(u'Then "([^"]*)" reads "([^"]*)"')
def then_elementId_reads_text(step, elementId, text):
    elt = world.firefox.find_element_by_id(elementId)
    elt_text = elt.get_attribute("value")
    assert elt_text == text, elt_text
    
@step(u'Then I can specify my issue')
def then_i_can_specify_my_issue(step):
    elt = world.firefox.find_element_by_css_selector('div.issue-subtext textarea')
    assert elt.is_displayed() == True, "element div.issue-subtext textarea should be visible"
    
@step(u'Then I cannot specify my issue')
def then_i_cannot_specify_my_issue(step):
    elt = world.firefox.find_element_by_css_selector('div.issue-subtext textarea')
    assert elt.is_displayed() == False, "element div.issue-subtext textarea should be invisible"
    
@step(u'Then I specify my issue as "([^"]*)"')
def then_i_specify_my_issue(step, text):
    elt = world.firefox.find_element_by_css_selector('div.issue-subtext textarea')
    elt.send_keys(text)

@step(u'my issue is "([^"]*)"')
def my_issue_is(step, text):
    elt = world.firefox.find_element_by_css_selector('div.issue-subtext textarea')
    elt_text = elt.get_attribute("value")
    assert elt_text == text, elt_text
      
