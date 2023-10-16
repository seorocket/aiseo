from django.template import Context
from django.template import loader
from django.http import HttpResponse
from django.utils import translation


def render_groups(request, queryset):
    template = loader.get_template('ajax/ajax_groups.html')

    context_data = {
        'projects': queryset
    }
    result = template.render(context_data)

    return HttpResponse(result)


def render_proxy(request, queryset):
    template = loader.get_template('ajax/ajax_proxy.html')

    context_data = {
        'proxy': queryset
    }
    result = template.render(context_data)

    return HttpResponse(result)
