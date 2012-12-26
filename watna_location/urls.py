from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from emailusernames.forms import EmailAuthenticationForm

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('gmapi.urls.media')), # Use for debugging only.
    url(r'^$', 'location.views.map_page'),
    url(r'^places/$', 'location.views.locations_page'),
    url(r'^places/(?P<pk>\d+)$', 'location.views.edit_location_page'),
    url(r'^place/$', 'location.views.add_location_page'),
    url(r'^delete_place/$', 'location.views.delete_location_page'), 
    url(r'^find_location_by_id/$', 'location.views.find_location_by_id_page'),        
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'location.views.login_page'), 
    url(r'^logout/$', 'location.views.logout_page'),
    url(r'^register/$', 'location.views.register_page'),
    url(r'^edit_user/$', 'location.views.edit_user_page'),
    url(r'^register/success/$', direct_to_template,
        {'template': 'registration/register_success.html'}),    
)
