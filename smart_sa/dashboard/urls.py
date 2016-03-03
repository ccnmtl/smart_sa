from django.conf.urls import patterns

urlpatterns = patterns(
    '',
    (r'^$', 'smart_sa.dashboard.views.index'),
    (r'^download/$', 'smart_sa.dashboard.views.download'),
)
