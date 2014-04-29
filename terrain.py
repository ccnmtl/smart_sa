# -*- coding: utf-8 -*-
from lettuce.django import get_server
get_server()
from lettuce.django import django_url
from lettuce import before, after, world, step
from django.conf import settings
from django.test import client
from smart_sa.intervention.models import Intervention, Participant, ClientSession, Activity
import os
import sys

import time
try:
    from lxml import html
    from selenium import webdriver
    from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.common.keys import Keys
    import selenium
except:
    pass


@before.harvest
def setup_browser(variables):
    browser = getattr(settings, 'BROWSER', None)
    if browser == 'Headless':
        # this should really be called 'world.browser'
        # but we'll fix that later
        world.firefox = webdriver.PhantomJS()
    else:
        ff_profile = FirefoxProfile()
        ff_profile.set_preference("webdriver_enable_native_events", False)
        world.firefox = webdriver.Firefox(ff_profile)
    world.client = client.Client()
    world.using_selenium = False


@after.harvest
def teardown_browser(total):
    world.firefox.quit()


@before.harvest
def setup_database(_foo):
    # make sure we have a fresh test database
    os.system("rm -f lettuce.db")
    os.system("cp test_data/test.db lettuce.db")


@after.harvest
def teardown_database(_foo):
    os.system("rm -f lettuce.db")


@before.each_scenario
def clear_participant_data(_foo):
    for p in ['test',]:
        participant = Participant.objects.get(name=p)
        participant.clear_all_data()
        participant.save()

@step(u'Using selenium')
def using_selenium(step):
    world.using_selenium = True

@step(u'Finished using selenium')
def finished_selenium(step):
    world.using_selenium = False

@before.each_scenario
def clear_selenium(step):
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
        world.firefox.get(django_url("/accounts/logout/"))
    else:
        world.client.logout()

@step(u'I access the management console')
def i_access_the_management_console(step):
    if world.using_selenium:
        world.firefox.get(django_url("/manage/"))
    else:
        response = world.client.get(django_url("/manage/"),follow=True)
        world.response = response
        world.dom = html.fromstring(response.content)

@step(u'I access the counselor landing page')
def i_access_the_counselor_landing_page(step):
    if world.using_selenium:
        world.firefox.get(django_url("/intervention/"))
    else:
        response = world.client.get(django_url("/intervention/"),follow=True)
        world.response = response
        world.dom = html.fromstring(response.content)


@step(u'I am taken to a login screen')
def i_am_taken_to_a_login_screen(step):
    assert len(world.response.redirect_chain) > 0
    (url,status) = world.response.redirect_chain[0]
    assert status == 302, status
    assert "/login/" in url, "URL redirected to was %s" % url

@step(u'I am taken to the index')
def i_am_taken_to_the_index(step):
    assert len(world.response.redirect_chain) > 0
    (url,status) = world.response.redirect_chain[0]
    assert status == 302, status
    assert "http://testserver/" == url, "URL redirected to was %s" % (url,)


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

@step(u'I log out')
def i_log_out(step):
    if world.using_selenium:
        world.firefox.get(django_url("/accounts/logout/"))
    else:
        response = world.client.get(django_url("/accounts/logout/"),follow=True)
        world.response = response
        world.dom = html.fromstring(response.content)

@step(u'I am logged in as an admin')
def given_i_am_logged_in_as_an_admin(step):
    if world.using_selenium:
        world.firefox.get(django_url("/accounts/logout/"))
        world.firefox.get(django_url("/accounts/login/?next=/intervention/"))
        username_field = world.firefox.find_element_by_id("id_username")
        password_field = world.firefox.find_element_by_id("id_password")
        form = world.firefox.find_element_by_id("login-form")
        username_field.send_keys("testadmin")
        password_field.send_keys("test")
        form.submit()
        assert world.firefox.current_url.endswith("/intervention/"), world.firefox.current_url
        assert "testadmin" in world.firefox.page_source, world.firefox.page_source
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
        for a in world.dom.cssselect("a"):
            if a.text:
                if text.strip().lower() in a.text.strip().lower():
                    href = a.attrib['href']
                    response = world.client.get(django_url(href))
                    world.dom = html.fromstring(response.content)
                    return
        assert False, "could not find the '%s' link" % text
    else:
        link = None
        try:
            link = world.firefox.find_element_by_partial_link_text(text)
            assert link.is_displayed()
            link.click()
        except:
            try:
                time.sleep(1)
                link = world.firefox.find_element_by_partial_link_text(text)
                assert link.is_displayed()
                link.click()
            except:
                world.firefox.get_screenshot_as_file("/tmp/selenium.png")
                assert False, link.location


@step(u'I fill in "([^"]*)" in the "([^"]*)" form field')
def i_fill_in_the_form_field(step, value, field_name):
    # note: relies on input having id set, not just name
    if not world.using_selenium:
        assert False, "this step needs to be implemented for the django test client"

    world.firefox.find_element_by_id(field_name).send_keys(value)

@step(u'I submit the "([^"]*)" form')
def i_submit_the_form(step, id):
    if not world.using_selenium:
        assert False, "this step needs to be implemented for the django test client"

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
        assert False, "this step needs to be implemented for the django test client"
    try:
        link = world.firefox.find_element_by_id("session%s" % session_number)
    except:
        import pdb;pdb.set_trace()
    link.click()

@step(u'I click on the Session Home')
def i_click_on_the_session_home(step):
    if not world.using_selenium:
        assert False, "this step needs to be implemented for the django test client"
    try:
        link = world.firefox.find_elements_by_css_selector("h2#sessioninfo a")[0]
        link.click()
    except:
        # if we can't find the sessioninfo element, it just means that we're already there
        pass

@step(u'I click on Activity (\d+)')
def i_click_activity(step, activity_number):
    if not world.using_selenium:
        assert False, "this step needs to be implemented for the django test client"
    try:
        link = world.firefox.find_element_by_partial_link_text("Activity %s:" % activity_number)
        link.click()
    except Exception, e:
        assert False, str(e)

@step(u'I click on Complete Activity')
def i_click_on_complete_activity(step):
    if not world.using_selenium:
        assert False, "this step needs to be implemented for the django test client"
    try:
        link = world.firefox.find_element_by_partial_link_text("Next →")
        link.click()
    except:
        link = world.firefox.find_element_by_partial_link_text("Wrap Up")
        link.click()

@step(u'I am on the Session (\d+) page')
def i_am_on_the_session_page(step,session_id):
    if not world.using_selenium:
        assert False, "this step needs to be implemented for the django test client"
    try:
        h2 = world.firefox.find_elements_by_tag_name('h2')[0]
    except:
        time.sleep(1)
        h2 = world.firefox.find_elements_by_tag_name('h2')[0]
    assert h2.text.startswith("Session %s:" % session_id)

@step(u'I am on the Activity (\d+) page')
def i_am_on_the_activity_page(step,activity_id):
    if not world.using_selenium:
        assert False, "this step needs to be implemented for the django test client"
    try:
        breadcrumb = world.firefox.find_element_by_id("breadcrumb-text")
    except:
        time.sleep(1)
        breadcrumb = world.firefox.find_element_by_id("breadcrumb-text")
    assert "Activity %s:" % activity_id in breadcrumb.text, breadcrumb.text

@step(u'Then I am on the "([^"]*)" Activity')
def i_am_on_the_activity_with_title(step, title):
    if not world.using_selenium:
        assert False, "this step needs to be implemented for the django test client"
    current_activity = world.firefox.find_elements_by_css_selector("h3")[0]
    title = title.replace("  "," ")
    assert current_activity.text == title, current_activity.text


@step('there is a game')
def there_is_a_game(self):
    if not world.using_selenium:
        assert len(world.dom.cssselect('#gamebox')) > 0
    else:
        assert world.firefox.find_element_by_id('gamebox')

@step('I go back')
def i_go_back(self):
    """ need to back out of games currently"""
    if not world.using_selenium:
        assert False, "this step needs to be implemented for the django test client"
    world.firefox.back()

@step(u'I have logged in a participant')
def i_have_logged_in_a_participant(step):
    if world.using_selenium:
        step.behave_as("""
        When I access the url "/"
        When I click the "Let's get started!" link
        When I click the "Counsel" link
        When I fill in "test" in the "name" form field
        When I fill in "test" in the "id_number" form field
        When I submit the "login-participant-form" form
        Then I am on the Intervention page
    """)
    else:
        response = world.client.post(django_url('/set_participant/'), {'name': 'test', 'id_number': 'test'})
        world.participant = Participant.objects.filter(name='test')[0]

@step(u'the participant has not completed any sessions')
def participant_has_not_completed_any_sessions(step):
    world.participant.participantsession_set.all().delete()
    world.participant.participantactivity_set.all().delete()


@step(u'I go to Activity (\d+) of Session (\d+)')
def i_go_to_session(step,activity_number,session_number):
    i = Intervention.objects.all()[0]
    s = i.clientsession_set.all()[int(session_number) - 1]
    assert s.index() == int(session_number)
    a = s.activity_set.all()[int(activity_number) - 1]
    assert a.index() == int(activity_number)

    if world.using_selenium:
        world.firefox.get(django_url("/activity/%d/" % a.id))
    else:
        response = world.client.get(django_url("/activity/%d/" % a.id))
        world.dom = html.fromstring(response.content)
        world.response = response



@step(u'I go to Session (\d+)')
def i_go_to_session(step,session_number):
    i = Intervention.objects.all()[0]
    s = i.clientsession_set.all()[int(session_number) - 1]
    assert s.index() == int(session_number)
    response = world.client.get(django_url("/session/%d/" % s.id))
    world.dom = html.fromstring(response.content)
    world.response = response

@step(u'there is no "([^"]*)" button')
def there_is_no_button(step, label):
    found = False
    n = len(world.dom.cssselect('a.action'))
    for a in world.dom.cssselect('a.action'):
        if a.text.strip().lower() == label.strip().lower():
            found = True
    assert not found

@step(u'the participant has completed (\d+) activit[y|ies] in session (\d+)')
def the_participant_has_completed_activity_in_session_1(step,num_activities,session_number):
    world.participant.participantsession_set.all().delete()
    world.participant.participantactivity_set.all().delete()
    i = Intervention.objects.all()[0]
    s = i.clientsession_set.all()[int(session_number) - 1]
    for a in s.activity_set.all()[:int(num_activities)]:
        r = world.client.post(django_url("/activity/%d/complete/" % a.id),{})
    

@step(u'the participant has completed all activities in session (\d+)')
def the_participant_has_completed_all_activities(step,session_number):
    i = Intervention.objects.all()[0]
    s = i.clientsession_set.all()[int(session_number) - 1]
    for a in s.activity_set.all():
        r = world.client.post(django_url("/activity/%d/complete/" % a.id),{})

@step(u'the participant has completed all activities except the first in session (\d+)')
def the_participant_has_completed_all_activities_except_the_first(step,session_number):
    i = Intervention.objects.all()[0]
    s = i.clientsession_set.all()[int(session_number) - 1]
    for a in list(s.activity_set.all())[1:]:
        r = world.client.post(django_url("/activity/%d/complete/" % a.id),{})

@step(u'there is a "([^"]*)" button')
def then_there_is_button(step, label):
    found = False
    n = len(world.dom.cssselect('a.action'))
    for a in world.dom.cssselect('a.action'):
        if a.text.strip().lower() == label.strip().lower():
            found = True
    assert found

@step(u'there is a "([^"]*)" nav button')
def then_there_is_navbutton(step, label):
    found = False
    n = len(world.dom.cssselect('a.navlink'))
    for a in world.dom.cssselect('a.navlink'):
        if a.text.strip().lower() == label.strip().lower():
            found = True
    assert found

@step(u'there is no "([^"]*)" nav button')
def there_is_no_navbutton(step, label):
    found = False
    n = len(world.dom.cssselect('a.navlink'))
    for a in world.dom.cssselect('a.navlink'):
        if a.text.strip().lower() == label.strip().lower():
            found = True
    assert not found, "expecting no nav button, but we found one"

@step(u'I wait for (\d+) seconds')
def wait(step,seconds):
    time.sleep(int(seconds))
        

@step(u'I am not on an activity page')
def i_am_not_on_an_activity_page(step):
    # look for an h3.activitytitle
    if len(world.dom.cssselect("h3.activitytitle")) > 0:
        # if there is one, we're either on an activity or a game
        # let's make sure it's a game page
        assert len(world.dom.cssselect("#gamebox")) > 0, "on an activity page"
    else:
        assert True

@step(u'I am on a game page')
def i_am_on_a_game_page(step):
    assert len(world.dom.cssselect("#gamebox")) > 0, "not a game page"

@step(u'Participant "([^"]*)" is a defaulter')
def participant_is_a_defaulter(step,participant_name):
    p = Participant.objects.get(name=participant_name)
    p.defaulter = True
    p.save()
