from django.contrib import admin
from .models import *


@admin.register(Proxy)
class ProxyAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'port', 'username')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'project')


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('query', 'project','impressions','ctr','clicks','position','demand')
