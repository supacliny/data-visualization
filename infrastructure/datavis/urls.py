# Serve static content.
from django.conf.urls.defaults import patterns, url
from infrastructure import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('datavis.views',
    url(r'^$', 'index', name='index'),
	url(r'^predict/(?P<symbol>.*)$', 'predict', name='predict'),
	url(r'^fft/(?P<symbol>.*)$', 'fft', name='fft'),
	url(r'^kalman/(?P<symbol>.*)$', 'kalman', name='kalman'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^content/(?P<path>.*)$', 'django.views.static.serve',  
         {'document_root':     settings.MEDIA_ROOT}),
    )

