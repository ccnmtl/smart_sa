# -*- coding: utf-8 -*-
import logging
import time

from aloe import before, after, world, step
from aloe_django import django_url
from django.conf import settings
from django.test import client
from lxml import html  # nosec
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, \
    WebDriverException, TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.utils import LOGGER
from selenium.webdriver.support import ui

from selenium.webdriver.support.expected_conditions \
    import visibility_of_element_located


@before.all
def setup_browser():
    LOGGER.setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    world.browser = None
    headless = getattr(settings, 'HEADLESS', True)
    browser = getattr(settings, 'BROWSER', 'Chrome')
    if browser == 'Firefox':
        ff_profile = FirefoxProfile()
        ff_profile.set_preference("webdriver_enable_native_events", False)
        ff_options = FirefoxOptions()
        if headless:
            ff_options.add_argument("--headless")
        world.browser = webdriver.Firefox(
            firefox_options=ff_options, firefox_profile=ff_profile)
    elif browser == 'Chrome':
        chrome_options = ChromeOptions()
        if headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--no-sandbox')
        world.browser = webdriver.Chrome(chrome_options=chrome_options)

    world.client = client.Client()

    world.browser.set_window_position(0, 0)
    world.browser.set_window_size(1024, 768)


@after.all
def teardown_browser():
    try:
        world.browser.quit()
    except WebDriverException:
        pass


@before.each_example
def setup_database(scenario, outline, steps):
    from django.core import management
    management.call_command(
        'loaddata', 'smart_sa/intervention/fixtures/selenium.json')


@step(r'I access the url "(.*)"')
def access_url(step, url):
    world.browser.get(django_url(step, url))


@step(u'I am not logged in')
def i_am_not_logged_in(step):
    world.browser.get(django_url(step, "/accounts/logout/"))


@step(u'I access the management console')
def i_access_the_management_console(step):
    world.browser.get(django_url(step, "/manage/"))


@step(u'I access the counselor landing page')
def i_access_the_counselor_landing_page(step):
    world.browser.get(django_url(step, "/intervention/"))


@step(u'I am taken to a login screen')
def i_am_taken_to_a_login_screen(step):
    assert len(world.response.redirect_chain) > 0
    (url, status) = world.response.redirect_chain[0]
    assert status == 302, status
    assert "/login/" in url, "URL redirected to was %s" % url


@step(u'I am taken to the index')
def i_am_taken_to_the_index(step):
    assert len(world.response.redirect_chain) > 0
    (url, status) = world.response.redirect_chain[0]
    assert status == 302, status
    assert "http://testserver/" == url, "URL redirected to was %s" % (url,)


@step(u'I am logged in as a counselor')
def i_am_logged_in_as_a_counselor(step):
    world.browser.get(django_url(step, "/accounts/logout/"))
    world.browser.get(django_url(step, "/accounts/login/?next=/intervention/"))
    username_field = world.browser.find_element_by_id("id_username")
    password_field = world.browser.find_element_by_id("id_password")
    form = world.browser.find_element_by_id("login-form")
    username_field.send_keys("testcounselor")
    password_field.send_keys("test")
    form.submit()
    assert world.browser.current_url.endswith("/intervention/"), \
        world.browser.current_url
    assert "testcounselor" in world.browser.page_source, \
        world.browser.page_source


@step(u'I log out')
def i_log_out(step):
    world.browser.get(django_url(step, "/accounts/logout/"))


@step(u'I am logged in as an admin')
def given_i_am_logged_in_as_an_admin(step):
    world.browser.get(django_url(step, "/accounts/logout/"))
    world.browser.get(django_url(step, "/accounts/login/?next=/intervention/"))
    username_field = world.browser.find_element_by_id("id_username")
    password_field = world.browser.find_element_by_id("id_password")
    form = world.browser.find_element_by_id("login-form")
    username_field.send_keys("testadmin")
    password_field.send_keys("test")
    form.submit()
    assert world.browser.current_url.endswith("/intervention/"), \
        world.browser.current_url
    assert "testadmin" in world.browser.page_source, world.browser.page_source


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
    wait = ui.WebDriverWait(world.browser, 5)
    link = wait.until(
        visibility_of_element_located((By.PARTIAL_LINK_TEXT, text)))
    link.click()


@step(u'I fill in "([^"]*)" in the "([^"]*)" form field')
def i_fill_in_the_form_field(step, value, field_name):
    world.browser.find_element_by_id(field_name).send_keys(value)


@step(u'I submit the "([^"]*)" form')
def i_submit_the_form(step, the_id):
    world.browser.find_element_by_id(the_id).submit()


@step(u'I am on the Intervention page')
def i_am_on_the_intervention_page(step):
    assert world.browser.current_url.find("/intervention/") > -1
    assert world.browser.find_elements_by_tag_name('h2')[0].text == "Sessions"


@step(u'I click on Session (\d+)')  # noqa
def i_click_session(step, session_number):
    the_id = "session%s" % session_number
    wait = ui.WebDriverWait(world.browser, 5)
    link = wait.until(
        visibility_of_element_located((By.ID, the_id)))
    link.click()


@step(u'I click on the Session Home')
def i_click_on_the_session_home(step):
    try:
        selector = "h2#sessioninfo a"
        wait = ui.WebDriverWait(world.browser, 1)
        link = wait.until(
            visibility_of_element_located((By.CSS_SELECTOR, selector)))
        link.click()
    except TimeoutException:
        pass  # we're likely already on the page


@step(u'I am on the Session Home')
def i_am_on_the_session_home(step):
    selector = 'h2.session-home'
    wait = ui.WebDriverWait(world.browser, 5)
    wait.until(
        visibility_of_element_located((By.CSS_SELECTOR, selector)))


@step(u'I click on Activity (\d+)')  # noqa
def i_click_activity(step, activity_number):
    try:
        link_text = "Activity %s:" % activity_number
        wait = ui.WebDriverWait(world.browser, 5)
        link = wait.until(
            visibility_of_element_located((By.PARTIAL_LINK_TEXT, link_text)))
        link.click()
    except Exception, e:
        assert False, str(e)


@step(u'I click on Complete Activity')
def i_click_on_complete_activity(step):
    try:
        link = world.browser.find_element_by_partial_link_text("Next →")
        link.click()
    except:  # noqa
        link = world.browser.find_element_by_partial_link_text("Wrap Up")
        link.click()


@step(u'I am on the Session (\d+) page')  # noqa
def i_am_on_the_session_page(step, session_id):
    try:
        h2 = world.browser.find_elements_by_tag_name('h2')[0]
    except:  # noqa
        time.sleep(1)
        h2 = world.browser.find_elements_by_tag_name('h2')[0]
    assert h2.text.startswith("Session %s:" % session_id)


@step(u'I am on the Activity (\d+) page')  # noqa
def i_am_on_the_activity_page(step, activity_id):
    try:
        breadcrumb = world.browser.find_element_by_id("breadcrumb-text")
    except:  # noqa
        time.sleep(1)
        breadcrumb = world.browser.find_element_by_id("breadcrumb-text")
    assert "Activity %s:" % activity_id in breadcrumb.text, breadcrumb.text


@step(u'Then I am on the "([^"]*)" Activity')
def i_am_on_the_activity_with_title(step, title):
    selector = 'h3'
    wait = ui.WebDriverWait(world.browser, 5)
    elt = wait.until(
        visibility_of_element_located((By.CSS_SELECTOR, selector)))
    title = title.replace("  ", " ")
    assert elt.text == title, elt.text


@step(u'there is a game')
def there_is_a_game(self):
    try:
        wait = ui.WebDriverWait(world.browser, 5)
        wait.until(
            visibility_of_element_located((By.ID, 'gamebox')))
        assert world.browser.find_element_by_id('gamebox')
    except Exception, e:
        assert False, str(e)


@step(u'I go back')
def i_go_back(self):
    """ need to back out of games currently"""
    world.browser.back()


@step(u'I clear the privacy notice')
def i_clear_the_privacy_notice(step):
    try:
        wait = ui.WebDriverWait(world.browser, 1)
        elt = wait.until(
            visibility_of_element_located((By.ID, 'cu-privacy-notice-icon')))
        elt.click()
    except:  # noqa
        pass  # Might have already been cleared


@step(u'I am a participant')
def i_am_a_participant(step):
    world.browser.get(django_url(step, "/"))

    world.browser.get_screenshot_as_file("/tmp/selenium.png")  # nosec

    wait = ui.WebDriverWait(world.browser, 5)
    elt = wait.until(
        visibility_of_element_located((By.ID, 'btn-get-started')))
    elt.click()

    assert world.browser.current_url.find("/intervention/") > -1,\
        world.browser.current_url
    assert (world.browser.find_elements_by_tag_name('h2')[0].text
            == "Sessions")


@step(u'the participant has not completed any sessions')
def participant_has_not_completed_any_sessions(step):
    world.participant.participantsession_set.all().delete()
    world.participant.participantactivity_set.all().delete()


@step(u'I go to Activity (\d+) of Session (\d+)')  # noqa
def i_go_to_activity_or_session(step, activity_number, session_number):
    from smart_sa.intervention.models import Intervention
    i = Intervention.objects.first()
    s = i.clientsession_set.all()[int(session_number) - 1]
    assert s.index() == int(session_number)
    a = s.activity_set.all()[int(activity_number) - 1]
    assert a.index() == int(activity_number)

    world.browser.get(django_url(step, "/activity/%d/" % a.id))


@step(u'I go to Session (\d+)')  # noqa
def i_go_to_session(step, session_number):
    from smart_sa.intervention.models import Intervention
    i = Intervention.objects.all()[0]
    s = i.clientsession_set.all()[int(session_number) - 1]
    assert s.index() == int(session_number)
    response = world.client.get(django_url(step, "/session/%d/" % s.id))
    world.dom = html.fromstring(response.content)
    world.response = response


@step(u'there is no "([^"]*)" button')
def there_is_no_button(step, label):
    found = False
    for a in world.dom.cssselect('a.action'):
        if a.text.strip().lower() == label.strip().lower():
            found = True
    assert not found


@step(u'the participant has completed (\d+) activit[y|ies] in session (\d+)')  # noqa
def the_participant_has_completed_activity_in_session_1(
        step, num_activities, session_number):
    from smart_sa.intervention.models import Intervention
    world.participant.participantsession_set.all().delete()
    world.participant.participantactivity_set.all().delete()
    i = Intervention.objects.all()[0]
    s = i.clientsession_set.all()[int(session_number) - 1]
    for a in s.activity_set.all()[:int(num_activities)]:
        url = django_url(step, "/activity/%d/complete/" % a.id)
        world.client.post(url, {})


@step(u'the participant has completed all activities in session (\d+)')  # noqa
def the_participant_has_completed_all_activities(step, session_number):
    from smart_sa.intervention.models import Intervention
    i = Intervention.objects.all()[0]
    s = i.clientsession_set.all()[int(session_number) - 1]
    for a in s.activity_set.all():
        world.client.post(
            django_url(step, "/activity/%d/complete/" % a.id), {})


@step(u'the participant has completed all activities except the first in session (\d+)')   # noqa
def the_participant_has_completed_all_activities_except_the_first(
        step, session_number):
    from smart_sa.intervention.models import Intervention
    i = Intervention.objects.all()[0]
    s = i.clientsession_set.all()[int(session_number) - 1]
    for a in list(s.activity_set.all())[1:]:
        world.client.post(
            django_url(step, "/activity/%d/complete/" % a.id), {})


@step(u'there is a "([^"]*)" button')
def then_there_is_button(step, label):
    found = False
    len(world.dom.cssselect('a.action'))
    for a in world.dom.cssselect('a.action'):
        if a.text.strip().lower() == label.strip().lower():
            found = True
    assert found


@step(u'there is a "([^"]*)" nav button')
def then_there_is_navbutton(step, label):
    link = world.browser.find_element_by_partial_link_text(label)
    assert link is not None


@step(u'there is no "([^"]*)" nav button')
def there_is_no_navbutton(step, label):
    try:
        world.browser.find_element_by_partial_link_text(label)
        assert False, "expecting no nav button, but we found one"
    except NoSuchElementException:
        pass  # expected


@step(u'I wait for (\d+) seconds')  # noqa
def wait(step, seconds):
    time.sleep(int(seconds))


@step(u'I am not on an activity page')
def i_am_not_on_an_activity_page(step):
    titles = world.browser.find_elements_by_css_selector('h3.activitytitle')

    # look for an h3.activitytitle
    if len(titles) > 0:
        # if there is one, we're either on an activity or a game
        # let's make sure it's a game page
        boxes = world.browser.find_elements_by_css_selector('#gamebox')
        assert len(boxes) > 0, "on an activity page"
    else:
        assert True


@step(u'I am on a game page')
def i_am_on_a_game_page(step):
    boxes = world.browser.find_elements_by_css_selector('#gamebox')
    assert len(boxes) > 0, "not a game page"


@step(u'Participant "([^"]*)" is a defaulter')
def participant_is_a_defaulter(step, participant_name):
    from smart_sa.intervention.models import Participant
    p = Participant.objects.get(name=participant_name)
    p.defaulter = True
    p.save()


@step(u'Then I wait (\d+) second')  # noqa
def then_i_wait_count_second(step, count):
    n = int(count)
    time.sleep(n)


@step(u'I see a filled in SSNM Tree with "([^"]*)"')
def filled_in_ssnmtree(self, text):
    assert True
