import django_filters
from django_filters import rest_framework as filters

from rest_framework import viewsets
from rest_framework.filters import SearchFilter
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
