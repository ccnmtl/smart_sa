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

        print "fetching content from prod..."
        zc = GET(settings.PROD_BASE_URL + "intervention_admin/content_sync/")
        uploads = GET(settings.PROD_BASE_URL + "intervention_admin/list_uploads/").split("\n")

        buffer = StringIO(zc)
        zipfile = ZipFile(buffer,"r")
        json = loads(zipfile.read("interventions.json"))

        print "clearing database content..."
        Intervention.objects.all().delete()

        print "importing prod database content..."
        for i in json['interventions']:
            intervention = Intervention.objects.create(name="tmp")
            intervention.from_dict(i)

        print "updating uploaded files..."
        base_len = len(settings.PROD_MEDIA_BASE_URL)
        for upload in uploads:
            relative_path = upload[base_len:]
            relative_dir = os.path.join(*os.path.split(relative_path)[:-1])
            full_dir = os.path.join(settings.MEDIA_ROOT,relative_dir)
            try:
                os.makedirs(full_dir)
            except OSError:
                pass
            with open(os.path.join(settings.MEDIA_ROOT,relative_path),"w") as f:
                print "   writing %s to %s" % (upload,relative_path)
                f.write(GET(upload))
            
