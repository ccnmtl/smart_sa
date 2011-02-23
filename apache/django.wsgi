import os, sys, site

# enable the virtualenv
site.addsitedir('/var/www/smart_sa/smart_sa/ve/lib/python2.6/site-packages')

# paths we might need to pick up the project's settings
sys.path.append('/var/www/')
sys.path.append('/var/www/smart_sa/')
sys.path.append('/var/www/smart_sa/smart_sa/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'smart_sa.settings_production'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
