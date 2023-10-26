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
from rest_framework.pagination import PageNumberPagination


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


class CustomPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'  # Параметр запроса для изменения количества объектов на странице
    max_page_size = 100


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


class DomainFilter(filters.FilterSet):
    project = django_filters.CharFilter(field_name="project")

    class Meta:
        model = Domain
        fields = ['project']


class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filterset_class = DomainFilter
    changed_objects = []

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


class DomainImagesFilter(filters.FilterSet):
    domain_id = django_filters.CharFilter(field_name="domain_id")

    class Meta:
        model = DomainImages
        fields = ['domain_id']


class DomainImagesViewSet(viewsets.ModelViewSet):
    queryset = DomainImages.objects.all()
    serializer_class = DomainImagesSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filterset_class = DomainImagesFilter

    @action(detail=False, methods=['get'])
    def add_domain_image(self, request):
        if request.method == 'GET':
            file_names = request.GET.get('file', '').split(',')
            domain_id = request.GET.get('domain_id')
            if domain_id:
                try:
                    domain_id = int(domain_id)
                    domain = Domain.objects.get(id=domain_id)  # Получаем объект Domain по id
                except (ValueError, Domain.DoesNotExist):
                    return JsonResponse({'error': 'Invalid domain_id'}, status=400)

                for file_name in file_names:
                    DomainImages.objects.create(photo=f'image_domain/{file_name}', domain_id=domain)

                return JsonResponse({'success': 'DomainImages records added successfully'}, status=200)

            return JsonResponse({'error': 'domain_id parameter is missing'}, status=400)

        return JsonResponse({'error': 'Invalid request method'}, status=405)


class SearchQueryFilter(filters.FilterSet):
    project = django_filters.CharFilter(field_name="project")
    status = django_filters.CharFilter(field_name="status")

    class Meta:
        model = SearchQuery
        fields = ['project', 'status']


class SearchQueryViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPagination
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

    @action(detail=False, methods=['get'])
    def check_status(self, request):
        project_id = self.request.query_params.get('project', None)

        if project_id is not None:
            search_queries = SearchQuery.objects.filter(project_id=project_id)
        else:
            search_queries = SearchQuery.objects.all()

        count = search_queries.count()
        message = ''
        if count:
            added = search_queries.filter(status=0).count()
            done = search_queries.filter(status=1).count()
            inprogress = search_queries.filter(status=2).count()
            error = search_queries.filter(status=3).count()

            percentage = round((done / count) * 100, 1) if count > 0 else 0
            status_message = ""

            if done == count:
                status_message = 'Completed'
            elif done+added == count:
                status_message = 'There are not verified'
            elif done+error == count:
                status_message = 'There are errors'
            elif done+error+added == count:
                status_message = 'There are tested, not tested and errors'
            elif error+added == count:
                status_message = 'There are errors and not verified'
            elif error == count:
                status_message = 'Error'
            elif added == count:
                status_message = 'Added'
            else:
                status_message = 'In process'

            message = f'{done}/{count} ({percentage}%) {status_message}'

        response_data = {
            'status': message
        }

        return Response(data=response_data, status=status.HTTP_200_OK)

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

    @action(detail=False, methods=['post'])
    def bulk_create_files(self, request):
        data = request.data
        serializer = FileSerializer(data=data, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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

    @action(detail=False, methods=['post'])
    def bulk_create_shots(self, request):
        data = request.data
        serializer = ShotSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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