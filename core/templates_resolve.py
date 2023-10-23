from django.template import Context
from django.template import loader
from django.http import HttpResponse
from django.utils import translation
from .views import *
from django.core import serializers


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


def render_phrases(request, queryset):
    template = loader.get_template('ajax/ajax_phrases.html')

    context_data = {
        'keys': queryset
    }
    result = template.render(context_data)

    return HttpResponse(result)


def render_accordion_projects(request, queryset):
    template = loader.get_template('ajax/ajax_accordion_projects.html')

    choices = dict()

    for choice in CHOICE_SEARCHQUERY_STATUS:
        choices[choice[0]] = {'name': choice[1]}

    context_data = {
        'projects': queryset,
        'statuses': choices,
    }
    result = template.render(context_data)

    return HttpResponse(result)


def render_domains(request, queryset):
    template = loader.get_template('ajax/ajax_domains.html')

    context_data = {
        'domains': queryset
    }
    result = template.render(context_data)

    return result