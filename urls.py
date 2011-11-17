from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import os.path
admin.autodiscover()

site_media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
        # Example:
        # (r'^smart_sa/', include('smart_sa.foo.urls')),
        ('^accounts/',include('djangowind.urls')),
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media_root}),
        (r'^multimedia/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.MEDIA_ROOT}),

        (r'^smart_sa$', 'smart_sa.intervention.views.no_vars', {'template_name': 'intervention/index.html'}),
        (r'^logout$', 'django.contrib.auth.views.logout', {'template_name': 'intervention/logged_out.html'}),
        #(r'^admin_confirm$', 'smart_sa.intervention.views.admin_confirm'), # login confirmation p.3

        ########
        # PUBLIC CLIENT VIEW
        # goals for static delivery require:
        # 1. no content at a directory 'root' i.e. urls that end in a '/'
        # 2. no name with the same as a directory
        # 3. windoze file-friendly names (e.g. no ';'s or other weird chars)
        ########

        (r'^intervention(?P<intervention_id>\d+)_intro.html$', 'smart_sa.intervention.views.intervention'),
        # page 4, 5
        (r'^session(?P<session_id>\d+)_agenda.html$', 'smart_sa.intervention.views.session'),
        # page 6,7, 15
        (r'^activity(?P<activity_id>\d+)_overview.html$', 'smart_sa.intervention.views.activity'), # page 12
        #game names can have a '-' e.g. video
        (r'^task/(?P<game_name>[-\w]+?)/(?P<game_id>\d+)?(?P<page_id>\w+).html$', 'smart_sa.intervention.views.game'),

        (r'^home.html$', 'smart_sa.intervention.views.no_vars',{'template_name':'intervention/index.html'}),
        (r'^index.html$', 'smart_sa.intervention.views.no_vars',{'template_name':'intervention/index.html'}),
        (r'^client_login.html$', 'smart_sa.intervention.views.no_vars',{'template_name':'intervention/client_login.html'}),
        (r'^client_login_confirm.html$', 'smart_sa.intervention.views.no_vars',{'template_name':'intervention/client_login_confirm.html'}),# login confirmation, p.2

        (r'^masivukeni_admin_data.html$', 'smart_sa.intervention.views.smart_data'),
        (r'^help/backup.html$', 'django.views.generic.simple.direct_to_template',{'template':'flatpages/backup_help.html'}),
        (r'^help/credits.html$', 'django.views.generic.simple.direct_to_template',{'template':'flatpages/credits.html'}),

        ########
        # TEST
        ########
        (r'^sessionNone_agenda.html$', 'smart_sa.intervention.views.test_session'),                       
        (r'^activityTest(?P<game_name>[-\w]+?)_overview.html$', 'smart_sa.intervention.views.test_activity'), # page 12

        ########
        # SERVER VIEW
        ########
        (r'^store_backup$', 'smart_sa.intervention.views.store_backup'),
        (r'^intervention_admin/save_backup$', 'smart_sa.intervention.views.save_backup_htmlupload'),
        (r'^intervention_admin/restore$', 'smart_sa.intervention.views.restore_from_backup'),

        # page 13, 14
        ########
        # ADMIN view
        ########
        (r'^intervention_admin/(?P<intervention_id>\d+)/$', 'smart_sa.intervention.views.intervention_admin'),
        (r'^intervention_admin/session/(?P<session_id>\d+)/$', 'smart_sa.intervention.views.session_admin'),
        (r'^intervention_admin/activity/(?P<activity_id>\d+)/$', 'smart_sa.intervention.views.activity_admin'), # page 12
        (r'^intervention_admin/task/(?P<activity_id>\d+)/$', 'smart_sa.intervention.views.gamepage_admin'), # page 12                       

        (r'^intervention_admin/content_sync/$','smart_sa.intervention.views.content_sync'),

        (r'^Masivukeni/Masivukeni/client_login.html', 'django.views.generic.simple.redirect_to', {'url':'/client_login.html'}),

        #semi-static help pages, etc.
        #(r'^background/(?P<content_label>\d+)/$', 'smart_sa.intervention.views.background'),

        # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
        # to INSTALLED_APPS to enable admin documentation:
        #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

        # Uncomment the next line to enable the admin:
        (r'^admin/(.*)', admin.site.root),
        ('^$','smart_sa.intervention.views.no_vars',{'template_name':'intervention/index.html'}),
                       
)
