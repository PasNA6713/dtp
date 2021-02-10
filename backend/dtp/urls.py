from django.urls import path

from . import views


urlpatterns = [
    path("dtp/create/", views.DtpCreateView.as_view()),
    path("dtp/retrieve/<int:pk>/", views.DtpRetrieveView.as_view()),
    path("dtp/list/", views.DtpListView.as_view()),
    path('get-filter-params/', views.GetFilterParams.as_view()),
]