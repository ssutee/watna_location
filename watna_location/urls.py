from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from emailusernames.forms import EmailAuthenticationForm
from django.conf import settings
from location.views import PictureCreateView, PictureDeleteView
from django.contrib.auth.decorators import login_required

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^i18n/', include('django.conf.urls.i18n')),        
    url(r'', include('gmapi.urls.media')), # Use for debugging only.
    url(r'^$', 'location.views.map_page'),
    url(r'^my_info/$', 'location.views.my_info_page'),
    url(r'^places/$', 'location.views.locations_page'),    
    url(r'^places/(?P<pk>\d+)$', 'location.views.edit_location_page'),
    url(r'^place/$', 'location.views.add_location_page'),
    url(r'^delete_place/$', 'location.views.delete_location_page'), 
    url(r'^find_location_by_id/$', 'location.views.find_location_by_id_page'),  
    url(r'^set_map_type/$', 'location.views.set_map_type_page'),   
    url(r'^set_sorting/$', 'location.views.set_sorting_page'),
    url(r'^set_display/$', 'location.views.set_display_page'),                
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'location.views.login_page'), 
    url(r'^logout/$', 'location.views.logout_page'),
    url(r'^register/$', 'location.views.register_page'),
    url(r'^edit_user/$', 'location.views.edit_user_page'),
    url(r'^register/success/$', direct_to_template,
        {'template': 'registration/register_success.html'}),  
    url(r'^new_upload/(?P<pk>\d+)$', login_required(PictureCreateView.as_view()), {}, 'upload-new'),
    url(r'^delete_upload/(?P<pk>\d+)$', login_required(PictureDeleteView.as_view()), {}, 'upload-delete'),              
    url(r'^messages/',include('django_messages.urls')),
)

import os

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(.*)$', 'django.views.static.serve', 
            {'document_root': settings.MEDIA_ROOT}),
    )