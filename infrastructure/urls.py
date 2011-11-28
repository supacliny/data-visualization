# Modularize URLS for each app.
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^datavis/', include('datavis.urls')),
)