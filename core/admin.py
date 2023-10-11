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
    list_display = ('ip_address', 'port', 'username', 'password', 'protocol', 'status')
    list_filter = ('protocol', 'status')
    search_fields = ('ip_address', 'port', 'username', 'password')

    fieldsets = (
        (None, {'fields': ('ip_address', 'port', 'username', 'password')}),
        ('Протокол', {'fields': ('protocol',)}),
        ('Статус', {'fields': ('status',)}),
    )

    # Определите порядок протоколов в административном интерфейсе
    radio_fields = {'protocol': admin.VERTICAL}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'pages', 'history', 'status', 'snippet', 'image', 'first_captured', 'stripped_snippet', 'display_name', 'text', 'link', 'thumb', 'capture', 'video', 'webpage', 'audio', 'last_captured')
    list_filter = ('project', 'status')
    search_fields = ('name', 'project__name')  # поиск по имени и имени проекта


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('query', 'project')


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('url', 'mimetype', 'timestamp', 'endtimestamp', 'groupcount', 'uniqcount', 'domain', 'status', 'file')


@admin.register(Shot)
class ShotAdmin(admin.ModelAdmin):
    list_display = ('name', 'file', 'date', 'status')