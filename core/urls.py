from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.db.models import Q
from django.urls import path

from core.views import *

app_name = 'core'


urlpatterns = [
    re_path(r'^$', index, name='index'),
    re_path(r'^robots\.txt$', robots, name='robots'),
    re_path(r'^ajax/$', ajax, name='ajax'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)