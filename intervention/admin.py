from smart_sa.intervention.models import *
from django.contrib import admin

class InterventionAdmin(admin.ModelAdmin):
    fields = ['name']

class ClientSessionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General',  {'fields': ['intervention', 'short_title', 'long_title']}),
    ]
    list_filter = ['short_title']

admin.site.register(Intervention)
admin.site.register(ClientSession, ClientSessionAdmin)
admin.site.register(Activity)
admin.site.register(GamePage)
admin.site.register(Instruction)
admin.site.register(Fact)
