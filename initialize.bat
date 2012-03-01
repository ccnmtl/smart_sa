set HOME=C:\Users\CCNMTLSTAFF\Downloads\smart_sa\
cd C:\Users\CCNMTLSTAFF\Downloads\smart_sa\
C:\Python27\python.exe manage.py syncdb --settings=settings_windows
C:\Python27\python.exe manage.py migrate --settings=settings_windows
C:\Python27\python.exe manage.py pull_from_prod --settings=settings_windows
C:\Python27\python.exe manage.py runserver --settings=settings_windows

