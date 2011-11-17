from django.core.management.base import BaseCommand
from intervention.models import *
from django.conf import settings

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        if not settings.DEBUG:
            print "this should never be run on production"
            return
        print "pulling from prod"
        # get zip file from production
        # check integrity
        # wipe existing content from database
        # recursively import db content
        # copy file uploads into MEDIA_ROOT
