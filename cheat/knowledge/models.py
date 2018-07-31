from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class SystemCommand(models.Model):
    cmd = models.CharField(max_length=255, unique=True)
    detail = models.CharField(max_length=2 * 1024, null=True, blank=True)


class People(models.Model):

    username = models.CharField(max_length=255, unique=True)


class Entity(models.Model):
    """
    Holds entities.
    """
    updated_by = models.ForeignKey(People, related_name='updated_by',  null=True, blank=True)
    key = models.CharField(max_length=255, unique=True, db_index=True)
    detail = models.TextField(max_length=5 * 1024, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(People, null=True, related_name='created_by',  blank=True)
    is_published = models.BooleanField(default=False)



