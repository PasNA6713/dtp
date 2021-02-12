from django.urls import path

from . import views


urlpatterns = [
    path('', views.GetClastersView.as_view()),
]