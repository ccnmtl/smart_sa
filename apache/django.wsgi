import os, sys, site

# enable the virtualenv
site.addsitedir('/var/www/masivukeni2/masivukeni2/ve/lib/python2.6/site-packages')

# paths we might need to pick up the project's settings
sys.path.append('/var/www/')
sys.path.append('/var/www/masivukeni2/')
sys.path.append('/var/www/masivukeni2/masivukeni2/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'masivukeni2.settings_production'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
