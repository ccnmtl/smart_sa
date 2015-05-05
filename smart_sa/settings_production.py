# flake8: noqa
from settings_shared import *
import os
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)

MEDIA_ROOT = '/var/www/masivukeni/uploads/'

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

STATICFILES_DIRS = ()
STATIC_ROOT = os.path.join(os.path.dirname(__file__), "../media")

AWS_S3_CUSTOM_DOMAIN = "d6wadfi3s9mi3.cloudfront.net"

AWS_STORAGE_BUCKET_NAME = "ccnmtl-masivukeni-static-prod"
AWS_PRELOAD_METADATA = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'cacheds3storage.CompressorS3BotoStorage'
S3_URL = 'https://%s/' % AWS_S3_CUSTOM_DOMAIN
STATIC_URL = 'https://%s/media/' % AWS_S3_CUSTOM_DOMAIN
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_URL = STATIC_URL
DEFAULT_FILE_STORAGE = 'cacheds3storage.MediaRootS3BotoStorage'
MEDIA_URL = S3_URL + '/media/'
COMPRESS_STORAGE = 'cacheds3storage.CompressorS3BotoStorage'
AWS_QUERYSTRING_AUTH = False


INTERVENTION_BACKUP_HEXKEY = "d37fb81dff7672c76f4881a8f57c002403ba2ce5155dc4ac6b68a2d9caa51d88"
INTERVENTION_BACKUP_IV = "899f6762313185a9593480e6f015b0d5053464daa5ecadd00dc4e7e2984f028f"

if 'migrate' not in sys.argv:
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')

try:
    from local_settings import *
except ImportError:
    pass
