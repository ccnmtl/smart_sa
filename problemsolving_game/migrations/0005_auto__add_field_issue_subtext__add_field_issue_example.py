# flake8: noqa
# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Issue.subtext'
        db.add_column('problemsolving_game_issue', 'subtext', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True), keep_default=False)

        # Adding field 'Issue.example'
        db.add_column('problemsolving_game_issue', 'example', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Issue.subtext'
        db.delete_column('problemsolving_game_issue', 'subtext')

        # Deleting field 'Issue.example'
        db.delete_column('problemsolving_game_issue', 'example')


    models = {
        'problemsolving_game.issue': {
            'Meta': {'object_name': 'Issue'},
            'example': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ordinality': ('django.db.models.fields.IntegerField', [], {}),
            'subtext': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['problemsolving_game']
