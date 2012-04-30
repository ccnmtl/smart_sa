# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'CounselorNote.participant'
        db.add_column('intervention_counselornote', 'participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['intervention.Participant'], null=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'CounselorNote.participant'
        db.delete_column('intervention_counselornote', 'participant_id')


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
            'collect_buddy_name': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'collect_notes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'collect_reasons_for_returning': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'collect_referral_info': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'deployment': ('django.db.models.fields.CharField', [], {'default': "'Clinic'", 'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json_data': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'intervention.clientsession': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'ClientSession'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'defaulter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['intervention.Participant']", 'null': 'True'}),
            'participantsession': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['intervention.ParticipantSession']"})
        },
        'intervention.deployment': {
            'Meta': {'object_name': 'Deployment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Clinic'", 'max_length': '256'})
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
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
            'buddy_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'clinical_notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'defaulter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'defaulter_referral_alcohol': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'defaulter_referral_drugs': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'defaulter_referral_mental_health': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'defaulter_referral_notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'defaulter_referral_other': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'male'", 'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_number': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'initial_referral_alcohol': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'initial_referral_drug_use': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'initial_referral_mental_health': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'initial_referral_notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'initial_referral_other': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'patient_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'reasons_for_returning': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
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
