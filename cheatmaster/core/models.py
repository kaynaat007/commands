from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Entity(models.Model):
    """
    Holds entities
    """
    updated_by = models.ForeignKey(User, related_name='updated_by', null=True, blank=True)
    key = models.CharField(max_length=255, unique=True, db_index=True)
    detail = models.TextField(max_length=5 * 1024, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='created_by', null=True, blank=True)
    is_published = models.BooleanField(default=False)


