# flake8: noqa
# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Participant'
        db.create_table('intervention_participant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('id_number', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('defaulter', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('intervention', ['Participant'])

        # Adding model 'ParticipantActivity'
        db.create_table('intervention_participantactivity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['intervention.Participant'])),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['intervention.Activity'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='incomplete', max_length=256)),
        ))
        db.send_create_signal('intervention', ['ParticipantActivity'])

        # Adding model 'ParticipantGameVar'
        db.create_table('intervention_participantgamevar', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['intervention.Participant'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('value', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
        ))
        db.send_create_signal('intervention', ['ParticipantGameVar'])

        # Adding model 'CounselorNote'
        db.create_table('intervention_counselornote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participantsession', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['intervention.ParticipantSession'])),
            ('counselor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('notes', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
        ))
        db.send_create_signal('intervention', ['CounselorNote'])

        # Adding model 'ParticipantSession'
        db.create_table('intervention_participantsession', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['intervention.Participant'])),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['intervention.ClientSession'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='incomplete', max_length=256)),
        ))
        db.send_create_signal('intervention', ['ParticipantSession'])


    def backwards(self, orm):
        
        # Deleting model 'Participant'
        db.delete_table('intervention_participant')

        # Deleting model 'ParticipantActivity'
        db.delete_table('intervention_participantactivity')

        # Deleting model 'ParticipantGameVar'
        db.delete_table('intervention_participantgamevar')

        # Deleting model 'CounselorNote'
        db.delete_table('intervention_counselornote')

        # Deleting model 'ParticipantSession'
        db.delete_table('intervention_participantsession')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
        'intervention.counselornote': {
            'Meta': {'object_name': 'CounselorNote'},
            'counselor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'participantsession': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['intervention.ParticipantSession']"})
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
        },
        'intervention.participant': {
            'Meta': {'object_name': 'Participant'},
            'defaulter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_number': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'intervention.participantactivity': {
            'Meta': {'object_name': 'ParticipantActivity'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['intervention.Activity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['intervention.Participant']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'incomplete'", 'max_length': '256'})
        },
        'intervention.participantgamevar': {
            'Meta': {'object_name': 'ParticipantGameVar'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['intervention.Participant']"}),
            'value': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'})
        },
        'intervention.participantsession': {
            'Meta': {'object_name': 'ParticipantSession'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['intervention.Participant']"}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['intervention.ClientSession']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'incomplete'", 'max_length': '256'})
        }
    }

    complete_apps = ['intervention']
