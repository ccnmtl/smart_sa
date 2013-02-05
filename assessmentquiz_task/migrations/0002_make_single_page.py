# flake8: noqa
# encoding: utf-8
from south.v2 import DataMigration
from intervention.models import Activity, GamePage

class Migration(DataMigration):

    def forwards(self, orm):
        activities = Activity.objects.filter(game='assessmentquiz')
        for a in activities:
            GamePage.objects.filter(activity=a, _order__gte=1).delete()


    def backwards(self, orm):
        "Write your backwards methods here."


    models = {
        
    }

    complete_apps = ['assessmentquiz_task']
