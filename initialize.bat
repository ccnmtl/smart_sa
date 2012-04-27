set HOME=C:\smart_sa\
cd C:\smart_sa\
"C:\Program Files\Bitnami DjangoStack\postgresql\bin\dropdb.exe" -U postgres masivukeni
"C:\Program Files\Bitnami DjangoStack\postgresql\bin\createdb.exe" -U postgres masivukeni
"C:\Program Files\Bitnami DjangoStack\Python\python.exe" manage.py syncdb --noinput --settings=settings_windows
"C:\Program Files\Bitnami DjangoStack\Python\python.exe" manage.py migrate intervention --settings=settings_windows
"C:\Program Files\Bitnami DjangoStack\Python\python.exe" manage.py migrate --settings=settings_windows
"C:\Program Files\Bitnami DjangoStack\Python\python.exe" manage.py migrate --settings=settings_windows
"C:\Program Files\Bitnami DjangoStack\Python\python.exe" manage.py load_intervention_content --settings=settings_windows
"C:\Program Files\Bitnami DjangoStack\Python\python.exe" manage.py loaddata --settings=settings_windows intervention/fixtures/admins.json
