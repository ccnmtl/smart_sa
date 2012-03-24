from settings import *

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'test_masivukeni2.db' 

# Running tests
# 
# The database needs to exist & be current Prior to first run
# sqlite3 test_masivukeni2.db
# ./manage.py syncdb --settings=settings_test
# ./manage.py migrate intervention --settings=settings_test
# ./manage.py migrate --settings=settings_test
# ./manage.py pull_from_prod --settings=settings_test
# ./manage.py loaddata intervention/fixtures/counselors.json --settings=settings_test
# ./manage.py loaddata intervention/fixtures/default_participants.json --settings=settings_test
# 
# Subsequent runs
# python manage.py --settings=settings_test harvest 
