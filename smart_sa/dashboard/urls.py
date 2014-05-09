from django.conf.urls import patterns

urlpatterns = patterns(
    '',
    (r'^$', 'smart_sa.dashboard.views.index'),
)
