from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('map/', include('map.urls')),
    path('statistic/', include('statist.urls')),
    path('about_project/', include('about_project.urls'))
]
