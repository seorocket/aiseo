from django.contrib import admin
from .models import *

seo_fields = [
    'alias',
    'seo_h1',
    'seo_title',
    'seo_description',
    'content'
]


@admin.register(TextPage)
class TextPageAdmin(admin.ModelAdmin):
    fieldsets = [('Основные', {"fields": ["name"]}), ('SEO информация', {'fields': seo_fields})]

    def get_prepopulated_fields(self, request, obj=None):
        return {"alias": ("name",)}


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
    list_display = ('query', 'project')


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('url', 'mimetype', 'timestamp', 'endtimestamp', 'groupcount', 'uniqcount', 'domain', 'status', 'file')


@admin.register(Shot)
class ShotAdmin(admin.ModelAdmin):
    list_display = ('name', 'file', 'date', 'status')