import sys, time
from lettuce import world, step

@step(u'there is an edit deployment form')
def there_is_an_edit_deployment_form(step):
    found = False
    for form in world.dom.cssselect("form"):
        if form.attrib.get('action','') == "/set_deployment/":
            found = True
    assert found

@step(u'there is not an edit deployment form')
def there_is_not_an_edit_deployment_form(step):
    found = False
    for form in world.dom.cssselect("form"):
        if form.attrib.get('action','') == "/set_deployment/":
            found = True
    assert not found

@step(u'there is a counselors table')
def there_is_a_counselors_table(step):
    try:
        t = world.dom.get_element_by_id("counselors")
        assert True
    except KeyError:
        assert False, 'no counselors table visible to admin'

@step(u'there is not a counselors table')
def there_is_not_a_counselors_table(step):
    try:
        t = world.dom.get_element_by_id("counselors")
        assert False, "counselors table is visible to non-admin"
    except KeyError:
        assert True



