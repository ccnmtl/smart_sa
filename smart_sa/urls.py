import os.path
from django.urls import path
import django.contrib.auth.views
import django.views.static

from django.conf.urls import include
from django.urls import re_path
from django.contrib import admin
from django.conf import settings
from django_cas_ng import views as cas_views


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
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    path('cas/login', cas_views.LoginView.as_view(),
         name='cas_ng_login'),
    path('cas/logout', cas_views.LogoutView.as_view(),
         name='cas_ng_logout'),

    re_path(r'^site_media/(?P<path>.*)$',
            django.views.static.serve, {'document_root': site_media_root}),
    re_path(r'^multimedia/(?P<path>.*)$',
            django.views.static.serve, {'document_root': settings.MEDIA_ROOT}),

    re_path(r'^testgen/$', testgen),
    re_path(r'^set_participant/$', set_participant),
    re_path(r'^clear_participant/$', clear_participant),
    re_path(r'^set_deployment/$', set_deployment),
    re_path(r'^intervention/$', counselor_landing_page),
    re_path(r'^manage/$', manage_participants),
    re_path(r'^manage/add_participant/$', add_participant),
    re_path(r'^manage/participant/(?P<participant_id>\d+)/delete/$',
            delete_participant),
    re_path(r'^manage/participant/(?P<participant_id>\d+)/edit/$',
            edit_participant),
    re_path(r'^manage/participant/(?P<participant_id>\d+)/view/$',
            view_participant),

    re_path(r'^manage/add_counselor/$', add_counselor),
    re_path(r'^manage/counselor/(?P<counselor_id>\d+)/edit/$', edit_counselor),

    re_path(r'mnage/report/$', report_index),
    re_path(r'manage/report/download/$', participant_data_download),
    re_path(r'manage/restore_participants/$', restore_participants),
    re_path(r'manage/update_intervention_content/$',
            update_intervention_content),

    re_path(r'^practice/(?P<intervention_id>\d+)/$', start_practice_mode),
    re_path(r'^intervention/(?P<intervention_id>\d+)/$', intervention),
    re_path(r'^intervention/participant-report$',
            view_participant_progress),
    re_path(r'^intervention/(?P<pk>\d+)/report/$',
            InterventionReport.as_view(), name='intervention-report'),
    re_path(r'^session/(?P<session_id>\d+)/$', session),
    re_path(r'^session/(?P<session_id>\d+)/complete/$', complete_session),
    re_path(r'^session/(?P<session_id>\d+)/visit/$', log_session_visit),
    re_path(r'^activity/(?P<activity_id>\d+)/$', activity),
    re_path(r'^activity/(?P<activity_id>\d+)/complete/$', complete_activity),
    re_path(r'^activity/(?P<activity_id>\d+)/visit/$', log_activity_visit),
    re_path(r'^task/(?P<game_id>\d+)/(?P<page_id>\w+)/$', game),
    re_path(r'^save_game_state/$', save_game_state),

    ########
    # ADMIN view
    ########
    re_path(r'^intervention_admin/(?P<intervention_id>\d+)/$',
            intervention_admin),
    re_path(r'^intervention_admin/session/(?P<session_id>\d+)/$',
            session_admin),
    # page 12
    re_path(r'^intervention_admin/activity/(?P<activity_id>\d+)/$',
            activity_admin),
    # page 12
    re_path(r'^intervention_admin/task/(?P<activity_id>\d+)/$',
            gamepage_admin),

    re_path(r'^intervention_admin/content_sync/$', content_sync),
    re_path(r'^intervention_admin/zip_download/$', zip_download),
    re_path(r'^intervention_admin/list_uploads/$', list_uploads),

    re_path(r'^admin/', admin.site.urls),
    re_path(r'^smoketest/', include('smoketest.urls')),

    re_path('^$', IndexView.as_view()),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]
