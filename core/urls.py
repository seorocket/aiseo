from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from core.views import *

app_name = 'core'


urlpatterns = [
    re_path(r'^$', index, name='index'),
    re_path(r'^robots\.txt$', robots, name='robots'),
    re_path(r'^ajax/$', ajax, name='ajax'),
    # re_path(r'^phrases/$', phrases, name='phrases'),
    # re_path(r'^projects/$', projects, name='projects'),
    re_path(r'^domains/$', domains, name='domains'),
    re_path(r'^domains/(?P<domain_id>[0-9A-Za-z\-_]+)/$', domain_item, name='domain_item'),
    re_path(r'^urls/$', urls, name='urls'),
    re_path(r'^urls/(?P<url_id>[0-9A-Za-z\-_]+)/$', url_item, name='url_item'),
    re_path(r'^shots/$', shots, name='shots'),
    re_path(r'^proxy/$', proxy, name='proxy'),
    re_path(r'^check-domains/$', check_domains, name='check_domains'),
    re_path(r'^domains-timestamps/$', domains_timestamps, name='domains_timestamps'),
    re_path(r'^get-urls-domain/(?P<domen_id>\d+)/$', get_urls_domain, name='get_urls_domain'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)