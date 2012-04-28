from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import os.path
admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
        (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
        ('^accounts/',include('djangowind.urls')),
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media_root}),
        (r'^multimedia/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.MEDIA_ROOT}),

        (r'^testgen/$', 'smart_sa.intervention.views.testgen'),
        (r'^set_participant/$','smart_sa.intervention.views.set_participant'),
        (r'^clear_participant/$','smart_sa.intervention.views.clear_participant'),
        (r'^set_deployment/$','smart_sa.intervention.views.set_deployment'),
        (r'^intervention/$','smart_sa.intervention.views.counselor_landing_page'),
        (r'^manage/$','smart_sa.intervention.views.manage_participants'),
        (r'^manage/add_participant/$','smart_sa.intervention.views.add_participant'),
        (r'^manage/participant/(?P<participant_id>\d+)/delete/$','smart_sa.intervention.views.delete_participant'),
        (r'^manage/participant/(?P<participant_id>\d+)/edit/$','smart_sa.intervention.views.edit_participant'),                       
        (r'^manage/participant/(?P<participant_id>\d+)/view/$','smart_sa.intervention.views.view_participant'),                       

        (r'^manage/add_counselor/$','smart_sa.intervention.views.add_counselor'),
        (r'^manage/counselor/(?P<counselor_id>\d+)/edit/$','smart_sa.intervention.views.edit_counselor'),

        (r'manage/report/$','smart_sa.intervention.views.report_index'),
        (r'manage/report/download/$','smart_sa.intervention.views.participant_data_download'),
        (r'manage/restore_participants/$','smart_sa.intervention.views.restore_participants'),
        (r'manage/update_intervention_content/$','smart_sa.intervention.views.update_intervention_content'),                               

        (r'^practice/(?P<intervention_id>\d+)/$','smart_sa.intervention.views.start_practice_mode'),
        (r'^intervention/(?P<intervention_id>\d+)/$','smart_sa.intervention.views.intervention'),
        (r'^session/(?P<session_id>\d+)/$','smart_sa.intervention.views.session'),
        (r'^session/(?P<session_id>\d+)/complete/$','smart_sa.intervention.views.complete_session'),
        (r'^activity/(?P<activity_id>\d+)/$','smart_sa.intervention.views.activity'),
        (r'^activity/(?P<activity_id>\d+)/complete/$','smart_sa.intervention.views.complete_activity'),
        (r'^task/(?P<game_id>\d+)/(?P<page_id>\w+)/$', 'smart_sa.intervention.views.game'),
        (r'^save_game_state/$','smart_sa.intervention.views.save_game_state'),                       

        ########
        # ADMIN view
        ########
        (r'^intervention_admin/(?P<intervention_id>\d+)/$', 'smart_sa.intervention.views.intervention_admin'),
        (r'^intervention_admin/session/(?P<session_id>\d+)/$', 'smart_sa.intervention.views.session_admin'),
        (r'^intervention_admin/activity/(?P<activity_id>\d+)/$', 'smart_sa.intervention.views.activity_admin'), # page 12
        (r'^intervention_admin/task/(?P<activity_id>\d+)/$', 'smart_sa.intervention.views.gamepage_admin'), # page 12                       

        (r'^intervention_admin/content_sync/$','smart_sa.intervention.views.content_sync'),
        (r'^intervention_admin/zip_download/$','smart_sa.intervention.views.zip_download'),
        (r'^intervention_admin/list_uploads/$','smart_sa.intervention.views.list_uploads'),                       

        (r'^admin/', include(admin.site.urls)),
        ('^$','smart_sa.intervention.views.no_vars',{'template_name':'intervention/index.html'}),
                       
)
