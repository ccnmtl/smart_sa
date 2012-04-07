from django.core.management.base import BaseCommand
from intervention.models import Participant
from django.conf import settings
from optparse import make_option

class Command(BaseCommand):
    args = ''
    help = ''

    option_list = BaseCommand.option_list + (
        make_option('-p', '--participant', dest='participant',
                    default=None,help='participant name'),
    )

    def handle(self, *args, **options):
        if not settings.DEBUG:
            print "this should never be run on production"
            return
            
        if not options["participant"]:
            print "Please specify the participant"
            return

        print "clearing participant data for [%s]" % options["participant"]
        participant = Participant.objects.get(name=options["participant"])
        participant.clear_all_data()
        participant.save()
        