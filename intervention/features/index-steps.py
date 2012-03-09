from lettuce import *
from lxml import html
from django.test.client import Client
from nose.tools import assert_equals
from lettuce.django import django_url


@step(r'I see the header "(.*)"')
def see_header(step, text):
    if world.using_selenium:
        assert text.strip() == world.firefox.find_element_by_tag_name("h2").text.strip()
    else:
        header = world.dom.cssselect('h2')[0]
        assert text.strip() == header.text.strip()

@step(r'I see the page title "(.*)"')
def see_title(step, text):
    if world.using_selenium:
        assert text == world.firefox.title
    else:
        assert text == world.dom.find(".//title").text

@step(r'the deployment is displayed as "(.*)"')
def check_deployment(step, name):
    deployment = world.dom.cssselect("#deployment")[0].text
    assert name == deployment, "Got %s" % deployment

@step(u'Then I see a counselor login form')
def then_i_see_a_counselor_login_form(step):
    formtitle = world.dom.cssselect("form.login .formtitle")[0].text
    assert formtitle == "Log In to Masivukeni", "Got %s" % formtitle

@step(u'Then I do not see a WIND login form')
def then_i_do_not_see_a_wind_login_form(step):
    forms = world.dom.cssselect("form.cu")
    assert len(forms) == 0

@step(u'Then I am not logged in')
def then_i_am_not_logged_in(step):
    username = world.dom.cssselect("#username")[0].text.strip()
    assert username == "", "Got '%s'" % str(username)

@step(u'Then there is a login link')
def then_there_is_a_login_link(step):
    # <a class="loginlogout loginlogout-remote" href="/intervention/">Log In</a>
    link = world.dom.cssselect("a.loginlogout")[0]
    assert link.text == "Log In", "Got '%s'" % link.text


