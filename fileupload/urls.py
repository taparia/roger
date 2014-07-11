# encoding: utf-8
from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#from django.views.generic.simple import direct_to_template
#admin.autodiscover()

urlpatterns = patterns('',
#    url(r'^basic/$', BasicVersionCreateView.as_view(), name='upload-basic'),
    url(r'^basic/$', 'fileupload.views.list'),
    url(r'^result/$', 'fileupload.views.result'),
)
