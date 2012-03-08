from lettuce import *
from lxml import html
from django.test.client import Client
from nose.tools import assert_equals
from lettuce.django import django_url

@step(r'I access the url "(.*)"')
def access_url(step, url):
    world.browser.get(django_url(url))

@step(r'I see the header "(.*)"')
def see_header(step, text):
    assert text.strip() == world.browser.find_element_by_tag_name("h2").text.strip()

