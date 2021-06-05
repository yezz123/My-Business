from django.db import models


class Server(models.Model):
    uid = models.IntegerField(primary_key=True)
    root_password = models.CharField(max_length=32)
    services = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_services(self):
        return self.services.splitlines()
