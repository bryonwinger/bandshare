from django.db import models
from django.utils.timezone import now

class Group(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_date = models.DateField(default=now)

    name = models.CharField(max_length=256)
    members = models.ManyToManyField('User')
    genres = models.ManyToManyField('Genre')
