from lettuce.django import django_url
from lettuce import before, after, world, step
from django.test import client
from lxml import html

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

@before.all
def setup_browser():
    world.firefox = webdriver.Firefox()
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

