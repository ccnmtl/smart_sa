from lettuce import before, after, world, step
import sys, time

@step(u'There is a "([^"]*)" title')
def there_is_a_group1_title(step, group1):
    i = world.firefox.find_element_by_css_selector('#pill-list h4')
    assert i.text == group1, i.text

@step(u'There are (\d+) pills')
def there_are_n_pills(step, n):
    a = world.firefox.find_elements_by_css_selector('#pill-list div.pill')
    assert len(a) == int(n), "Expecting %s pills, but see %s" % (n, len(a))