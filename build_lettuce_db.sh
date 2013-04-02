#!/bin/bash
rm -f lettuce.db
./manage.py syncdb --noinput --settings=smart_sa.settings_test
./manage.py migrate intervention --settings=smart_sa.settings_test
./manage.py migrate --settings=smart_sa.settings_test
./manage.py migrate --settings=smart_sa.settings_test
./manage.py pull_from_prod --settings=smart_sa.settings_test
./manage.py loaddata smart_sa/intervention/fixtures/counselors.json --settings=smart_sa.settings_test
./manage.py loaddata smart_sa/intervention/fixtures/default_participants.json --settings=smart_sa.settings_test
mv lettuce.db test_data/test.db
