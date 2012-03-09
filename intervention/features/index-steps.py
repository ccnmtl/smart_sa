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
