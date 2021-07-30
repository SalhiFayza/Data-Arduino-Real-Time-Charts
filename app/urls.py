
from django.urls import path, re_path
from app import views
app_name = 'app'
urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('fetch_sensor_values_ajax_com', views.fetch_sensor_values_ajax_com,
         name='fetch_sensor_values_ajax_com'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]