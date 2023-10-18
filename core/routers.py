from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'proxies', ProxyViewSet, basename='proxy')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'domains', DomainViewSet, basename='domain')
router.register(r"domain_images", DomainImagesViewSet),
router.register(r'file', FileViewSet, basename='file')
router.register(r'shot', FileViewSet, basename='shot')
router.register(r'searchqueries', SearchQueryViewSet, basename='searchquery')

