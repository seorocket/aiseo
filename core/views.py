import django_filters
import random
from django_filters import rest_framework as filters
import json

from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .templates_resolve import *
from django.contrib.auth.models import User
from .models import *
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template import loader
from django.template.context_processors import csrf
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


class UserFilter(filters.FilterSet):
    username = django_filters.CharFilter(field_name="username")

    class Meta:
        model = User
        fields = ['username']


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    # permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filterset_class = UserFilter

    def get_queryset(self):
        return User.objects.all()


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


def index(request):
    context = default_context(request, "index", TextPage)
    template = loader.get_template('index.html')
    projects = Project.objects.all()

    context.update({
        'link': True,
        'projects': projects
    })

    return HttpResponse(template.render(context))


def phrases(request):
    context = default_context(request, "index", TextPage)
    template = loader.get_template('phrases.html')
    projects = Project.objects.all()
    keys = SearchQuery.objects.all()

    status_entry = request.GET.get('status')
    if status_entry:
        keys = keys.filter(status=status_entry)

    choices = dict()

    for choice in CHOICE_DOMAIN_STATUS:
        choices[choice[0]] = {'name': choice[1]}

    context.update({
        'link': True,
        'projects': projects,
        'keys': keys,
        'statuses': choices,
    })

    return HttpResponse(template.render(context))


def projects(request):
    context = default_context(request, "index", TextPage)
    template = loader.get_template('projects.html')
    projects = Project.objects.all()

    context.update({
        'link': True,
        'projects': projects,
    })

    return HttpResponse(template.render(context))


def domains(request):
    context = default_context(request, "index", TextPage)
    template = loader.get_template('domains.html')
    domains = Domain.objects.all()

    choices = dict()

    for choice in CHOICE_DOMAIN_STATUS:
        choices[choice[0]] = {'name': choice[1]}

    projects = Project.objects.all()

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

    context.update({
        'link': True,
        'filter': True,
        'domains': domains,
        'statuses': choices,
        'projects': projects,
        'ahrefs_rank': True,
        'domains_filter': True
    })

    return HttpResponse(template.render(context))


def domain_item(request, domain_id):
    data = get_object_or_404(Domain, id=domain_id)
    template = loader.get_template('domain-item.html')

    urls = File.objects.filter(domain=domain_id)

    choices = dict()

    for choice in CHOICE_FILE_STATUS:
        choices[choice[0]] = {'name': choice[1]}

    status_entry = request.GET.get('status')
    if status_entry:
        urls = urls.filter(status=status_entry)

    urls_data = [{"name": url.url, "id": url.id} for url in urls]
    nested_urls = create_nested_url_list(urls_data)

    context = {
        'link': True,
        'filter': True,
        'data': data,
        'urls': urls,
        'statuses': choices,
        'request': request,
        'nested_urls': nested_urls
    }
    context.update(csrf(request))

    return HttpResponse(template.render(context))


def urls(request):
    context = default_context(request, "index", TextPage)
    template = loader.get_template('urls.html')
    urls = File.objects.all()
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

    context.update({
        'link': True,
        'filter': True,
        'statuses': choices,
        'urls': urls,
        'domains': domains,
    })

    return HttpResponse(template.render(context))


def url_item(request, url_id):
    data = get_object_or_404(File, id=url_id)
    template = loader.get_template('url-item.html')

    shots = Shot.objects.filter(file=url_id)

    choices = dict()

    for choice in CHOICE_FILE_STATUS:
        choices[choice[0]] = {'name': choice[1]}

    status_entry = request.GET.get('status')
    if status_entry:
        shots = shots.filter(status=status_entry)

    context = {
        'link': True,
        'filter': True,
        'data': data,
        'shots': shots,
        'statuses': choices,
        'request': request,
    }
    context.update(csrf(request))

    return HttpResponse(template.render(context))


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

    context.update({
        'link': True,
        'filter': True,
        'statuses': choices,
        'shots': shots,
        'urls': urls
    })

    return HttpResponse(template.render(context))


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


class ProxyViewSet(viewsets.ModelViewSet):
    queryset = Proxy.objects.all()
    serializer_class = ProxySerializer

    @action(detail=False, methods=['get'])
    def get_random_proxy(self, request):
        valid_proxies = Proxy.objects.filter(status=0)  # Фильтруем только действительные (valid) прокси

        if valid_proxies.exists():
            random_proxy = random.choice(valid_proxies)  # Выбираем случайный действительный прокси
            proxy_url = f"{random_proxy.protocol}://{random_proxy.username}:{random_proxy.password}@{random_proxy.ip_address}:{random_proxy.port}"

            return Response({'proxy_url': proxy_url}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Не найдено действительных прокси."}, status=status.HTTP_404_NOT_FOUND)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer

    @action(detail=False, methods=['get'])
    def update_status(self, request):
        status_param = request.query_params.get('status', None)
        if status_param is None:
            return Response({"error": "Параметр 'status' не указан в запросе."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            status_code = int(status_param)
        except ValueError:
            return Response({"error": "Параметр 'status' должен быть числом."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Domain.objects.filter(status=status_code)

        if not queryset.exists():
            return Response({"error": f"По статусу {status_code} не найдено объектов Domain."},
                            status=status.HTTP_404_NOT_FOUND)

        # Обновляем статус первого объекта в queryset на 3
        first_domain = queryset.first()
        first_domain.status = 2
        first_domain.save()

        # Возвращаем объект Domain с обновленным статусом
        serializer = DomainSerializer(first_domain)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchQueryFilter(filters.FilterSet):
    project = django_filters.CharFilter(field_name="project")
    status = django_filters.CharFilter(field_name="status")

    class Meta:
        model = SearchQuery
        fields = ['project', 'status']


class SearchQueryViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filterset_class = SearchQueryFilter
    queryset = SearchQuery.objects.all()
    serializer_class = SearchQuerySerializer

    @action(detail=False, methods=['get'])
    def update_status(self, request):
        status_param = request.query_params.get('status', None)
        if status_param is None:
            return Response({"error": "Параметр 'status' не указан в запросе."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            status_code = int(status_param)
        except ValueError:
            return Response({"error": "Параметр 'status' должен быть числом."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = SearchQuery.objects.filter(status=status_code)

        if not queryset.exists():
            return Response({"error": f"По статусу {status_code} не найдено объектов SearchQuery."},
                            status=status.HTTP_404_NOT_FOUND)

        # Обновляем статус первого объекта в queryset на 3
        first_query = queryset.first()
        first_query.status = 2
        first_query.save()

        # Возвращаем объект SearchQuery с обновленным статусом
        serializer = SearchQuerySerializer(first_query)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        queries = request.data.get('queries', [])
        created_queries = []

        for query in queries:
            project_id = query.pop('project', None)  # Удаляем поле "project" из словаря
            if project_id:
                project = Project.objects.get(pk=project_id)  # Получаем объект Project по id
                query['project'] = project  # Присваиваем объект Project обратно в словарь
                serializer = SearchQuerySerializer(data=query)
                if serializer.is_valid():
                    created_queries.append(serializer.save())

        return Response(SearchQuerySerializer(created_queries, many=True).data, status=status.HTTP_201_CREATED)

'''
Формат запроса: 
/api/searchqueries/bulk_create/?format=json
{
    "queries": [
        {"project": 1, "query": "query1"},
        {"project": 1, "query": "query2"}
    ]
}
'''


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    # ... Ваш существующий код ...

    @action(detail=False, methods=['get'])
    def update_status(self, request):
        status_param = request.query_params.get('status', None)
        if status_param is None:
            return Response({"error": "Параметр 'status' не указан в запросе."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            status_code = int(status_param)
        except ValueError:
            return Response({"error": "Параметр 'status' должен быть числом."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = File.objects.filter(status=status_code)

        if not queryset.exists():
            return Response({"error": f"По статусу {status_code} не найдено объектов File."},
                            status=status.HTTP_404_NOT_FOUND)

        # Обновляем статус первого объекта в queryset на 3
        first_file = queryset.first()
        first_file.status = 3
        first_file.save()

        # Возвращаем объект File с обновленным статусом
        serializer = FileSerializer(first_file)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShotViewSet(viewsets.ModelViewSet):
    queryset = Shot.objects.all()
    serializer_class = ShotSerializer

    # ... Ваш существующий код ...

    @action(detail=False, methods=['get'])
    def update_status(self, request):
        status_param = request.query_params.get('status', None)
        if status_param is None:
            return Response({"error": "Параметр 'status' не указан в запросе."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            status_code = int(status_param)
        except ValueError:
            return Response({"error": "Параметр 'status' должен быть числом."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Shot.objects.filter(status=status_code)

        if not queryset.exists():
            return Response({"error": f"По статусу {status_code} не найдено объектов Shot."},
                            status=status.HTTP_404_NOT_FOUND)

        # Обновляем статус первого объекта в queryset на 3
        first_shot = queryset.first()
        first_shot.status = 3
        first_shot.save()

        # Возвращаем объект Shot с обновленным статусом
        serializer = ShotSerializer(first_shot)
        return Response(serializer.data, status=status.HTTP_200_OK)


def ajax(request):
    result = dict()
    if request.method == 'POST':
        obj_info = {}
        data = json.loads(request.body)
        if data.get('type') == 'new_group':
            try:
                for name in data:
                    if name != 'type':
                        obj_info[name] = data.get(name, '')
                Project.objects.create(**obj_info)
                project = Project.objects.all()
                result = render_groups(request, project)
                return HttpResponse(result)
            except Exception as e:
                result = {"error": e}
        if data.get('type') == 'save_phrase':
            try:
                project = data['project']
                phrases = data['phrases']
                if project:
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
                                    result = {"status": True}
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
        if data.get('type') == 'delete_selected':
            try:
                id_array = data['id_array']
                if id_array:
                    for id_item in id_array:
                        phrase = SearchQuery.objects.get(id=id_item)
                        phrase.delete()
                result = {'delete': True}
            except Exception as e:
                result = {"error": e}

    return JsonResponse(result)