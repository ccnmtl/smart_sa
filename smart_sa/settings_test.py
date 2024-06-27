# flake8: noqa
from smart_sa.settings_shared import *
import os


DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

HEADLESS = True
# BROWSER = 'Firefox'
BROWSER = 'Chrome'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'HOST': '',
        'PORT': '',
        'USER': '',
        'PASSWORD': '',
        'ATOMIC_REQUESTS': False
    }
}



PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

MIDDLEWARE.remove(
    'django_statsd.middleware.GraphiteRequestTimingMiddleware')
MIDDLEWARE.remove(
    'django_statsd.middleware.GraphiteMiddleware')
MIDDLEWARE.remove(
    'impersonate.middleware.ImpersonateMiddleware')

SESSION_COOKIE_SECURE = False

ALLOWED_HOSTS.append('127.0.0.1')


if os.environ.get('SELENIUM_BROWSER', False):
    # it's handy to be able to set this from an
    # environment variable
    BROWSER = os.environ.get('SELENIUM_BROWSER')
