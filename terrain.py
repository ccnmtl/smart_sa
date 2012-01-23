from lettuce import *
from lettuce.django import django_url
from selenium import selenium
 
#@before.harvest
#def prepare_browser_driver(variables):
#    if variables.get('run_server', False) is True:
#        world.browser = selenium('localhost', 8000, '*firefox', django_url('/'))
#        world.browser.start()

#@after.harvest
#def shutdown_browser_driver(results):
#    world.browser.stop()
