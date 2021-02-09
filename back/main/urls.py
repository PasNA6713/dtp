from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name="login"),
    path('about_us', views.about, name='about'),
    path('statist', include('statist.urls'), name='graph'),
    path('about_project', include('about_project.urls'), name='inform'),
    path('create-user', views.create_user, name="create-user"),
    path('map', include('map.urls'), name='map')
]