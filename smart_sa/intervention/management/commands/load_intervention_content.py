from django.core.management.base import BaseCommand
from smart_sa.intervention.models import Intervention
from smart_sa.problemsolving_game.models import Issue
from django.conf import settings
from zipfile import ZipFile
from simplejson import loads
import os
import os.path
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

        zipfile = ZipFile(os.path.join("data", "intervention.zip"), "r")

        # Load Intervention objects
        json = loads(zipfile.read("interventions.json"))

        print "clearing intervention prod database content..."
        Intervention.objects.all().delete()

        print "importing prod database content..."
        for i in json['interventions']:
            intervention = Intervention.objects.create(name="tmp")
            intervention.from_dict(i)

        # Load Problem Solving objects
        json = loads(zipfile.read("issues.json"))

        print "clearing problemsolving database content..."
        Issue.objects.all().delete()

        print "importing problemsolving prod database content..."
        for i in json['issues']:
            issue = Issue.objects.create(name="tmp", ordinality=0)
            issue.from_dict(i)
