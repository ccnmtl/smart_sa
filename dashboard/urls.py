from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns(
    '',
    (r'^$', 'smart_sa.dashboard.views.index'),
)
