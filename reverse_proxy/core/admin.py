# core/admin.py

from django.contrib import admin
from .models import Server, Endpoint, EndpointServer

admin.site.register(Server)
admin.site.register(Endpoint)
admin.site.register(EndpointServer)
