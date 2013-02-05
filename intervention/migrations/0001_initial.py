# flake8: noqa
# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Intervention'
        db.create_table('intervention_intervention', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('general_instructions', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('intervention', ['Intervention'])

        # Adding model 'ClientSession'
        db.create_table('intervention_clientsession', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('intervention', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['intervention.Intervention'])),
            ('short_title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('long_title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('introductory_copy', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('intervention', ['ClientSession'])

        # Adding model 'Activity'
        db.create_table('intervention_activity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('clientsession', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['intervention.ClientSession'])),
            ('short_title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('long_title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('objective_copy', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('game', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('intervention', ['Activity'])

        # Adding model 'GamePage'
        db.create_table('intervention_gamepage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['intervention.Activity'], null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('instructions', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('intervention', ['GamePage'])

        # Adding model 'Instruction'
        db.create_table('intervention_instruction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['intervention.Activity'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('style', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('instruction_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('help_copy', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('intervention', ['Instruction'])

        # Adding model 'Backup'
        db.create_table('intervention_backup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('json_data', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('intervention', ['Backup'])

        # Adding model 'Fact'
        db.create_table('intervention_fact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fact_key', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('fact_value', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('help_copy', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('intervention', ['Fact'])


    def backwards(self, orm):
        
        # Deleting model 'Intervention'
        db.delete_table('intervention_intervention')

        # Deleting model 'ClientSession'
        db.delete_table('intervention_clientsession')

        # Deleting model 'Activity'
        db.delete_table('intervention_activity')

        # Deleting model 'GamePage'
        db.delete_table('intervention_gamepage')

        # Deleting model 'Instruction'
        db.delete_table('intervention_instruction')

        # Deleting model 'Backup'
        db.delete_table('intervention_backup')

        # Deleting model 'Fact'
        db.delete_table('intervention_fact')


    models = {
        'intervention.activity': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Activity'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'clientsession': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['intervention.ClientSession']"}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['intervention']
