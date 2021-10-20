from django.db import models
from django.utils.timezone import now

class Group(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_date = models.DateField(default=now)

    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512, blank=True)
    bio = models.CharField(max_length=4096, blank=True)

    members = models.ManyToManyField('User')
    genres = models.ManyToManyField('Genre')
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, blank=True, null=True)
