from django.db import models
from django.utils.timezone import now

class Setlist(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=512, default='', blank=True)
    songs = models.ManyToManyField('Song', blank=True)
    owner_group = models.ForeignKey('Group', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
