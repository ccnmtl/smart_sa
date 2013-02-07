# flake8: noqa
# encoding: utf-8
from south.v2 import DataMigration
from django.core import management

class Migration(DataMigration):

    def forwards(self, orm):
        management.call_command('loaddata', 'initial_issues', verbosity=0)

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'problemsolving_game.issue': {
            'Meta': {'object_name': 'Issue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ordinality': ('django.db.models.fields.IntegerField', [], {}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['problemsolving_game']
