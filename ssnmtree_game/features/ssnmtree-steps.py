from lettuce import world, step
import sys, time

@step('I fill in the SSNM Tree with "([^"]*)"')
def fill_in_ssnmtree(self, text):
    if not world.using_selenium:
        assert False, "this step needs to be implemented for the django test client"
    for i in world.firefox.find_elements_by_tag_name('input'):
        if i.get_attribute('type') == 'text':
            i.clear()
            i.send_keys(text)

@step('there is a filled in SSNM Tree with "([^"]*)"')
def filled_in_ssnmtree(self, text):
    if not world.using_selenium:
        assert False, "this step needs to be implemented for the django test client"
    all_filled = True
    for i in world.firefox.find_elements_by_tag_name('input[type=text]'):
        if i.get_attribute('type') == 'text':
            if i.get_attribute('value') != text:
                all_filled = False
    assert all_filled
    
