# flake8: noqa
# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Issue'
        db.create_table('problemsolving_game_issue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('ordinality', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('problemsolving_game', ['Issue'])


    def backwards(self, orm):
        
        # Deleting model 'Issue'
        db.delete_table('problemsolving_game_issue')


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
