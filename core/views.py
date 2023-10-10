import django_filters
from django_filters import rest_framework as filters

from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from django.contrib.auth.models import User
from .models import Proxy, Project, Domain, SearchQuery



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




class ProxyViewSet(viewsets.ModelViewSet):
    queryset = Proxy.objects.all()
    serializer_class = ProxySerializer

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

class SearchQueryViewSet(viewsets.ModelViewSet):
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


