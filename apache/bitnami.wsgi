import os, sys, site
sys.path.append('C:/')
sys.path.append('C:/smart_sa/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'smart_sa.settings_windows'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
