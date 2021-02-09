from django.urls import path
from . import views

urlpatterns = [
    path('', views.present, name='map'),
    path('change/heatmap', views.change_heatmap, name="change_haetmap"),
    path('change/camera', views.change_camera_map, name="change_camera"),
    path('add-point', views.add_point),
    path('load', views.load_data),
]