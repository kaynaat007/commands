from django.db import models

# Create your models here.


class SystemCommand(models.Model):
    cmd = models.CharField(max_length=255, unique=True)
    detail = models.CharField(max_length=2 * 1024, null=True, blank=True)

