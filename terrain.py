from lettuce.django import django_url
from lettuce import before, after, world, step
from django.test import client
from intervention.models import Intervention

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
#    time.sleep(3)
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
    if world.using_selenium:
        pass
    else:
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
    if world.using_selenium:
        world.firefox.get(django_url("/accounts/logout/"))
        world.firefox.get(django_url("/accounts/login/?next=/intervention/"))
        username_field = world.firefox.find_element_by_id("id_username")
        password_field = world.firefox.find_element_by_id("id_password")
        form = world.firefox.find_element_by_id("login-form")
        username_field.send_keys("testcounselor")
        password_field.send_keys("test")
        form.submit()
        assert world.firefox.current_url.endswith("/intervention/"), world.firefox.current_url
        assert "testcounselor" in world.firefox.page_source, world.firefox.page_source
    else:
        world.client.login(username='testcounselor',password='test')

@step(u'I am logged in as an admin')
def given_i_am_logged_in_as_an_admin(step):
    if world.using_selenium:
        pass
    else:
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
    try:
        link = world.firefox.find_element_by_link_text(text)
        assert link.is_displayed()
        link.click()
    except:
        world.firefox.get_screenshot_as_file("/tmp/selenium.png")
        assert False, link.location


@step(u'I fill in "([^"]*)" in the "([^"]*)" form field')
def i_fill_in_the_form_field(step, value, field_name):
    if not world.using_selenium:
        return

    world.firefox.find_element_by_id(field_name).send_keys(value)

@step(u'I submit the "([^"]*)" form')
def i_submit_the_form(step, id):
    if not world.using_selenium:
        return

    world.firefox.find_element_by_id(id).submit()

@step(u'I am on the Intervention page')
def i_am_on_the_intervention_page(step):
    if not world.using_selenium:
        return
    i = Intervention.objects.all()[0]
    assert world.firefox.current_url.endswith("/intervention/%d/" % i.id), world.firefox.current_url
    assert world.firefox.find_elements_by_tag_name('h2')[0].text == "Sessions"

@step(u'I click on Session (\d+)')
def i_click_session(step, session_number):
    if not world.using_selenium:
        return
    link = world.firefox.find_element_by_partial_link_text("Session %s:" % session_number)
    link.click()

@step(u'I click on Activity (\d+)')
def i_click_activity(step, activity_number):
    if not world.using_selenium:
        return
    try:
        link = world.firefox.find_element_by_partial_link_text("Activity %s:" % activity_number)
        link.click()
        time.sleep(1)
    except:
        assert False, world.firefox.page_source

@step(u'I click on Complete Activity')
def i_click_on_complete_activity(step):
    if not world.using_selenium:
        return
    try:
        link = world.firefox.find_element_by_partial_link_text("Complete This Activity")
        link.click()
        time.sleep(1)
    except:
        link = world.firefox.find_element_by_partial_link_text("Wrap-Up")
        link.click()
        time.sleep(1)

@step(u'I am on the Session (\d+) page')
def i_am_on_the_session_page(step,session_id):
    if not world.using_selenium:
        return
    assert world.firefox.find_elements_by_tag_name('h2')[0].text.startswith("Session %s:" % session_id)

@step(u'I am on the Activity (\d+) page')
def i_am_on_the_activity_page(step,activity_id):
    if not world.using_selenium:
        return
    """<div id="breadcrumb-text">
		You are currently in: <span class="breadcrumb-text-current">Session 1: Getting Started &rarr; Activity 2: Your questions and concerns</span>
	</div>"""
    breadcrumb = world.firefox.find_element_by_id("breadcrumb-text")
    assert "Activity %s:" % activity_id in breadcrumb.text, breadcrumb.text

@step('there is a game')
def there_is_a_game(self):
    if not world.using_selenium:
        return
    assert world.firefox.find_element_by_id('gamebox')

@step('there is an assessmentquiz')
def there_is_an_assessmentquiz(self):
    if not world.using_selenium:
        return
    assert world.firefox.find_element_by_id('assessmentquiz')


@step('I go back')
def i_go_back(self):
    """ need to back out of games currently"""
    if not world.using_selenium:
        return
    world.firefox.back()

@step('I fill in all (\d)s in the quiz')
def fill_in_quiz(self,value):
    if not world.using_selenium:
        return
    for i in world.firefox.find_elements_by_tag_name('input'):
        if i.get_attribute('type') == 'radio' and i.get_attribute('value') == value:
            i.click()

