from django.conf import settings
from smart_sa.settings_shared import *  # noqa: F403
from ctlsettings.production import common, init_sentry

locals().update(
    common(
        project=project,  # noqa: F405
        base=base,  # noqa: F405
        INSTALLED_APPS=INSTALLED_APPS,  # noqa: F405
        STATIC_ROOT=STATIC_ROOT,  # noqa: F405
        cloudfront="d6wadfi3s9mi3",
        s3prefix='ccnmtl',
    ))

MEDIA_ROOT = '/var/www/masivukeni/uploads/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'masivukeni2',
        'HOST': '',
        'PORT': 6432,
        'USER': '',
        'PASSWORD': '',
        }
}

AWS_STORAGE_BUCKET_NAME = "ccnmtl-masivukeni-static-prod"

INTERVENTION_BACKUP_HEXKEY = "d37fb81dff7672c76f4881a8f57c002403ba2ce5155dc4ac6b68a2d9caa51d88"  # noqa: E501
INTERVENTION_BACKUP_IV = "899f6762313185a9593480e6f015b0d5053464daa5ecadd00dc4e7e2984f028f"  # noqa: E501

try:
    from smart_sa.local_settings import *  # noqa: F403
except ImportError:
    pass

if hasattr(settings, 'SENTRY_DSN'):
    init_sentry(SENTRY_DSN)  # noqa F405
