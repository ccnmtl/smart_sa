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

    
