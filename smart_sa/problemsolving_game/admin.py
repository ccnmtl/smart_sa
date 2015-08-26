from django.contrib import admin
from django import forms
from smart_sa.problemsolving_game.models import Issue


class IssueForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)
    subtext = forms.CharField(required=False, widget=forms.Textarea)
    example = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = Issue
        exclude = []


class IssueAdmin(admin.ModelAdmin):
    form = IssueForm

admin.site.register(Issue, IssueAdmin)
