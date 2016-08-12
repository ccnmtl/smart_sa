from django.conf.urls import url
from .views import index, download

urlpatterns = [
    url(r'^$', index),
    url(r'^download/$', download),
]
