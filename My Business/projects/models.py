from django.db import models
from partners.models import Partner


class Project(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    partner = models.ForeignKey(Partner, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company
