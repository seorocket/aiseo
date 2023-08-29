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

class SearchQueryViewSet(viewsets.ModelViewSet):
    queryset = SearchQuery.objects.all()
    serializer_class = SearchQuerySerializer


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