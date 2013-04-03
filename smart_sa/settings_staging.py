# flake8: noqa
from settings_shared import *
TEMPLATE_DIRS = (
    "/var/www/masivukeni/smart_sa/smart_sa/templates",
)

MEDIA_ROOT = '/var/www/masivukeni/uploads/'

DEBUG = False
TEMPLATE_DEBUG = DEBUG
STAGING_ENV = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'masivukeni2',
        'HOST': '',
        'PORT': 6432,
        'USER': '',
        'PASSWORD': '',
        }
}


INTERVENTION_BACKUP_HEXKEY = "d37fb81dff7672c76f4881a8f57c002403ba2ce5155dc4ac6b68a2d9caa51d88"
INTERVENTION_BACKUP_IV = "899f6762313185a9593480e6f015b0d5053464daa5ecadd00dc4e7e2984f028f"

SENTRY_SITE = 'masivukeni-staging'
STATSD_PREFIX = 'masivukeni-staging'
SENTRY_SERVERS = ['http://sentry.ccnmtl.columbia.edu/sentry/store/']

if 'migrate' not in sys.argv:
    import logging
    from raven.contrib.django.handlers import SentryHandler
    logger = logging.getLogger()
    # ensure we havent already registered the handler
    if SentryHandler not in map(type, logger.handlers):
        logger.addHandler(SentryHandler())
        logger = logging.getLogger('sentry.errors')
        logger.propagate = False
        logger.addHandler(logging.StreamHandler())

try:
    from local_settings import *
except ImportError:
    pass
