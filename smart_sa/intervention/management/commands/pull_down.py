""" just pull the data down and save it into a data directory
this is prep for making the windows install USB key """

from django.core.management.base import BaseCommand
from django.conf import settings
import os
import os.path
import requests
from optparse import make_option


class Command(BaseCommand):
    args = ''
    help = ''

    option_list = BaseCommand.option_list + (
        make_option('-d', '--db-only', dest='dbonly',
                    default=False, help='only pull the database content'),
    )

    def handle(self, *args, **options):
        if not settings.DEBUG:
            print "this should never be run on production"
            return

        print "fetching content from prod..."
        r = requests.get(
            settings.PROD_BASE_URL + "intervention_admin/content_sync/")
        zc = r.text
        if not options["dbonly"]:
            r = requests.get(
                settings.PROD_BASE_URL + "intervention_admin/list_uploads/")
            uploads = r.text.split("\n")

        with open("data/intervention.zip", "w") as zipfile:
            zipfile.write(zc)

        if options["dbonly"]:
            return

        print "updating uploaded files..."
        base_len = len(settings.PROD_MEDIA_BASE_URL)
        for upload in uploads:
            relative_path = upload[base_len:]
            relative_dir = os.path.join(*os.path.split(relative_path)[:-1])
            full_dir = os.path.join(settings.MEDIA_ROOT, relative_dir)
            try:
                os.makedirs(full_dir)
            except OSError:
                pass
            r = requests.get(upload)
            with open(os.path.join(settings.MEDIA_ROOT, relative_path),
                      "w") as f:
                print "   writing %s to %s" % (upload, relative_path)
                f.write(r.text)
