from django.urls import path

from . import views


urlpatterns = [
    path('<int:number>/', views.GetClastersView.as_view()),
]