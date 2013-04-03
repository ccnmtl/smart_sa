import os, sys, site

# paths we might need to pick up the project's settings
sys.path.append('/var/www/masivukeni/smart_sa/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'smart_sa.settings_production'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
