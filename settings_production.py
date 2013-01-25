from settings_shared import *
TEMPLATE_DIRS = (
    "/var/www/masivukeni2/smart_sa/templates",
)

MEDIA_ROOT = '/var/www/masivukeni2/uploads/'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

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

import logging
from sentry.client.handlers import SentryHandler
logger = logging.getLogger()
if SentryHandler not in map(lambda x: x.__class__, logger.handlers):
    logger.addHandler(SentryHandler())
    logger = logging.getLogger('sentry.errors')
    logger.propagate = False
    logger.addHandler(logging.StreamHandler())
SENTRY_REMOTE_URL = 'http://sentry.ccnmtl.columbia.edu/sentry/store/'
SENTRY_SITE = 'masivukeni2' # can't rely on the sites framework when a transaction is aborted

try:
    from local_settings import *
except ImportError:
    pass
