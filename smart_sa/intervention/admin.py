from smart_sa.intervention.models import Intervention, Activity
from smart_sa.intervention.models import ClientSession, GamePage
from smart_sa.intervention.models import Participant, ParticipantSession
from smart_sa.intervention.models import ParticipantActivity
from smart_sa.intervention.models import ParticipantGameVar
from smart_sa.intervention.models import CounselorNote
from smart_sa.intervention.models import Deployment
from smart_sa.intervention.models import Instruction
from django.contrib import admin


class InterventionAdmin(admin.ModelAdmin):
    fields = ['name']


class ClientSessionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General',
         {'fields': ['intervention', 'short_title', 'long_title']}),
    ]
    list_filter = ['short_title']

admin.site.register(Intervention)
admin.site.register(ClientSession, ClientSessionAdmin)
admin.site.register(Activity)
admin.site.register(GamePage)
admin.site.register(Instruction)
admin.site.register(Participant)
admin.site.register(ParticipantSession)
admin.site.register(ParticipantActivity)
admin.site.register(ParticipantGameVar)
admin.site.register(CounselorNote)
admin.site.register(Deployment)
