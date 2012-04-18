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


