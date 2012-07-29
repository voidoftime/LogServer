from django.conf.urls import patterns, include, url

from ORM.models import AllDevicesId

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import settings
from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webLogAdmin.views.home', name='home'),
    # url(r'^webLogAdmin/', include('webLogAdmin.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #Dajaxice URLS
    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
    url(r'^polls/$', 'polls.views.index'),
    url(r'^polls/'+AllDevicesId+'/$', 'polls.views.index'),
    url(r'^polls/(?P<poll_id>.+)/$', 'polls.views.detail'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
