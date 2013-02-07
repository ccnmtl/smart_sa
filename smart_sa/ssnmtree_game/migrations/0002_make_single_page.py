# flake8: noqa
# encoding: utf-8
from south.v2 import DataMigration
from smart_sa.intervention.models import Activity, GamePage

class Migration(DataMigration):

    def forwards(self, orm):
        # All ssnmtree activities should have a single game page
        # Kill off the other ones.
        activities = Activity.objects.filter(game='ssnmTree')
        for a in activities:
            GamePage.objects.filter(activity=a, _order__gte=1).delete()


    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")


    models = {
        
    }

    complete_apps = ['ssnmtree_game']
