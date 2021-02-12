from django.urls import path

from . import views


urlpatterns = [
    path("create/", views.DtpCreateView.as_view()),
    path("destroy/<int:pk>/", views.DtpDestroyView.as_view()),
    path("retrieve/<int:pk>/", views.DtpRetrieveView.as_view()),
    path("some/", views.GetSomeDtps.as_view()),
    path("list/", views.DtpListView.as_view()),
   

    path('get-filter-params/', views.GetFilterParams.as_view()),
]