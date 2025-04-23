from django.db import models

class Server(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    is_active = models.BooleanField(default=True)
    request_log = models.TextField(default="", blank=True)  # For simple file-based logs

    def __str__(self):
        return f"{self.ip_address} ({'UP' if self.is_active else 'DOWN'})"


class Endpoint(models.Model):
    name = models.CharField(max_length=100, unique=True)
    servers = models.ManyToManyField(Server, through='EndpointServer')

    def __str__(self):
        return self.name


class EndpointServer(models.Model):
    endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)  # For round-robin order