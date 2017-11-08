from django.conf.urls import url
from .views import index, download, participant

urlpatterns = [
    url(r'^$', index),
    url(r'^download/$', download),
    url(r'^participant/(?P<participant_id>\d+)/$', participant),
]
