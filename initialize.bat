set HOME=C:\smart_sa\
cd C:\smart_sa\
"C:\Program Files\Bitnami DjangoStack\postgres\bin\createdb.exe" -U postgres masivukeni
"C:\Program Files\Bitnami DjangoStack\Python\python.exe" manage.py syncdb --settings=settings_windows
"C:\Program Files\Bitnami DjangoStack\Python\python.exe" manage.py migrate intervention --settings=settings_windows
"C:\Program Files\Bitnami DjangoStack\Python\python.exe" manage.py migrate --settings=settings_windows
"C:\Program Files\Bitnami DjangoStack\Python\python.exe" manage.py migrate --settings=settings_windows
"C:\Program Files\Bitnami DjangoStack\Python\python.exe" manage.py pull_from_prod --settings=settings_windows
"C:\Program Files\Bitnami DjangoStack\Python\python.exe" manage.py runserver --settings=settings_windows
cp apache\bitnami.conf "C:\Program Files\Bitnami DjangoStack\apps\django\conf\django.conf"
