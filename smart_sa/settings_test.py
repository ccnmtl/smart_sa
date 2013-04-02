# flake8: noqa
from settings_shared import *
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'lettuce.db',
        'OPTIONS': {
            'timeout': 30,
        }
    }
}

# Running tests
#
# The database needs to exist & be current Prior to first run
# sqlite3 test_masivukeni2.db
# ./manage.py syncdb --settings=smart_sa.settings_test
# ./manage.py migrate intervention --settings=smart_sa.settings_test
# ./manage.py migrate --settings=smart_sa.settings_test
# ./manage.py pull_from_prod --settings=smart_sa.settings_test
# ./manage.py loaddata smart_sa/intervention/fixtures/counselors.json --settings=smart_sa.settings_test
# ./manage.py loaddata smart_sa/intervention/fixtures/default_participants.json --settings=smart_sa.settings_test
#
# Subsequent runs
# python manage.py --settings=settings_test harvest

if os.environ.get('SELENIUM_BROWSER', False):
    # it's handy to be able to set this from an
    # environment variable
    BROWSER = os.environ.get('SELENIUM_BROWSER')
