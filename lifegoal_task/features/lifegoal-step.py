from lettuce import world, step
import sys, time

def get_input(name):
    elt = None
    if name == "Step 2":
        elt = world.firefox.find_element_by_css_selector("div#step2 input")
    elif name == "Step 3":
        elt = world.firefox.find_element_by_css_selector("div#step3 input")
    elif name == "Step 4":
        elt = world.firefox.find_element_by_css_selector("div#step4 input")
    elif name == "Goal":
        elt = world.firefox.find_element_by_css_selector("div#goal input")
        
    assert elt != None, "%s does not exist" % input       
    assert elt.get_attribute('type') == 'text'
    
    return elt


@step(u'When I enter "([^"]*)" for "([^"]*)"')
def when_i_enter_value_for_input(step, value, input):
    elt = get_input(input)
    elt.clear()
    for c in value:
        elt.send_keys(c)

@step(u'Then "([^"]*)" is "([^"]*)"')
def then_input_is_value(step, input, value):
    elt = get_input(input)
    actual = elt.get_attribute("value") 
    assert actual == value, "Expected %s to equal %s. Actually is %s" % (input, value, actual)
   
@step(u'Then I wait (\d+) second')
def then_i_wait_count_second(step, count):
    n = int(count)
    time.sleep(n)
    
    
    
        
    
    
