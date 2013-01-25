# Django settings for smart_sa clone - masivukeni2 
import os.path
import sys

DEBUG = True
INTERNAL_IPS = ('128.59.153.16',)
TEMPLATE_DEBUG = DEBUG

ADMINS = tuple()

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'masivukeni2',
        'HOST': '',
        'PORT': 5432,
        'USER': '',
        'PASSWORD': '',
        }
}

if 'test' in sys.argv:
    DATABASES = {
        'default' : {
            'ENGINE' : 'django.db.backends.sqlite3',
            'NAME' : ':memory:',
            'HOST' : '',
            'PORT' : '',
            'USER' : '',
            'PASSWORD' : '',
            }
    }

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
#MEDIA_ROOT = "/var/www/smart_sa/uploads/"
MEDIA_ROOT = "uploads/"  #local file directory for dev
MEDIA_URL = '/multimedia/'
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = 'dummy-asdfasdfasdf'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
)
APPEND_SLASH = True

#generate these most easily by going to:
#http://www.josh-davis.org/ecmaScrypt
#  setting the Key Size to 256 and Mode of Op to OFB
#for public consumption on public site
FAKE_INTERVENTION_BACKUP_HEXKEY = "f8bb022b420b66ab585065366073eed24705932289279be63ee20896c335a1aa"
FAKE_INTERVENTION_BACKUP_IV = "209b8b7cea877f069df46a0994af20c36d86bbcd33cb4b79bde43dee55fc9c85"

#for actual consumption for people logged in, and on the desktop app
INTERVENTION_BACKUP_HEXKEY = "f8bb022b420b66ab585065366073eed24705932289279be63ee20896c335a1aa"
INTERVENTION_BACKUP_IV = "209b8b7cea877f069df46a0994af20c36d86bbcd33cb4b79bde43dee55fc9c85"

ROOT_URLCONF = 'smart_sa.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # Put application templates before these fallback ones:
    "/var/www/masivukeni2/templates/",
    os.path.join(os.path.dirname(__file__),"templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'django.contrib.admin',
    'raven.contrib.django',
    'smart_sa.assessmentquiz_task',
    'smart_sa.lifegoal_task',
    'smart_sa.pill_game',
    'smart_sa.island_game',
    'smart_sa.ssnmtree_game',
    'smart_sa.watchvideo_game',
    'smart_sa.problemsolving_game',
    'smart_sa.intervention',
    'south',
    'lettuce.django',
    'django_nose',
)


if 'test' in sys.argv:
    DATABASE_ENGINE = 'sqlite3'

SOUTH_TESTS_MIGRATE = False
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=intervention',
]


SOUTH_AUTO_FREEZE_APP = True
THUMBNAIL_SUBDIR = "thumbs"
EMAIL_SUBJECT_PREFIX = "[masivukeni2] "
EMAIL_HOST = 'localhost'
SERVER_EMAIL = "masivukeni2@ccnmtl.columbia.edu"

LETTUCE_APPS = (
    'smart_sa.intervention',
    'smart_sa.intervention.assessmentquiz_task',
    'smart_sa.intervention.ssnmtree_task',
    'smart_sa.problemsolving_game',
    'smart_sa.pill_game',
    'smart_sa.lifegoal_task',
    'smart_sa.ssnmtree_game',
)

# WIND settings

AUTHENTICATION_BACKENDS = ('djangowind.auth.WindAuthBackend','django.contrib.auth.backends.ModelBackend',)
WIND_BASE = "https://wind.columbia.edu/"
WIND_SERVICE = "cnmtl_full_np"
WIND_PROFILE_HANDLERS = []
WIND_AFFIL_HANDLERS = ['djangowind.auth.AffilGroupMapper','djangowind.auth.StaffMapper','djangowind.auth.SuperuserMapper']
WIND_STAFF_MAPPER_GROUPS = ['tlcxml.cunix.local:columbia.edu']
WIND_SUPERUSER_MAPPER_GROUPS = ['anp8','jb2410','zm4','sld2131','mar227']

#TEMPLATES
TEMPLATE_CONTEXT_PROCESSORS = ("django.core.context_processors.auth",
                               "django.core.context_processors.debug",
                               "django.core.context_processors.i18n",
                               "django.core.context_processors.media",
                               #non-default:
                               "django.core.context_processors.request",
                               "smart_sa.intervention.views.inject_deployment",
                               )

PROD_BASE_URL = "http://masivukeni2.ccnmtl.columbia.edu/"
PROD_MEDIA_BASE_URL = "http://masivukeni2.ccnmtl.columbia.edu/multimedia/"

DISABLE_OFFLINE = False

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

try:
    from release_id import LAST_GIT_HEAD
except ImportError:
    LAST_GIT_HEAD = "undefined"
