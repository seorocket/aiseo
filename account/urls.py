from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url, include

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    url(r'^login/$', views.user_login, name='login'),
    path('logout/', views.my_logout, name="logout"),
]