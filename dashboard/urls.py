from django.conf.urls.defaults import patterns

urlpatterns = patterns(
    '',
    (r'^$', 'smart_sa.dashboard.views.index'),
)
