from django.template import Context
from django.template import loader
from django.http import HttpResponse
from django.utils import translation

def render_shot(request, queryset, count_filter):
    template = loader.get_template('ajax_shot.html')

    context_data = {
        'shot': queryset,
        'count_filter': count_filter
    }
    result = template.render(context_data)

    return HttpResponse(result)


def render_groups(request, queryset):
    template = loader.get_template('ajax/ajax_groups.html')

    context_data = {
        'projects': queryset
    }
    result = template.render(context_data)

    return HttpResponse(result)


def render_domains(request, queryset, count_filter, choices):
    template = loader.get_template('ajax_domains.html')

    context_data = {
        'domains': queryset,
        'count_filter': count_filter,
        'statuses': choices
    }
    result = template.render(context_data)

    return HttpResponse(result)

def render_link_key(request, group, key, choices):
    template = loader.get_template('ajax_link_key.html')

    context_data = {
        'group': group,
        'key': key,
        'statuses': choices
    }
    result = template.render(context_data)

    return HttpResponse(result)

def render_urls(request, queryset, count_filter, choices):
    template = loader.get_template('ajax_urls.html')

    context_data = {
        'urls': queryset,
        'count_filter': count_filter,
        'statuses': choices
    }
    result = template.render(context_data)

    return HttpResponse(result)

