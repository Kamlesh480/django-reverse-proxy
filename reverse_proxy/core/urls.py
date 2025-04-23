# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('proxy/<str:endpoint_name>/', views.proxy_request),
    path('server/update/', views.update_server_status),
    path('server/logs/', views.server_logs),
    path('server/add/', views.add_server, name='add-server'),
    path('endpoint/assign/', views.assign_server_to_endpoint),
]