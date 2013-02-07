from lettuce import world, step
from smart_sa.intervention.models import Participant, Deployment
from lettuce.django import django_url
try:
    from lxml import html
except ImportError:
    pass


@step(u'there is an edit deployment form')
def there_is_an_edit_deployment_form(step):
    found = False
    for form in world.dom.cssselect("form"):
        if form.attrib.get('action', '') == "/set_deployment/":
            found = True
    assert found


@step(u'there is not an edit deployment form')
def there_is_not_an_edit_deployment_form(step):
    found = False
    for form in world.dom.cssselect("form"):
        if form.attrib.get('action', '') == "/set_deployment/":
            found = True
    assert not found


@step(u'there is a counselors table')
def there_is_a_counselors_table(step):
    try:
        world.dom.get_element_by_id("counselors")
        assert True
    except KeyError:
        assert False, 'no counselors table visible to admin'


@step(u'there is not a counselors table')
def there_is_not_a_counselors_table(step):
    try:
        world.dom.get_element_by_id("counselors")
        assert False, "counselors table is visible to non-admin"
    except KeyError:
        assert True


@step(u'I go to the Edit Participant page for "([^"]*)"')
def i_go_to_the_edit_participant_page(step, participant_name):
    p = Participant.objects.get(name=participant_name)
    world.firefox.get(django_url("/manage/participant/%d/edit/" % p.id))


@step(u'I toggle the Defaulter checkbox')
def i_toggle_the_defaulter(step):
    cb = world.firefox.find_element_by_xpath("//input[@name=\"defaulter\"]")
    cb.click()


@step(u'I save')
def i_save(step):
    s = world.firefox.find_element_by_xpath("//input[@type=\"submit\"]")
    s.click()


@step(u'the "([^"]*)" field has the value "([^"]*)"')
def the_field_has_the_value(step, field_name, field_value):
    f = world.firefox.find_element_by_xpath(
        "//input[@name=\"%s\"]" % field_name)
    assert f.get_attribute('value') == field_value


@step(u'participant named "([^"]*)" exists')
def participant_exists(step, name):
    if Participant.objects.filter(name=name).count() == 0:
        Participant.objects.create(name=name, id_number=name, patient_id=name)


@step(u'I go to the Add Participant Page')
def i_go_to_the_add_participant_page(step):
    if world.using_selenium:
        world.firefox.get(django_url("/manage/add_participant/"))
    response = world.client.get(
        django_url("/manage/add_participant/"), follow=True)
    world.response = response
    world.dom = html.fromstring(response.content)


@step(u'there is an error message')
def there_is_an_error_message(step):
    if not world.using_selenium:
        assert False, 'This step must be implemented for django test client'
    world.firefox.find_element_by_xpath("//p[@class=\"error\"]")


@step(u'the deployment is set to "([^"]*)"')
def the_deployment_is_set_to(step, name):
    d = Deployment.objects.all()[0]
    d.name = name
    d.save()
