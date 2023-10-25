import django_filters
import random
from django_filters import rest_framework as filters
import json
import validators

from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from core.serializers import *
from core.templates_resolve import *
from django.contrib.auth.models import User
from core.models import *
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template import loader
from django.template.context_processors import csrf
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.serializers import serialize
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def default_context(request, alias, obj):
    data = get_object_or_404(obj, alias=alias)
    # csrf_token = csrf(request)
    # c = csrf(request)
    user = request.user

    context = {
        'data': data,
        # 'csrf_token': csrf_token,
        # 'c': c,
        'request': request,
        'user': user,
    }
    context.update(csrf(request))

    return context


def robots(request):
    template = loader.get_template('robots.txt')

    context = default_context(request, "index", TextPage)
    context.update({
        'ssl': request.is_secure()
    })

    return HttpResponse(template.render(context), content_type="text/plain")


@login_required
def index(request):
    context = default_context(request, "index", TextPage)
    template = loader.get_template('index.html')
    current_user = request.user
    if current_user.is_staff:
        projects = Project.objects.all().order_by('-id')
    else:
        projects = Project.objects.filter(user=current_user).order_by('-id')
    keys = SearchQuery.objects.all()

    status_entry = request.GET.get('status')
    if status_entry:
        keys = keys.filter(status=status_entry)

    choices = dict()

    for choice in CHOICE_SEARCHQUERY_STATUS:
        choices[choice[0]] = {'name': choice[1]}

    paginator = Paginator(projects, 250)
    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)

    context.update({
        'link': True,
        'projects': projects,
        'keys': keys,
        'statuses': choices,
    })

    return HttpResponse(template.render(context))


# @login_required
# def phrases(request):
#     context = default_context(request, "index", TextPage)
#     template = loader.get_template('phrases.html')
#     projects = Project.objects.all()
#     keys = SearchQuery.objects.all()
#
    # status_entry = request.GET.get('status')
    # if status_entry:
    #     keys = keys.filter(status=status_entry)
    #
    # choices = dict()
    #
    # for choice in CHOICE_SEARCHQUERY_STATUS:
    #     choices[choice[0]] = {'name': choice[1]}
#
#     paginator = Paginator(projects, 250)
#     page = request.GET.get('page')
#     try:
#         projects = paginator.page(page)
#     except PageNotAnInteger:
#         projects = paginator.page(1)
#     except EmptyPage:
#         projects = paginator.page(paginator.num_pages)
#
#     context.update({
#         'link': True,
#         'projects': projects,
#         'keys': keys,
#         'statuses': choices,
#     })
#
#     return HttpResponse(template.render(context))


# @login_required
# def projects(request):
#     context = default_context(request, "index", TextPage)
#     template = loader.get_template('projects.html')
#     projects = Project.objects.all()
#
#     paginator = Paginator(projects, 250)
#     page = request.GET.get('page')
#     try:
#         projects = paginator.page(page)
#     except PageNotAnInteger:
#         projects = paginator.page(1)
#     except EmptyPage:
#         projects = paginator.page(paginator.num_pages)
#
#     context.update({
#         'link': True,
#         'projects': projects,
#     })
#
#     return HttpResponse(template.render(context))


@login_required
def domains(request):
    context = default_context(request, "index", TextPage)
    template = loader.get_template('domains.html')
    domains = Domain.objects.exclude(status=4).order_by('-id')
    current_user = request.user
    if current_user.is_staff:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(user=current_user)

    choices = dict()

    for choice in CHOICE_DOMAIN_STATUS:
        choices[choice[0]] = {'name': choice[1]}

    search_query = request.GET.get('search')
    if search_query:
        search_filter = Q(name__icontains=search_query)
        domains = domains.filter(search_filter)

    # фильтр по левому меню
    left_filter = request.GET.dict()
    if left_filter.get('left_filter'):
        left_filter.pop('filter_p_sort')

    for key in left_filter.keys():
        value = left_filter.get(key)
        if ',' in value:
            values = [int(v) for v in value.split(',')]
            q_objects = Q()
            for v in values:
                q_objects |= Q(**{key: v})
            domains = domains.filter(q_objects)
        try:
            domains = domains.filter(**{key: value})
        except Exception:
            pass

    status_entry = request.GET.get('status')
    if status_entry:
        domains = domains.filter(status=status_entry)

    domains_count = domains.count()

    paginator = Paginator(domains, 250)
    page = request.GET.get('page')
    try:
        domains = paginator.page(page)
    except PageNotAnInteger:
        domains = paginator.page(1)
    except EmptyPage:
        domains = paginator.page(paginator.num_pages)

    context.update({
        'link': True,
        'filter': True,
        'domains': domains,
        'domains_count': domains_count,
        'statuses': choices,
        'projects': projects,
        'ahrefs_rank': True,
        'domains_filter': True
    })

    return HttpResponse(template.render(context))


@login_required
def domain_item(request, domain_id):
    data = get_object_or_404(Domain, id=domain_id)
    template = loader.get_template('domain-item.html')
    urls = File.objects.filter(domain=domain_id).order_by('-id')

    choices = dict()

    for choice in CHOICE_FILE_STATUS:
        choices[choice[0]] = {'name': choice[1]}

    search_query = request.GET.get('search')
    if search_query:
        search_filter = Q(name__icontains=search_query)
        urls = urls.filter(search_filter)

    status_entry = request.GET.get('status')
    if status_entry:
        urls = urls.filter(status=status_entry)

    urls_count = urls.count()

    urls_data = [{"name": url.url, "id": url.id} for url in urls]
    nested_urls = create_nested_url_list(urls_data)

    paginator = Paginator(urls, 250)
    page = request.GET.get('page')
    try:
        urls = paginator.page(page)
    except PageNotAnInteger:
        urls = paginator.page(1)
    except EmptyPage:
        urls = paginator.page(paginator.num_pages)

    context = {
        'link': True,
        'filter': True,
        'data': data,
        'urls': urls,
        'urls_count': urls_count,
        'statuses': choices,
        'request': request,
        'nested_urls': nested_urls,
        'user': request.user,
        'urls_filter': True
    }
    context.update(csrf(request))

    return HttpResponse(template.render(context))


@login_required
def urls(request):
    context = default_context(request, "index", TextPage)
    template = loader.get_template('urls.html')
    urls = File.objects.all().order_by('-id')
    domains = Domain.objects.all()

    choices = dict()

    for choice in CHOICE_FILE_STATUS:
        choices[choice[0]] = {'name': choice[1]}

    search_query = request.GET.get('search')
    if search_query:
        search_filter = Q(url__icontains=search_query)
        urls = urls.filter(search_filter)

    # фильтр по левому меню
    left_filter = request.GET.dict()
    if left_filter.get('left_filter'):
        left_filter.pop('filter_p_sort')

    for key in left_filter.keys():
        value = left_filter.get(key)
        if ',' in value:
            values = [int(v) for v in value.split(',')]
            q_objects = Q()
            for v in values:
                q_objects |= Q(**{key: v})
            urls = urls.filter(q_objects)
        try:
            urls = urls.filter(**{key: value})
        except Exception:
            pass

    status_entry = request.GET.get('status')
    if status_entry:
        urls = urls.filter(status=status_entry)

    urls_count = urls.count()

    paginator = Paginator(urls, 250)
    page = request.GET.get('page')
    try:
        urls = paginator.page(page)
    except PageNotAnInteger:
        urls = paginator.page(1)
    except EmptyPage:
        urls = paginator.page(paginator.num_pages)

    context.update({
        'link': True,
        'filter': True,
        'statuses': choices,
        'urls': urls,
        'urls_count': urls_count,
        'urls_filter': True
    })

    return HttpResponse(template.render(context))


@login_required
def url_item(request, url_id):
    data = get_object_or_404(File, id=url_id)
    template = loader.get_template('url-item.html')
    shots = Shot.objects.filter(file=url_id).order_by('-id')

    choices = dict()

    for choice in CHOICE_FILE_STATUS:
        choices[choice[0]] = {'name': choice[1]}

    search_query = request.GET.get('search')
    if search_query:
        search_filter = Q(name__icontains=search_query)
        shots = shots.filter(search_filter)

    status_entry = request.GET.get('status')
    if status_entry:
        shots = shots.filter(status=status_entry)

    shots_count = shots.count()

    paginator = Paginator(shots, 250)
    page = request.GET.get('page')
    try:
        shots = paginator.page(page)
    except PageNotAnInteger:
        shots = paginator.page(1)
    except EmptyPage:
        shots = paginator.page(paginator.num_pages)

    context = {
        'link': True,
        'filter': True,
        'data': data,
        'shots': shots,
        'shots_count': shots_count,
        'statuses': choices,
        'request': request,
        'user': request.user
    }
    context.update(csrf(request))

    return HttpResponse(template.render(context))


@login_required
def shots(request):
    context = default_context(request, "index", TextPage)
    template = loader.get_template('shots.html')
    shots = Shot.objects.all()
    urls = File.objects.all()

    choices = dict()

    for choice in CHOICE_SHOT_STATUS:
        choices[choice[0]] = {'name': choice[1]}

    search_query = request.GET.get('search')
    if search_query:
        search_filter = Q(name__icontains=search_query)
        shots = shots.filter(search_filter)

    # фильтр по левому меню
    left_filter = request.GET.dict()
    if left_filter.get('left_filter'):
        left_filter.pop('filter_p_sort')

    for key in left_filter.keys():
        value = left_filter.get(key)
        if ',' in value:
            values = [int(v) for v in value.split(',')]
            q_objects = Q()
            for v in values:
                q_objects |= Q(**{key: v})
            shots = shots.filter(q_objects)
        try:
            shots = shots.filter(**{key: value})
        except Exception:
            pass

    status_entry = request.GET.get('status')
    if status_entry:
        shots = shots.filter(status=status_entry)

    shots_count = shots.count()

    paginator = Paginator(shots, 250)
    page = request.GET.get('page')
    try:
        shots = paginator.page(page)
    except PageNotAnInteger:
        shots = paginator.page(1)
    except EmptyPage:
        shots = paginator.page(paginator.num_pages)

    context.update({
        'link': True,
        'filter': True,
        'statuses': choices,
        'shots': shots,
        'shots_count': shots_count,
        'urls': urls
    })

    return HttpResponse(template.render(context))


@login_required
def check_domains(request):
    context = default_context(request, "index", TextPage)
    template = loader.get_template('check-domains.html')
    domains = Domain.objects.filter(status=4).order_by('-id')
    current_user = request.user
    if current_user.is_staff:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(user=current_user)

    choices = dict()

    for choice in CHOICE_DOMAIN_STATUS:
        choices[choice[0]] = {'name': choice[1]}

    search_query = request.GET.get('search')
    if search_query:
        search_filter = Q(name__icontains=search_query)
        domains = domains.filter(search_filter)

    # фильтр по левому меню
    left_filter = request.GET.dict()
    if left_filter.get('left_filter'):
        left_filter.pop('filter_p_sort')

    for key in left_filter.keys():
        value = left_filter.get(key)
        if ',' in value:
            values = [int(v) for v in value.split(',')]
            q_objects = Q()
            for v in values:
                q_objects |= Q(**{key: v})
            domains = domains.filter(q_objects)
        try:
            domains = domains.filter(**{key: value})
        except Exception:
            pass

    status_entry = request.GET.get('status')
    if status_entry:
        domains = domains.filter(status=status_entry)

    domains_count = domains.count()

    paginator = Paginator(domains, 250)
    page = request.GET.get('page')
    try:
        domains = paginator.page(page)
    except PageNotAnInteger:
        domains = paginator.page(1)
    except EmptyPage:
        domains = paginator.page(paginator.num_pages)

    context.update({
        'link': True,
        'filter': True,
        'domains': domains,
        'domains_count': domains_count,
        'statuses': choices,
        'projects': projects,
        'ahrefs_rank': True,
        'domains_filter': True,
    })

    return HttpResponse(template.render(context))


@login_required
def domains_timestamps(request):
    context = default_context(request, "index", TextPage)
    template = loader.get_template('domains-timestamps.html')
    domains = Domain.objects.filter(status=6).order_by('-id')
    current_user = request.user
    if current_user.is_staff:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(user=current_user)

    choices = dict()

    for choice in CHOICE_DOMAIN_STATUS:
        choices[choice[0]] = {'name': choice[1]}

    search_query = request.GET.get('search')
    if search_query:
        search_filter = Q(name__icontains=search_query)
        domains = domains.filter(search_filter)

    # фильтр по левому меню
    left_filter = request.GET.dict()
    if left_filter.get('left_filter'):
        left_filter.pop('filter_p_sort')

    for key in left_filter.keys():
        value = left_filter.get(key)
        if ',' in value:
            values = [int(v) for v in value.split(',')]
            q_objects = Q()
            for v in values:
                q_objects |= Q(**{key: v})
            domains = domains.filter(q_objects)
        try:
            domains = domains.filter(**{key: value})
        except Exception:
            pass

    status_entry = request.GET.get('status')
    if status_entry:
        domains = domains.filter(status=status_entry)

    domains_count = domains.count()

    paginator = Paginator(domains, 250)
    page = request.GET.get('page')
    try:
        domains = paginator.page(page)
    except PageNotAnInteger:
        domains = paginator.page(1)
    except EmptyPage:
        domains = paginator.page(paginator.num_pages)

    context.update({
        'link': True,
        'filter': True,
        'domains': domains,
        'domains_count': domains_count,
        'statuses': choices,
        'projects': projects,
        'ahrefs_rank': True,
        'domains_filter': True
    })

    return HttpResponse(template.render(context))


@login_required
def proxy(request):
    context = default_context(request, "index", TextPage)
    template = loader.get_template('proxy.html')
    proxies = Proxy.objects.all()

    context.update({
        'link': True,
        'proxies': proxies
    })

    return HttpResponse(template.render(context))


@login_required
def get_urls_domain(request, domen_id):
    urls = File.objects.filter(domain__id=domen_id).select_related('domain')
    urls_data = [{"name": url.url, "id": url.id} for url in urls]
    nested_urls = create_nested_url_list(urls_data)
    return JsonResponse({'nested_urls': nested_urls})


def create_nested_url_list(urls_data):
    # Создаем пустой словарь для хранения вложенных уровней
    nested_urls = {}

    for idx, url_info in enumerate(urls_data):
        url = url_info['name']
        if not validators.url(url):
            # Если ссылка невалидна, пропускаем ее и переходим к следующей итерации цикла
            continue

        # Добавляем слеш в конец URL, если его там нет
        if not url.endswith('/'):
            url_with_slash = url + '/'
        else:
            url_with_slash = url

        # Разделяем URL на протокол и оставшуюся часть
        protocol, remaining_url = url_with_slash.split('://')

        parts = remaining_url.split('/')  # Разбиваем URL на части

        current_level = nested_urls
        # Если учитываем протокол
        if protocol not in current_level:
            current_level[protocol] = {}

        current_level = current_level[protocol]

        for part in parts:
            if part not in current_level:
                current_level[part] = {'count': 0}  # Создаем новый уровень и счетчик
            current_level = current_level[part]  # Переходим на следующий уровень
            current_level['count'] += 1  # Увеличиваем счетчик на этом уровне

        # Добавляем id и ссылку к текущему уровню, только если есть id в urls_data
        if 'id' in url_info:
            current_level['id'] = url_info['id']
            current_level['link'] = url

    return nested_urls


@receiver(post_save, sender=Domain)
def send_update_to_websocket(sender, instance, **kwargs):
    channel_layer = get_channel_layer()

    serialized_data = serialize('json', [instance])
    deserialized_data = json.loads(serialized_data)[0]
    domains = Domain.objects.filter(id=deserialized_data['pk'])
    domains_main = Domain.objects.all()
    domains_count_not_checked = domains_main.exclude(status=4).count()
    domains_count_checked = domains_main.filter(status=4).count()
    domains_count_timestamps = domains_main.filter(status=6).count()
    html_content = render_domains(None, domains)
    data = {
        'html_content': html_content,
        'serialized_data': serialized_data,
        'domains_count_not_checked': domains_count_not_checked,
        'domains_count_checked': domains_count_checked,
        'domains_count_timestamps': domains_count_timestamps,
    }
    json_data = json.dumps(data)

    async_to_sync(channel_layer.group_send)(
        "domains_group",
        {
            "type": "send_update",
            "text": 'json_data'
        }
    )


def ajax(request):
    result = dict()
    if request.method == 'POST':
        obj_info = {}
        data = json.loads(request.body)
        if data.get('type') == 'new_group':
            try:
                current_user = request.user
                for name in data:
                    if name != 'type':
                        obj_info[name] = data.get(name, '')
                Project.objects.create(user=current_user, **obj_info)
                if current_user.is_staff:
                    project = Project.objects.all()
                else:
                    project = Project.objects.filter(user=current_user)
                result = render_groups(request, project)
                return HttpResponse(result)
            except Exception as e:
                result = {"error": e}
        if data.get('type') == 'save_phrase':
            try:
                project = data['project']
                phrases = data['phrases']
                if project:
                    current_user = request.user
                    project = Project.objects.get(id=project)
                    if phrases:
                        p = phrases.split("\n")
                        for query in p:
                            if query:
                                keys_on_bd = SearchQuery.objects.filter(query=query, project=project)
                                if keys_on_bd.exists():
                                    result = {'status': 'ok'}
                                else:
                                    ph = SearchQuery(query=query, project=project)
                                    ph.save()
                        if current_user.is_staff:
                            project = Project.objects.all().order_by('-id')
                        else:
                            project = Project.objects.filter(user=current_user).order_by('-id')
                        result = render_accordion_projects(request, project)
                        return HttpResponse(result)
                    else:
                        result = {"error": 'The list of phrases is empty'}
                else:
                    result = {"error": 'No project selected'}
            except Exception as e:
                result = {"error": e}
        if data.get('type') == 'delete_phrases':
            try:
                phrase = SearchQuery.objects.get(id=data.get('id'))
                phrase.delete()
                result = {'delete': True}
            except Exception as e:
                result = {"error": e}
        if data.get('type') == 'delete_projects':
            try:
                project = Project.objects.get(id=data.get('id'))
                project.delete()
                result = {'delete': True}
            except Exception as e:
                result = {"error": e}
        if data.get('type') == 'delete_selected_phrases':
            try:
                id_array = data['id_array']
                if id_array:
                    for id_item in id_array:
                        phrase = SearchQuery.objects.get(id=id_item)
                        phrase.delete()
                result = {'delete': True}
            except Exception as e:
                result = {"error": e}
        if data.get('type') == 'delete_selected_projects':
            try:
                id_array = data['id_array']
                if id_array:
                    for id_item in id_array:
                        phrase = Project.objects.get(id=id_item)
                        phrase.delete()
                result = {'delete': True}
            except Exception as e:
                result = {"error": e}
        if data.get('type') == 'change_selected_phrases' or data.get('type') == 'change_selected_domains' or data.get('type') == 'change_selected_urls' or data.get('type') == 'change_selected_shots':
            try:
                model = ''
                if data.get('type') == 'change_selected_phrases':
                    model = SearchQuery
                elif data.get('type') == 'change_selected_domains':
                    model = Domain
                elif data.get('type') == 'change_selected_urls':
                    model = File
                elif data.get('type') == 'change_selected_shots':
                    model = Shot
                status = data['status']
                id_array = data['id_array']
                if id_array:
                    for id_item in id_array:
                        item = model.objects.get(id=id_item)
                        item.status = status
                        item.save()
                result = {'change': True}
            except Exception as e:
                result = {"error": e}
        if data.get('type') == 'add_proxy':
            try:
                proxies = data['proxy']
                if proxies:
                    for proxy in proxies:
                        obj_info = {}
                        for name in proxy:
                            obj_info[name] = proxy.get(name, '')
                        Proxy.objects.create(**obj_info)
                    proxy = Proxy.objects.all()
                    result = render_proxy(request, proxy)
                    return HttpResponse(result)
                else:
                    result = {"error": 'The list of phrases is empty'}
            except Exception as e:
                result = {"error": e}
        if data.get('type') == 'update_proxy':
            try:
                id = data.get('id')
                proxy = Proxy.objects.get(id=id)
                proxy.ip_address = data.get('ip_address')
                proxy.port = data.get('port')
                proxy.username = data.get('username')
                proxy.password = data.get('password')
                proxy.protocol = data.get('protocol')
                proxy.save()
                result = {'update': True}
            except Exception as e:
                result = {"error": e}
        if data.get('type') == 'delete_proxy':
            try:
                id = data['id']
                if id:
                    proxy = Proxy.objects.get(id=id)
                    proxy.delete()
                result = {'delete': True}
            except Exception as e:
                result = {"error": e}
        if data.get('type') == 'get_phrases':
            try:
                id = data.get('id')
                status = data.get('status')
                if status:
                    phrases = SearchQuery.objects.filter(project=id, status=status)
                else:
                    phrases = SearchQuery.objects.filter(project=id)
                result = render_phrases(request, phrases)
                return HttpResponse(result)
            except Exception as e:
                result = {"error": e}

    return JsonResponse(result)