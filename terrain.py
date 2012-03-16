from lettuce.django import django_url
from lettuce import before, after, world, step
from django.test import client
import time
try:
    from lxml import html
    from selenium import webdriver
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.common.keys import Keys
    import selenium
except:
    pass

@before.all
def setup_browser():
    world.firefox = webdriver.Firefox()
    time.sleep(5)
    world.client = client.Client()
    world.using_selenium = False

@after.all
def teardown_browser(total):
    world.firefox.quit()

@step(u'Using selenium')
def using_selenium(step):
    world.using_selenium = True

@step(u'Finished using selenium')
def finished_selenium(step):
    world.using_selenium = False

@step(r'I access the url "(.*)"')
def access_url(step, url):
    if world.using_selenium:
        world.firefox.get(django_url(url))
    else:
        response = world.client.get(django_url(url))
        world.dom = html.fromstring(response.content)

@step(u'I am not logged in')
def i_am_not_logged_in(step):
    world.client.logout()

@step(u'I access the management console')
def i_access_the_management_console(step):
    response = world.client.get(django_url("/manage/"),follow=True)
    world.response = response
    world.dom = html.fromstring(response.content)

@step(u'I am taken to a login screen')
def i_am_taken_to_a_login_screen(step):
    assert len(world.response.redirect_chain) > 0
    (url,status) = world.response.redirect_chain[0]
    assert status == 302, status
    assert "/login/" in url, "URL redirected to was %s" % url

@step(u'I am logged in as a counselor')
def i_am_logged_in_as_a_counselor(step):
    world.client.login(username='testcounselor',password='test')

@step(u'I am logged in as an admin')
def given_i_am_logged_in_as_an_admin(step):
    world.client.login(username='testadmin',password='test')

@step(u'there is not an? "([^"]*)" link')
def there_is_not_a_link(step, text):
    found = False
    for a in world.dom.cssselect("a"):
        if a.text and a.text.strip() == text:
            found = True
    assert not found

@step(u'there is an? "([^"]*)" link')
def there_is_a_link(step, text):
    found = False
    for a in world.dom.cssselect("a"):
        if a.text and a.text.strip() == text:
            found = True
    assert found

@step(u'there is a location edit form')
def there_is_a_location_edit_form(step):
    found = False
    for f in world.dom.cssselect("form"):
        if f.action == "/set_deployment/":
            found = True
    assert found

@step(u'I click the "([^"]*)" link')
def i_click_the_link(step, text):
    if not world.using_selenium:
        return
    link = world.firefox.find_element_by_link_text(text)
    assert link.is_displayed()
    link.click()


@step(u'I fill in "([^"]*)" in the "([^"]*)" form field')
def i_fill_in_the_form_field(step, value, field_name):
    if not world.using_selenium:
        return

    assert False, 'This step must be implemented'

@step(u'I click the "([^"]*)" submit button')
def i_click_the_submit_button(step, label):
    if not world.using_selenium:
        return

    assert False, 'This step must be implemented'

