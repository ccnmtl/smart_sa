from django.core.management.base import BaseCommand
from intervention.models import *
from django.conf import settings
from restclient import GET
from zipfile import ZipFile
from cStringIO import StringIO
from simplejson import dumps,loads
import os
import os.path


class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        if not settings.DEBUG:
            print "this should never be run on production"
            return

        zc = GET(settings.PROD_BASE_URL + "intervention_admin/content_sync/")
        uploads = GET(settings.PROD_BASE_URL + "intervention_admin/list_uploads/").split("\n")

        buffer = StringIO(zc)
        zipfile = ZipFile(buffer,"r")
        json = loads(zipfile.read("interventions.json"))

        # wipe existing content from database
        Intervention.objects.all().delete()

        # recursively import db content
        for i in json['interventions']:
            intervention = Intervention.objects.create(name="tmp")
            intervention.from_dict(i)


        # copy file uploads into MEDIA_ROOT
