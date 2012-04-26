from settings_shared import *
TEMPLATE_DIRS = (
    "C:/smart_sa/templates/",
)

MEDIA_ROOT = 'C:/smart_sa/uploads/'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INTERVENTION_BACKUP_HEXKEY = "d37fb81dff7672c76f4881a8f57c002403ba2ce5155dc4ac6b68a2d9caa51d88"
INTERVENTION_BACKUP_IV = "899f6762313185a9593480e6f015b0d5053464daa5ecadd00dc4e7e2984f028f"

DISABLE_OFFLINE=True

DATABASES = {
    'default' : {
        'ENGINE' : 'django.db.backends.postgresql_psycopg2',
        'NAME' : 'masivukeni',
        'HOST' : '',
        'PORT' : '5432',
        'USER' : 'postgres',
        'PASSWORD' : 'masivukeni',
        }
}


try:
    from local_settings import *
except ImportError:
    pass
