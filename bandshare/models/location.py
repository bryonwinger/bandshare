from django.db import models

class Location(models.Model):
    country = models.CharField(max_length=64, default='United States of America')
    state = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return self.postal_code

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['country', 'state', 'city', 'postal_code'], name='general location')
        ]