# flake8: noqa
from settings_shared import *
import os


DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'lettuce.db',
        'OPTIONS': {
            'timeout': 30,
        }
    }
}


BROWSER = 'Headless'
# BROWSER = 'Firefox'
# BROWSER = 'Chrome'

LETTUCE_APPS = (
    'smart_sa.intervention',
    'smart_sa.assessmentquiz_task',
    'smart_sa.ssnmtree_task',
    'smart_sa.problemsolving_game',
    'smart_sa.pill_game',
    'smart_sa.ssnmtree_game',
)

LETTUCE_DJANGO_APP = ['lettuce.django']
INSTALLED_APPS = INSTALLED_APPS + LETTUCE_DJANGO_APP

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

MIDDLEWARE_CLASSES.remove(
    'django_statsd.middleware.GraphiteRequestTimingMiddleware')
MIDDLEWARE_CLASSES.remove(
    'django_statsd.middleware.GraphiteMiddleware')
MIDDLEWARE_CLASSES.remove(
    'impersonate.middleware.ImpersonateMiddleware')

ALLOWED_HOSTS.append('127.0.0.1')


# Running tests
# python manage.py --settings=settings_test harvest

if os.environ.get('SELENIUM_BROWSER', False):
    # it's handy to be able to set this from an
    # environment variable
    BROWSER = os.environ.get('SELENIUM_BROWSER')
