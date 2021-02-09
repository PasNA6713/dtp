from django.urls import path, include
from . import views
from .views import graph


urlpatterns = [
    #path('', views.statist, name='statist'),
    path('', graph, name='graph'),

]