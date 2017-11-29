import os.path

import django.contrib.auth.views
import django.views.static

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

from smart_sa.intervention.views import (
    game, log_activity_visit, save_game_state, intervention_admin,
    session_admin, activity_admin, gamepage_admin, content_sync,
    zip_download, list_uploads, participant_data_download,
    restore_participants, intervention, session,
    view_participant, add_counselor, edit_counselor, report_index,
    activity, complete_activity, log_session_visit, complete_session,
    start_practice_mode,
    update_intervention_content, delete_participant, set_deployment,
    testgen, set_participant, clear_participant, counselor_landing_page,
    manage_participants, add_participant, edit_participant,
    IndexView, InterventionReport, view_participant_progress
)

admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__), "../media")

urlpatterns = [
    url(r'^accounts/logout/$',
        django.contrib.auth.views.logout, {'next_page': '/'}),
    url('^accounts/', include('djangowind.urls')),
    url(r'^site_media/(?P<path>.*)$',
        django.views.static.serve, {'document_root': site_media_root}),
    url(r'^multimedia/(?P<path>.*)$',
        django.views.static.serve, {'document_root': settings.MEDIA_ROOT}),

    url(r'^testgen/$', testgen),
    url(r'^set_participant/$', set_participant),
    url(r'^clear_participant/$', clear_participant),
    url(r'^set_deployment/$', set_deployment),
    url(r'^intervention/$', counselor_landing_page),
    url(r'^manage/$', manage_participants),
    url(r'^manage/add_participant/$', add_participant),
    url(r'^manage/participant/(?P<participant_id>\d+)/delete/$',
        delete_participant),
    url(r'^manage/participant/(?P<participant_id>\d+)/edit/$',
        edit_participant),
    url(r'^manage/participant/(?P<participant_id>\d+)/view/$',
        view_participant),

    url(r'^manage/add_counselor/$', add_counselor),
    url(r'^manage/counselor/(?P<counselor_id>\d+)/edit/$', edit_counselor),

    url(r'mnage/report/$', report_index),
    url(r'manage/report/download/$', participant_data_download),
    url(r'manage/restore_participants/$', restore_participants),
    url(r'manage/update_intervention_content/$', update_intervention_content),

    url(r'^practice/(?P<intervention_id>\d+)/$', start_practice_mode),
    url(r'^intervention/(?P<intervention_id>\d+)/$', intervention),
    url(r'^intervention/participant-report$',
        view_participant_progress),
    url(r'^intervention/(?P<pk>\d+)/report/$',
        InterventionReport.as_view(), name='intervention-report'),
    url(r'^session/(?P<session_id>\d+)/$', session),
    url(r'^session/(?P<session_id>\d+)/complete/$', complete_session),
    url(r'^session/(?P<session_id>\d+)/visit/$', log_session_visit),
    url(r'^activity/(?P<activity_id>\d+)/$', activity),
    url(r'^activity/(?P<activity_id>\d+)/complete/$', complete_activity),
    url(r'^activity/(?P<activity_id>\d+)/visit/$', log_activity_visit),
    url(r'^task/(?P<game_id>\d+)/(?P<page_id>\w+)/$', game),
    url(r'^save_game_state/$', save_game_state),

    ########
    # ADMIN view
    ########
    url(r'^intervention_admin/(?P<intervention_id>\d+)/$', intervention_admin),
    url(r'^intervention_admin/session/(?P<session_id>\d+)/$', session_admin),
    # page 12
    url(r'^intervention_admin/activity/(?P<activity_id>\d+)/$',
        activity_admin),
    # page 12
    url(r'^intervention_admin/task/(?P<activity_id>\d+)/$', gamepage_admin),

    url(r'^intervention_admin/content_sync/$', content_sync),
    url(r'^intervention_admin/zip_download/$', zip_download),
    url(r'^intervention_admin/list_uploads/$', list_uploads),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^smoketest/', include('smoketest.urls')),

    url('^$', IndexView.as_view()),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
