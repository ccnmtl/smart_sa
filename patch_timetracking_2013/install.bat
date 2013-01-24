set HOME=C:\smart_sa\
cd C:\smart_sa\
copy C:\patch_timetracking_2013\models.py C:\smart_sa\intervention\models.py
copy C:\patch_timetracking_2013\views.py C:\smart_sa\intervention\views.py
copy C:\patch_timetracking_2013\urls.py C:\smart_sa\urls.py
copy C:\patch_timetracking_2013\0018_auto__add_sessionvisit__add_activityvisit.py C:\smart_sa\intervention\migrations\0018_auto__add_sessionvisit__add_activityvisit.py
copy C:\patch_timetracking_2013\activity.html C:\smart_sa\templates\intervention\activity.html
copy C:\patch_timetracking_2013\session.html C:\smart_sa\templates\intervention\session.html
copy C:\patch_timetracking_2013\game.html C:\smart_sa\templates\intervention\game.html
"C:\Program Files\Bitnami DjangoStack\Python\python.exe" manage.py migrate intervention --settings=settings_windows
