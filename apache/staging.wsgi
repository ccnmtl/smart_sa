import os, sys, site

sys.path.append('/var/www/masivukeni/smart_sa/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'smart_sa.settings_staging'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
