from django.db import models

class Artist(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(unique=True, max_length=256)

    def __str__(self):
        return self.name
