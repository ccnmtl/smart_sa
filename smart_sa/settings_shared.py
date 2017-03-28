# Django settings for smart_sa clone - masivukeni2
import os.path
import sys
from ccnmtlsettings.shared import common

project = 'smart_sa'
base = os.path.dirname(__file__)
locals().update(common(project=project, base=base))

if 'test' not in sys.argv and 'jenkins' not in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'masivukeni2',
            'HOST': '',
            'PORT': 5432,
            'USER': '',
            'PASSWORD': '',
            'ATOMIC_REQUESTS': True,
        }
    }

MEDIA_URL = '/multimedia/'

# generate these most easily by going to:
# http://www.josh-davis.org/ecmaScrypt
#  setting the Key Size to 256 and Mode of Op to OFB
# for public consumption on public site
FAKE_INTERVENTION_BACKUP_HEXKEY = (
    "f8bb022b420b66ab585065366073eed24705932289279be63ee20896c335a1aa")
FAKE_INTERVENTION_BACKUP_IV = (
    "209b8b7cea877f069df46a0994af20c36d86bbcd33cb4b79bde43dee55fc9c85")

# for actual consumption for people logged in, and on the desktop app
INTERVENTION_BACKUP_HEXKEY = (
    "f8bb022b420b66ab585065366073eed24705932289279be63ee20896c335a1aa")
INTERVENTION_BACKUP_IV = (
    "209b8b7cea877f069df46a0994af20c36d86bbcd33cb4b79bde43dee55fc9c85")

INSTALLED_APPS += [  # noqa
    'smart_sa.assessmentquiz_task',
    'smart_sa.lifegoal_task',
    'smart_sa.pill_game',
    'smart_sa.island_game',
    'smart_sa.ssnmtree_game',
    'smart_sa.watchvideo_game',
    'smart_sa.problemsolving_game',
    'smart_sa.intervention',
]

STATSD_PREFIX = 'masivukeni'

PROJECT_APPS = [
    'smart_sa.assessmentquiz_task',
    'smart_sa.lifegoal_task',
    'smart_sa.pill_game',
    'smart_sa.island_game',
    'smart_sa.ssnmtree_game',
    'smart_sa.watchvideo_game',
    'smart_sa.problemsolving_game',
    'smart_sa.intervention',
]

EMAIL_SUBJECT_PREFIX = "[masivukeni2] "
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

TEMPLATES[0]['OPTIONS']['context_processors'].append(  # noqa
    "smart_sa.intervention.views.inject_deployment",
)

PROD_BASE_URL = "https://masivukeni2.ccnmtl.columbia.edu/"
PROD_MEDIA_BASE_URL = "https://masivukeni2.ccnmtl.columbia.edu/multimedia/"

DISABLE_OFFLINE = False

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
