from lettuce.django import django_url
from lettuce import before, after, world, step

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

@before.all
def setup_browser():
    world.browser = webdriver.Firefox()

@after.all
def teardown_browser(total):
    world.browser.quit()
 
@step(r'I access the url "(.*)"')
def access_url(step, url):
    world.browser.get(django_url(url))
