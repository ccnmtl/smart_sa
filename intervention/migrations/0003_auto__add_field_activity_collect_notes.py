# flake8: noqa
# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Activity.collect_notes'
        db.add_column('intervention_activity', 'collect_notes', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Activity.collect_notes'
        db.delete_column('intervention_activity', 'collect_notes')


    models = {
        'intervention.activity': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Activity'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'clientsession': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['intervention.ClientSession']"}),
            'collect_notes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'game': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'objective_copy': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        'intervention.backup': {
            'Meta': {'object_name': 'Backup'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json_data': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'intervention.clientsession': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'ClientSession'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intervention': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['intervention.Intervention']"}),
            'introductory_copy': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'long_title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        'intervention.fact': {
            'Meta': {'object_name': 'Fact'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fact_key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'fact_value': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'help_copy': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'intervention.gamepage': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'GamePage'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['intervention.Activity']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'})
        },
        'intervention.instruction': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Instruction'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['intervention.Activity']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'help_copy': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'instruction_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'})
        },
        'intervention.intervention': {
            'Meta': {'object_name': 'Intervention'},
            'general_instructions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intervention_id': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '8'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['intervention']
